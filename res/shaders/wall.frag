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
    float alpha_factor = 1.0;
    float angle = 0.0;
    if (color.a < 1.0 / 10) {
        angle = angle_diff(u_playerRot, PI / 2);
        alpha_factor = sqrt(angle / PI) * 1.7;
    } else if (color.a < 2.0 / 10) {
        angle = angle_diff(u_playerRot, PI);
        alpha_factor = sqrt(angle / PI) * 1.7;
    } else if (color.a < 3.0 / 10) {
        angle = angle_diff(u_playerRot, PI * 3 / 2);
        alpha_factor = sqrt(angle / PI) * 1.7;
    } else if (color.a < 4.0 / 10) {
        angle = angle_diff(u_playerRot, 0.0);
        alpha_factor = sqrt(angle / PI) * 1.7;
    } else if (color.a < 5.0 / 10) {
        alpha_factor = 1.5;
    }
    if (color.a != 0.0) {
        color.a = 1.0;
    }
    color.a *= pow(dist / 180, 2) + 0.16;
    color.a *= alpha_factor;
}