import pygame
from random import randint

class Platforms(pygame.sprite.Sprite):
	def __init__(self,speed):
		super().__init__()
		self.speed = speed
		img = pygame.image.load('images/platform_2.png')
		self.image = pygame.transform.scale(img, (randint(150,200), 35))
		self.rect = self.image.get_rect(center = (randint(0,500),randint(705,720)))


	def move(self):
		self.rect.y -= self.speed

	def destroy(self):
		if self.rect.y < -50:
			self.kill()
		

	def update(self):
		self.move()
		self.destroy()