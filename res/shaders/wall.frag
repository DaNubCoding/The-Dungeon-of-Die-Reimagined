#version 330 core

uniform sampler2D u_imageTexture;
uniform vec2 u_texSize;
uniform vec2 u_playerPos;

in vec2 fragmentTexCoord;

out vec4 color;

vec2 pixel = 1.0 / u_texSize;

void main() {
    color = texture2D(u_imageTexture, fragmentTexCoord);
    float dist = distance(u_playerPos, vec2(fragmentTexCoord.x, 1 - fragmentTexCoord.y) / pixel);
    if (dist < 200) {
        color.a *= pow(dist / 200, 2);
    }
}