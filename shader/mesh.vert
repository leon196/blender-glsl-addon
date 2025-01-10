
attribute vec3 position;

uniform mat4 worldMatrix;
uniform mat4 viewMatrix;
uniform mat4 windowMatrix;

varying vec2 uv;

void main()
{
    uv = position.xy;
    gl_Position = windowMatrix * viewMatrix * worldMatrix * vec4(position, 1.);
}