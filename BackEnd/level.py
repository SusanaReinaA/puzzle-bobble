import pygame

class Level:
    def __init__(self,number,image_path):
        self.number=number
        self.image=pygame.image.load(image_path)

    def draw(self,surface):
        surface.blit(self.image,(0,0))
