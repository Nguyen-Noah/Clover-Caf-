#version 330

layout (location=0) in vec2 aPos;
layout (location=1) in vec2 aTexCoords;
layout (location=2) in vec2 aOffset;

uniform mat4 uProjection;
uniform mat4 uView;

out vec2 fTexCoords;

void main() {
    fTexCoords = aTexCoords;
    vec2 pos = aPos + aOffset;
    gl_Position = uProjection * uView * vec4(pos, 0.0, 1.0);
}