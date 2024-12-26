#version 330

in vec2 fTexCoords;

uniform sampler2D TEX_ATLAS;

out vec4 color;

void main() {
    color = texture(TEX_ATLAS, fTexCoords);
}