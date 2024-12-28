#version 330

in vec4 fColor;
in vec2 fTexCoords;
in float fTexId;

uniform sampler2DArray uTextures;

out vec4 color;

void main() {
    if (fTexId != 0) {
        color = fColor * texture(uTextures, vec3(fTexCoords, fTexId - 1.0));    // fTexId - 1.0 because the 0th element will be held for blank
    } else {
        color = fColor - vec4(fTexId);
    }

    if (color.a < 0.1) {
        discard;
    }
}