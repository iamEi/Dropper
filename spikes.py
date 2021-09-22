import pygame

class Spikes(pygame.sprite.Sprite):
	def __init__(self,xpos,ypos):
		super().__init__()
		self.image = pygame.image.load('images/SpikeSteel.png')
		self.rect = self.image.get_rect(topleft = (xpos,ypos))
