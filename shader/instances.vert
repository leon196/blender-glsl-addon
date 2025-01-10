#extension GL_EXT_draw_instanced: enable

attribute vec3 position;
// attribute vec3 normal;

uniform mat4 worldMatrix;
uniform mat4 viewMatrix;
uniform mat4 windowMatrix;

varying vec2 uv;
// varying vec3 normal;

// Dave Hoskins
// https://www.shadertoy.com/view/4djSRW
vec4 hash44(vec4 p4)
{
	p4 = fract(p4  * vec4(.1031, .1030, .0973, .1099));
    p4 += dot(p4, p4.wzxy+33.33);
    return fract((p4.xxyz+p4.yzzw)*p4.zywx);
}

void main()
{
    uv = position.xy;
    vec3 pos = position;
    // pos += hash44(vec4(gl_InstanceID+357.))-.5)
    float id = float(gl_InstanceID);
    float grid = 10.;
    float x = mod(id, grid);
    float y = floor(mod(id, (grid*grid))/grid);
    float z = floor(id/(grid*grid));
    pos += vec3(x, y, z);
    gl_Position = windowMatrix * viewMatrix * worldMatrix * vec4(pos, 1.);
}