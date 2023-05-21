#version 330 core

uniform vec2 u_position;
uniform vec2 u_screenSize;

in vec3 vertexPos;
in vec2 vertexTexCoord;

out vec2 fragmentTexCoord;

vec2 pixel = vec2(2, -2) / u_screenSize;

void main()
{
    gl_Position = vec4((vertexPos.xy / pixel + u_position) * pixel, 0.0, 1.0);
    fragmentTexCoord = vertexTexCoord;
}