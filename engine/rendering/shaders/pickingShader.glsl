#version 330

in vec4 fColor;
in vec2 fTexCoords;
in float fTexId;
in float fEntityId;

uniform sampler2DArray uTextures;

out vec3 color;

void main() {
    vec4 texColor = vec4(1, 1, 1, 1);
    if (fTexId != 0) {
        texColor = fColor * texture(uTextures, vec3(fTexCoords, fTexId - 1.0));    // fTexId - 1.0 because the 0th element will be held for blank
    }

    if (texColor.a < 0.5) {
        discard;
    }
    color = vec3(fEntityId, fEntityId, fEntityId);
}