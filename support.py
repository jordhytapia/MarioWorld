from csv import reader
from settings import*
import pygame
from os import walk



def importCsvLayout(path):
    terrainMap = []
    with open(path) as map:
        level = reader(map,delimiter = ',')
        for row in level:
            terrainMap.append(list(row))
        return terrainMap

def importCutGraphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tileNumx = int(surface.get_size()[0] / verticalTileSize)
    tileNumy = int(surface.get_size()[1] / verticalTileSize)

    cutTiles = []
    for row in range(tileNumy):
        for col in range(tileNumx):
            x = col * verticalTileSize
            y = row * verticalTileSize
            newSurface = pygame.Surface((verticalTileSize,verticalTileSize), flags = pygame.SRCALPHA)
            newSurface.blit(surface,(0,0), pygame.Rect(x,y,verticalTileSize,verticalTileSize))
            cutTiles.append(newSurface)

    return cutTiles

def importFolder(path):
    surfaceList = []

    for information in walk(path):
        for _,__,imageFiles in walk(path):
            for image in imageFiles:
                fullPath = path +'/'+image
                imageSurface = pygame.image.load(fullPath).convert_alpha()
                surfaceList.append(imageSurface)
    return surfaceList



