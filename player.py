import pygame as pg

class Player(pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		
		self.stand = self.transform('images/front-stand.png')

		l1 = self.transform('images/left-stand.png')
		l2 = self.transform('images/left-stand2.png')
		l3 = self.transform('images/left-walk.png')
		l4 = self.transform('images/left-walk2.png')
		self.left = [l1,l3,l1,l4]

		r1 = self.transform('images/right-stand.png')
		r2 = self.transform('images/right-stand2.png')
		r3 = self.transform('images/right-walk.png')	
		r4 = self.transform('images/right-walk2.png')
		self.right = [r1,r3,r1,r4]

		self.image = self.stand
		self.rect = self.image.get_rect(midtop = (250,240))

		self.player_index = 0
		self.gravity = 6
		self.speed = 7
		self.moving = False
		self.direction = ''

	def transform(self,image):
		scaled = pg.image.load(image)
		return pg.transform.scale(scaled,(48,48))

	def apply_gravity(self):
		self.rect.y += self.gravity

	def block_movement(self):
		if self.direction == 'right':
			self.rect.x -= 5
		elif self.direction == 'left':
			self.rect.x += 5

	def move(self,direction = 0,vex = 0):
		if self.moving:
			self.rect.x += self.speed * vex
			self.player_index += 0.1
			if self.player_index > 4: self.player_index = 0
			self.image = direction[int(self.player_index)]
		else:
			self.image = self.stand

	def animate(self):
		keys = pg.key.get_pressed()
		if any(keys):
			if (keys[pg.K_LEFT] or keys[pg.K_a]):
				self.direction = 'left'
				if self.rect.left < -10:
					self.rect.x = 510
				self.moving = True
				self.move(self.left,-1)
			elif (keys[pg.K_RIGHT] or keys[pg.K_d]):
				self.direction = 'right'
				if self.rect.right > 510:
					self.rect.x = -10
				self.moving = True
				self.move(self.right,1)
		else:
			self.moving = False
			self.move()

	def reset(self):
		self.rect.midtop = (250,90)

	def update(self):
		self.apply_gravity()
		self.animate()