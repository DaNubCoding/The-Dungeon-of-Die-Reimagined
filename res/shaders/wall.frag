#version 330 core

uniform sampler2D u_imageTexture;
uniform vec2 u_texSize;
uniform vec2 u_playerPos;
uniform float u_playerRot;

in vec2 fragmentTexCoord;

out vec4 color;

const float PI = 3.14159265358;
vec2 pixel = 1.0 / u_texSize;

float angle_diff(float a1, float a2) {
    return abs(atan(sin(a1 - a2) / cos(a1 - a2)));
}

void main() {
    color = texture2D(u_imageTexture, fragmentTexCoord);
    float dist = distance(u_playerPos, vec2(fragmentTexCoord.x, 1 - fragmentTexCoord.y) / pixel);
    int i = int(color.a * 10);
    if (color.a != 0.0) {
        color.a = 1.0;
    }
    color.a *= pow(dist / 180, 2) + 0.16;
    if (i == 5) {
        color.a *= 1.7;
    } else {
        color.a *= sqrt(angle_diff(u_playerRot, (i + 1) * PI / 2) / PI * 1.7);
    }
}