precision mediump float;

varying vec2 uv;
uniform float angle;
uniform float count;
uniform float size;
uniform float range;
uniform float falloff;
uniform float noise;
uniform float easing;
uniform float blend;
uniform float tick;
uniform mat4 viewMatrix;
uniform mat4 viewMatrixInvert;
uniform mat4 windowMatrixInvert;
vec4 FragColor;

mat2 rot(float a) { float c=cos(a), s=sin(a); return mat2(c,s,-s,c); }

// Inigo Quilez
// https://iquilezles.org/articles/distfunctions/
float smin( float d1, float d2, float k )
{
    float h = clamp( 0.5 + 0.5*(d2-d1)/k, 0.0, 1.0 );
    return mix( d2, d1, h ) - k*h*(1.0-h);
}
float smax( float d1, float d2, float k )
{
    float h = clamp( 0.5 - 0.5*(d2+d1)/k, 0.0, 1.0 );
    return mix( d2, -d1, h ) + k*h*(1.0-h);
}
float sdBox( vec3 p, vec3 b )
{
  vec3 q = abs(p) - b;
  return length(max(q,0.0)) + min(max(q.x,max(q.y,q.z)),0.0);
}

// Dave Hoskins
// https://www.shadertoy.com/view/4djSRW
vec4 hash44(vec4 p4)
{
	p4 = fract(p4  * vec4(.1031, .1030, .0973, .1099));
    p4 += dot(p4, p4.wzxy+33.33);
    return fract((p4.xxyz+p4.yzzw)*p4.zywx);
}

// hornet
// https://www.shadertoy.com/view/MslGR8
// http://advances.realtimerendering.com/s2014/index.html
float InterleavedGradientNoise( vec2 uv )
{
    const vec3 magic = vec3( 0.06711056, 0.00583715, 52.9829189 );
    return fract( magic.z * fract( dot( uv, magic.xy ) ) );
}

// blackle
// https://suricrasia.online/blog/shader-functions/
vec3 erot(vec3 p, vec3 ax, float ro) {
  return mix(dot(ax, p)*ax, p, cos(ro)) + cross(ax,p)*sin(ro);
}

vec3 rndrot(vec3 p, vec4 rnd) {
  return erot(p, normalize(tan(rnd.xyz)), rnd.w*acos(-1.));
}

float gyroid (vec3 p) { return dot(cos(p), sin(p.yzx)); }

float fbm (vec3 p) {
    float r = 0.;
    float a = .5;
    for (float i = 0.; i < 6.; ++i)
    {
        p += r * .2;
        r += pow(abs(gyroid(p/a)), easing)*a;
        a /= 1.8;
    }
    return 1.-atan(r);
}

float map (vec3 p)
{
    float d = 100.;
    float spice = fbm(p);
    float plane = p.z;
    float sphere = length(p)-size;

    float a = 1.;
    float t = angle;
    for (float i = 0.; i < count; ++i)
    {
        p.xy *= rot(t+a);
        p.yz *= rot(t+a);
        p = abs(p)-range*a;
        d = smin(d, length(p)-size*a, blend*a);
        a /= falloff;
    }

    d = smax(sphere, d, 1.);
    d += spice * noise;
    d = abs(d) - .01;

    return d;
}

void main ()
{
    vec3 color = vec3(0);
    float alpha = 0.;
    vec2 p = uv - 0.5;
    vec3 pos = viewMatrixInvert[3].xyz;
    vec3 ray = normalize(mat3(viewMatrixInvert) * (windowMatrixInvert * vec4(p*2.,-1,1)).xyz);
    vec4 rng = hash44(vec4(gl_FragCoord.xy, 196., tick));
    float dither = InterleavedGradientNoise(gl_FragCoord.xy);

    float shade = 0.;
    float total = 0.;
    float dist = 0.;
    float max_dist = 1000.;
    for (shade = 1.; shade > 0.; shade -= 1./200.)
    {
        dist = map(pos);
        if (dist < 0.001 * total || total > max_dist) break;
        dist *= 0.5 + 0.1 * dither;
        total += dist;
        pos += ray * dist;
    }
    if (total < max_dist)
    {
        color = vec3(1);
        vec2 e1 = vec2(.5+.02*rng.y,0);
        vec2 e2 = vec2(.02,0);
        vec2 e3 = vec2(.1,0);
        vec2 e4 = vec2(5.,0);
        #define M(u) map(pos-u)
        vec3 n1 = normalize(dist - vec3(M(e1.xyy),M(e1.yxy),M(e1.yyx)));
        vec3 n2 = normalize(dist - vec3(M(e2.xyy),M(e2.yxy),M(e2.yyx)));
        vec3 n3 = normalize(dist - vec3(M(e3.xyy),M(e3.yxy),M(e3.yyx)));
        vec3 n4 = normalize(dist - vec3(M(e4.xyy),M(e4.yxy),M(e4.yyx)));
        n1 = normalize(mat3(viewMatrix) * n1);
        n2 = normalize(mat3(viewMatrix) * n2);
        n3 = normalize(mat3(viewMatrix) * n3);
        n4 = normalize(mat3(viewMatrix) * n4);
        color = vec3(0);
        color += vec3(0.5,.5,1)*pow(.5+.5*dot(n2, normalize(vec3(0,2,0))), 2.);
        color += vec3(1,.5,0)*(1.-pow(abs(n1.z), 1.));
        color += vec3(.5,1,.5)*(1.-pow(abs(n2.z), 1.));

        #define AO(u) clamp(abs((dist - M(ray*u))/u),0.,1.)
        color *= AO(.1);
        color *= AO(.5);
        color *= AO(1.);
        color *= .5+.5*smoothstep(.1,.9,n2.y+.5);
        color *= .5+.5*smoothstep(.0,.5,n3.z);
        color *= shade;
    }

    FragColor = vec4(color, 1.);
}