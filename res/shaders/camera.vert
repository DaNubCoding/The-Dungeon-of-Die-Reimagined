#version 330 core

uniform vec2 u_position, u_targetSize, u_screenSize, u_cameraPos;
uniform float u_cameraRot, u_cameraScale;

in vec3 vertexPos;
in vec2 vertexTexCoord;
out vec2 fragmentTexCoord;

vec2 pixel = vec2(2, -2) / u_screenSize;

float a = radians(u_cameraRot);
mat2 rotationMatrix = mat2(cos(a), sin(a), -sin(a), cos(a));
vec2 offset = u_position - u_cameraPos + u_screenSize / 2 - u_targetSize / 2;

void main()
{
    gl_Position = vec4(rotationMatrix * (vertexPos.xy / pixel + offset) * u_cameraScale * pixel, 0.0, 1.0);
    fragmentTexCoord = vertexTexCoord;
}