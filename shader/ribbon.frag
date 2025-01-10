precision mediump float;

varying vec2 uv;

vec4 FragColor;

void main()
{
    float shade = uv.y;
    shade = step(.5, fract(uv.x*2.));
    FragColor = vec4(vec3(shade),1);
}