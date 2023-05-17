#version 330 core

uniform vec2 u_vertexOffset;

in vec3 vertexPos;
in vec2 vertexTexCoord;

out vec2 fragmentTexCoord;

void main()
{
    gl_Position = vec4(vertexPos + vec3(u_vertexOffset, 0.0), 1.0);
    fragmentTexCoord = vertexTexCoord;
}