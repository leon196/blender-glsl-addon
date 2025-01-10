precision mediump float;

varying vec2 uv;
uniform float angle;
uniform float count;
uniform float size;
uniform float range;
uniform float falloff;
uniform float tick;
uniform mat4 viewMatrix;
uniform mat4 viewMatrixInvert;
uniform mat4 windowMatrixInvert;
vec4 FragColor;

mat2 rot(float a) { float c=cos(a), s=sin(a); return mat2(c,s,-s,c); }

// Inigo Quilez
// https://iquilezles.org/articles/distfunctions/
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

float map (vec3 p)
{
    float d = 100.;
    float a = 1.;
    float t = angle;
    for (float i = 0.; i < count; ++i)
    {
        p.xy *= rot(t+a);
        p = abs(p)-range*a;
        d = min(d, sdBox(p, vec3(size*a)));
        a /= falloff;
    }
    return abs(d) - .01;
}

void main ()
{
    vec3 color = vec3(0);
    float alpha = 0.;
    vec2 p = uv - 0.5;
    vec3 pos = viewMatrixInvert[3].xyz;
    vec3 ray = normalize(mat3(viewMatrixInvert) * (windowMatrixInvert * vec4(p*2.,-1,1)).xyz);
    vec4 rng = hash44(vec4(gl_FragCoord.xy, 196., tick));
    float shade = 0.;
    float total = 0.;
    float dist = 0.;
    float max_dist = 100.;
    for (shade = 1.; shade > 0.; shade -= 1./200.)
    {
        dist = map(pos);
        if (dist < 0.001 * total || total > max_dist) break;
        dist *= 0.9 + 0.1 * rng.z;
        total += dist;
        pos += ray * dist;
    }
    if (total < max_dist)
    {
        #define M(u) map(pos-u)
        #define AO(u) clamp(abs((dist - M(ray*u))/u),0.,1.)
        #define N(x,y,z) normalize(vec3(x,y,z))
        color = vec3(1);
        color *= AO(.01);
        color *= AO(.1);
        color *= AO(1.);
        color *= shade;
    }

    FragColor = vec4(color, 1.);
}