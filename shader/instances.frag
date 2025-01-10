precision mediump float;

varying vec2 uv;

vec4 FragColor;

void main()
{
    FragColor = vec4(uv*.5+.5,0,1);
}