#extension GL_EXT_draw_instanced: enable

attribute vec3 position;

uniform mat4 worldMatrix;
uniform mat4 viewMatrix;
uniform mat4 windowMatrix;

uniform float stretch;
uniform float range;
uniform float time;

varying vec2 uv;

mat2 rot(float a) { float c=cos(a), s=sin(a); return mat2(c,s,-s,c); }

// Dave Hoskins
// https://www.shadertoy.com/view/4djSRW
vec4 hash44(vec4 p4)
{
	p4 = fract(p4  * vec4(.1031, .1030, .0973, .1099));
    p4 += dot(p4, p4.wzxy+33.33);
    return fract((p4.xxyz+p4.yzzw)*p4.zywx);
}

vec3 curve (float t, float id)
{
    vec3 p = vec3(1,0,0);

    vec4 rng = hash44(vec4(id+7583.));
    vec4 rng2 = hash44(vec4(id+7583.));

    p = (rng.xyz-.5)*range;
 
    p.xz *= rot(t*2.+rng2.y);
    p.yx *= rot(t*3.+rng2.z);

    return p;
}

void main()
{
    float id = float(gl_InstanceID);
    vec4 rng = hash44(vec4(id+775.));
    vec4 rng2 = hash44(vec4(id+9576.));

    vec3 pos = position;
    float x = position.x;
    float y = position.y;

    pos = curve(y * stretch * (1.+rng2.x) + time, id);
    pos.z += x * .05;
    // pos += (rng.xyz-.5);//*(1.+rng.w);

    gl_Position = windowMatrix * viewMatrix * worldMatrix * vec4(pos, 1.);
    uv = position.xy*.5+.5;
}