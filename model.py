from obj import Obj
from Buffer import Buffer
from pygame import image
from OpenGL.GL import *
import glm
import pygame  # Asegúrate de tener esta línea al inicio del archivo


class Model(object):
  def __init__(self, filename):
    objFile = Obj(filename=filename)

    self.vertices = objFile.vertices
    self.texCoords = objFile.texcoords
    self.normals = objFile.normals
    self.faces = objFile.faces
    self.buffer = Buffer(self.BuildBuffer())       
    self.translation = glm.vec3(0,0,0)
    self.rotation = glm.vec3(0,0,0)
    self.scale = glm.vec3(1,1,1)
    self.texture = None  
    self.textureData = None  

  def BuildBuffer(self):
    data = []
    for face in self.faces:
        faceVerts = []
        for i in range(len(face)):
            vert = []
            position = self.vertices[face[i][0] - 1]
            vert.extend(position)

            # Invertir la coordenada y de la textura
            vts = self.texCoords[face[i][1] - 1]
            vert.extend([vts[0], 1 - vts[1]])  # Ajuste en la coordenada y

            normals = self.normals[face[i][2] - 1]
            vert.extend(normals)

            faceVerts.append(vert)

        for value in faceVerts[0]: data.append(value)
        for value in faceVerts[1]: data.append(value)
        for value in faceVerts[2]: data.append(value)

        if len(faceVerts) == 4:
            for value in faceVerts[0]: data.append(value)
            for value in faceVerts[2]: data.append(value)
            for value in faceVerts[3]: data.append(value)
    return data


  def AddTexture(self, textureFilename):
    self.textureSurface = image.load(textureFilename)
    self.textureSurface = pygame.transform.flip(self.textureSurface, False, True)  # Invertir verticalmente
    self.textureData = image.tostring(self.textureSurface, "RGB", True)
    self.texture = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, self.texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGB,
        self.textureSurface.get_width(),
        self.textureSurface.get_height(),
        0, GL_RGB, GL_UNSIGNED_BYTE,
        self.textureData
    )
    glGenerateMipmap(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)  # Desenlazar la textura



  def GetModelMatrix(self):
    identity = glm.mat4(1)
    translateMat = glm.translate(identity, self.translation)
    
    pitchMat = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))
    yawMat   = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
    rollMat  = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))
    
    rotationMat = pitchMat * yawMat * rollMat
    scaleMat = glm.scale(identity, self.scale)
    
    return translateMat * rotationMat * scaleMat

  def Render(self):
    if self.texture is not None:
      glActiveTexture(GL_TEXTURE0)
      glBindTexture(GL_TEXTURE_2D, self.texture)

    self.buffer.Render()

    # Desenlazar la textura para evitar problemas en futuros renders
    if self.texture is not None:
      glBindTexture(GL_TEXTURE_2D, 0)