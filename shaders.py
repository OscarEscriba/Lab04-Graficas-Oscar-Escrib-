
# voy a crear mis programas aqui pero voy a usar texto despues uso una funcion
# para compilarlos y usarlo
# en layout le digo que empiezo a leer el atributo en la posicion 0 y que es un vector llamado posicion
# vector numero el numero es la cantidad cuanto sale [0,0,0]
# los shaders son dificiles de debuggear porque es imposible poner un breackpoint
# glPosition es donde se guarda la posicion de los vertices
vertex_shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;

out vec2 outTextCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 proyectionMatrix;

void main()
{
  // Asegurarse de que 'outPosition' sea un 'vec4' correctamente
  outPosition = modelMatrix * vec4(position + vec3(0,1,0) * sin(time * position.x * 10) / 10, 1.0);

  // Multiplicación con las matrices de proyección y vista para obtener la posición final
  gl_Position = proyectionMatrix * viewMatrix * outPosition;

  outTextCoords = textCoords;
  outNormals = normals;
}

"""

distortion_shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;
out vec2 outTextCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 proyectionMatrix;
void main()
{
  outPosition = modelMatrix * vec4(position + normals * sin(time) /10, 1.0);
  gl_Position = proyectionMatrix * viewMatrix * outPosition;
  outTextCoords =  textCoords;
  outNormals = normals;
}
"""



water_shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;
out vec2 outTextCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 proyectionMatrix;
void main()
{
  outPosition = modelMatrix * vec4(position + vec3(0,1,0) * sin(time * position.x *10) /10, 1.0);
  gl_Position = proyectionMatrix * viewMatrix * outPosition;
  outTextCoords =  textCoords;
  outNormals = normals;
}
"""
# uniform datos que son todos iguales 
# no hay que enviarle el atributo del vertice . En este caso tiene antes que pasar por el vertice
fragmet_shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;
in vec4 outPosition;

out vec4 fragColor;
uniform sampler2D tex;
uniform vec3 pointLight;
void main()
{
  float intensity = dot(outNormals, normalize(pointLight - outPosition.xyz));
  fragColor = texture(tex, outTextCoords) * intensity;
}
"""

negative_shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;


out vec4 fragColor;
uniform sampler2D tex;
void main()
{
  fragColor = 1 - texture(tex, outTextCoords);
}
"""


fragment_shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;
in vec4 outPosition;

out vec4 fragColor;
uniform sampler2D tex;
uniform vec3 pointLight;
void main()
{
  float intensity = max(dot(outNormals, normalize(pointLight - outPosition.xyz)), 0.0);
  fragColor = texture(tex, outTextCoords) * intensity;
}
"""

#NUEVOS SHADERSSS PARA EL LAB... 
# Grayscale Shader
grayscale_shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;

out vec4 fragColor;
uniform sampler2D tex;

void main()
{
  vec4 color = texture(tex, outTextCoords);
  float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114)); // Escala de grises
  fragColor = vec4(gray, gray, gray, color.a); // Mantener alfa original
}
"""

# Sepia Shader
sepia_shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;

out vec4 fragColor;
uniform sampler2D tex;

void main()
{
  vec4 color = texture(tex, outTextCoords);
  vec3 sepia = vec3(0.393, 0.769, 0.189) * color.r +
               vec3(0.349, 0.686, 0.168) * color.g +
               vec3(0.272, 0.534, 0.131) * color.b;
  fragColor = vec4(sepia, color.a); // Mantener alfa original
}
"""

# Outline Shader
outline_shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;

out vec2 outTextCoords;
out vec3 outNormals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 proyectionMatrix;

void main()
{
  vec3 offset = normalize(normals) * 0.01; // Desplazamiento para el borde
  vec4 displaced = modelMatrix * vec4(position + offset, 1.0);
  gl_Position = proyectionMatrix * viewMatrix * displaced;
  outTextCoords = textCoords;
  outNormals = normals;
}
"""

# Wave Shader
wave_shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;

out vec2 outTextCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 proyectionMatrix;

void main()
{
  vec3 wave = position + vec3(0, sin(time + position.x * 10.0) / 10.0, 0);
  outPosition = modelMatrix * vec4(wave, 1.0);
  gl_Position = proyectionMatrix * viewMatrix * outPosition;
  outTextCoords = textCoords;
  outNormals = normals;
}
"""

#vertex shaders...
animated_shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;

out vec2 outTextCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 proyectionMatrix;

void main()
{
    // Posición animada en el eje Y con base en el tiempo
    vec3 animatedPosition = position + vec3(0, sin(time + position.x * 2.0) * 0.2, 0);
    outPosition = modelMatrix * vec4(animatedPosition, 1.0);
    gl_Position = proyectionMatrix * viewMatrix * outPosition;
    outTextCoords = textCoords;
    outNormals = normals;
}
"""
pulsating_shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;

out vec2 outTextCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 proyectionMatrix;

void main()
{
    // Escalado dinámico basado en el tiempo
    float scale = 1.0 + sin(time) * 0.1;
    vec3 scaledPosition = position * scale;
    outPosition = modelMatrix * vec4(scaledPosition, 1.0);
    gl_Position = proyectionMatrix * viewMatrix * outPosition;
    outTextCoords = textCoords;
    outNormals = normals;
}
"""
circular_movement_shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;

out vec2 outTextCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 proyectionMatrix;

void main()
{
    // Movimiento circular en los ejes X y Z
    vec3 circularPosition = position + vec3(sin(time + position.y) * 0.2, 0, cos(time + position.y) * 0.2);
    outPosition = modelMatrix * vec4(circularPosition, 1.0);
    gl_Position = proyectionMatrix * viewMatrix * outPosition;
    outTextCoords = textCoords;
    outNormals = normals;
}
"""
#fragment shaders...
pulse_color_shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;
in vec4 outPosition;

out vec4 fragColor;

uniform sampler2D tex;
uniform vec3 pointLight;
uniform float time;

void main()
{
    // Intensidad pulsante
    float pulse = abs(sin(time)) * 0.5 + 0.5;
    float intensity = max(dot(outNormals, normalize(pointLight - outPosition.xyz)), 0.0);
    fragColor = texture(tex, outTextCoords) * vec4(intensity * pulse, intensity * pulse, intensity * pulse, 1.0);
}
"""

rainbow_shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;

out vec4 fragColor;

uniform float time;

void main()
{
    // Efecto arcoíris usando senos de tiempo
    float r = abs(sin(time + outTextCoords.x));
    float g = abs(sin(time + outTextCoords.y));
    float b = abs(sin(time + outTextCoords.x + outTextCoords.y));
    fragColor = vec4(r, g, b, 1.0);
}
"""
toon_shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;
in vec4 outPosition;

out vec4 fragColor;

uniform sampler2D tex;
uniform vec3 pointLight;

void main()
{
    // Sombreado estilo "toon"
    float intensity = max(dot(outNormals, normalize(pointLight - outPosition.xyz)), 0.0);
    float levels = 4.0;
    float quantizedIntensity = floor(intensity * levels) / levels;
    fragColor = texture(tex, outTextCoords) * quantizedIntensity;
}
"""

