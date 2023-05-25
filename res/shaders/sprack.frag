#version 330 core

uniform sampler2D u_imageTexture;
uniform vec2 u_texSize;
uniform vec2[200] u_obstructing;
uniform int u_obstructingLen;

in vec2 fragmentTexCoord;

out vec4 color;

vec2 pixel = vec2(1.0, 1.0) / u_texSize;

void main() {
    bool transparent = false;
    for (int i = 0; i < u_obstructingLen; i++) {
        vec2 coord = vec2(fragmentTexCoord.x, 1 - fragmentTexCoord.y) / pixel - vec2(64, 64);
        if (coord.x < u_obstructing[i].x && u_obstructing[i].x < coord.x + 64 && coord.y < u_obstructing[i].y && u_obstructing[i].y < coord.y + 64) {
            transparent = true;
            break;
        }
    }
    color = texture2D(u_imageTexture, fragmentTexCoord);
    if (transparent) {
        color.a *= 0.25;
    }
}