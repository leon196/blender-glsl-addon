precision mediump float;

uniform sampler2D image;
uniform float fade;
varying vec2 uv;
vec4 FragColor;

void main()
{
    FragColor = texture2D(image, uv) * fade;
}