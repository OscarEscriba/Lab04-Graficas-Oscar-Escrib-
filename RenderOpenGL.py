import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from gl import Renderer
from model import Model
import numpy as np
from shaders import water_shader, vertex_shader, fragment_shader  # Asegúrate de importar tus shaders
from OpenGL.GL.shaders import compileShader, compileProgram

# Configuración de pantalla
width, height = 720, 720
pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

# Inicialización de OpenGL
glClearColor(0.2, 0.2, 0.2, 1.0)
glEnable(GL_DEPTH_TEST)  # Habilitar Z-buffer
glEnable(GL_TEXTURE_2D)  # Habilitar texturas

# Función para cargar y compilar los shaders
def load_shader(water_shader, fragment_code):
    water_shader = compileShader(water_shader, GL_VERTEX_SHADER)
    fragment_shader = compileShader(fragment_code, GL_FRAGMENT_SHADER)
    shader_program = compileProgram(vertex_shader, fragment_shader)
    return shader_program

# Cargar el shader y asignarlo
shader_program = load_shader(water_shader, fragment_shader)  # Usando el water_shader

# Configuración del modelo
faceModel = Model("Model.obj")
faceModel.AddTexture("Textures/model.bmp")  # Asumiendo que tienes una textura

# Variables de la cámara y la luz
view_matrix = np.identity(4)  # Puedes usar una matriz de vista calculada
projection_matrix = np.identity(4)  # Matriz de proyección (perspectiva)
model_matrix = np.identity(4)  # Matriz del modelo (puedes modificarla si es necesario)
point_light = np.array([1.0, 1.0, 1.0])  # Dirección de la luz

# Configura los uniformes
def set_uniforms(shader_program, model_matrix, view_matrix, projection_matrix, time, point_light):
    glUseProgram(shader_program)
    glUniformMatrix4fv(glGetUniformLocation(shader_program, "modelMatrix"), 1, GL_TRUE, model_matrix)
    glUniformMatrix4fv(glGetUniformLocation(shader_program, "viewMatrix"), 1, GL_TRUE, view_matrix)
    glUniformMatrix4fv(glGetUniformLocation(shader_program, "proyectionMatrix"), 1, GL_TRUE, projection_matrix)
    glUniform1f(glGetUniformLocation(shader_program, "time"), time)
    glUniform3fv(glGetUniformLocation(shader_program, "pointLight"), 1, point_light)

# Loop principal
isRunning = True
start_time = pygame.time.get_ticks() / 1000  # Empezar el contador de tiempo

while isRunning:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Calcular el tiempo transcurrido
    elapsed_time = (pygame.time.get_ticks() / 1000) - start_time
    
    # Configura los uniformes para el shader
    set_uniforms(shader_program, model_matrix, view_matrix, projection_matrix, elapsed_time, point_light)
    
    # Renderiza el modelo
    faceModel.Render()

    pygame.display.flip()
    clock.tick(60)  # Limitar a 60 FPS

pygame.quit()
