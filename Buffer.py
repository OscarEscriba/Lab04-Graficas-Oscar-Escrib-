import glm
from numpy import array, float32
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

class Buffer(object):
  def __init__(self, data):

    self.vertBuffer = array(data, float32)

    # Vertex Buffer Object
    #aqui es donde mando la informacion a la tarjeta de video
    self.VBO = glGenBuffers(1)

    #tenemos que mandarle la informacion de atributos como color normales, texcords
    self.VAO = glGenVertexArrays(1)
  
  def Render(self):
    # cada vez que llame render
    # voy a atar un bufffer a la tarjeta de video
    glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
    glBindVertexArray(self.VAO)

    # uso static draw es para dibujar de manera estatica
    glBufferData(GL_ARRAY_BUFFER,
                 self.vertBuffer.nbytes,
                 self.vertBuffer,
                 GL_STATIC_DRAW)
    # atributos especificar que representa y como usarla

    #atributo de posiciones
    glVertexAttribPointer(0,
                          3,
                          GL_FLOAT,
                          GL_FALSE,
                          4 * 8,
                          ctypes.c_void_p(0))

    #este paso es que atributo quiero activar
    glEnableVertexAttribArray(0)

    # Atributo de textCoords
    # el offset va a ser diferente
    glVertexAttribPointer(1,
                          2,
                          GL_FLOAT,
                          GL_FALSE,
                          4 * 8,
                          ctypes.c_void_p(4*3))

    #este paso es que atributo quiero activar
    glEnableVertexAttribArray(1)

    # Atributo de Noormales
    # el offset va a ser diferente
    glVertexAttribPointer(2,
                          3,
                          GL_FLOAT,
                          GL_FALSE,
                          4 * 8,
                          ctypes.c_void_p(4*5))

    #este paso es que atributo quiero activar
    glEnableVertexAttribArray(2)


    glDrawArrays(GL_TRIANGLES, 0,int(len(self.vertBuffer)/8))