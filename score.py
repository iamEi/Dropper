import pygame

class Score():
	def __init__(self,surface):
		self.new_hs_font = pygame.font.Font('fonts/Thaleahfat.ttf',30)
		self.score_font = pygame.font.Font('fonts/Thaleahfat.ttf',50)
		self.gameover_font = pygame.font.Font('fonts/Thaleahfat.ttf',100)
		self.screen = surface
		self.colors = {'blue':(111,196,169),'black': (0,0,0), 'red': (255,0,0),'white': (255,255,255)}
		self.index = 0

	def new_highscore(self):
		new_hs = self.draw_text(self.new_hs_font,'New Highscore!',self.colors['white'],250,70)
		self.draw_outline((self.colors['red'],self.colors['black'],self.colors['blue']),new_hs[1],(0,7,3))
		self.screen.blit(*new_hs)

		# offtext = pygame.Surface(new_hs[1].size)
		# surfaces = [new_hs[0],offtext]

		# for _ in range(100):
		# 	self.index += 1
		# 	if self.index > 1: self.index = 0
		# 	self.screen.blit(surfaces[self.index],new_hs[1])

	def update_score(self,score,start_time):
		time = pygame.time.get_ticks()//750 - start_time
		score = self.draw_text(self.score_font,'Score: ',self.colors['white'],250,30,score)
		self.draw_outline((self.colors['red'],self.colors['black'],self.colors['blue']),score[1],(0,15,5))
		self.screen.blit(*score)
		return time

	def display_highscore(self):
		highscore = self.draw_text(self.score_font,'High Score: ',self.colors['white'],250,550,self.get_hs())
		self.draw_outline((self.colors['red'],self.colors['black'],self.colors['blue']),highscore[1],(0,15,5))

		gameover = self.draw_text(self.gameover_font,'GAME OVER',self.colors['white'],250,325)
		self.draw_outline((self.colors['red'],self.colors['black'],self.colors['blue']),gameover[1],(0,15,5))

		self.screen.blit(*highscore)
		self.screen.blit(*gameover)

	def get_hs(self):
		with open('high_score.txt','r') as f:
			saved_hs = f.readline()
			return int(saved_hs)

	def save_highscore(self,score,high_score):
		with open('high_score.txt','r+') as f:
			saved_hs = f.readline()
			if int(saved_hs) <= score >= high_score:
				high_score = score
				f.truncate(0)
				f.seek(0)
				f.write(str(high_score))
			else: 
				high_score = int(saved_hs)
		return high_score

	def draw_text(self,font,text,color,xpos,ypos,vars = ''):
		rendered_text = font.render(text+str(vars),False,color)
		text_rect = rendered_text.get_rect(center = (xpos,ypos))
		return rendered_text,text_rect

	def draw_outline(self,colors,rect,options = (0,0,0)):
		#if options == 0, rectangle is filled
		#if options > 0, the number is used for line thickness
		#if options <0, nothing will be drawn
		pygame.draw.rect(self.screen,colors[0],rect,options[0])
		pygame.draw.rect(self.screen,colors[1],rect,options[1])
		pygame.draw.rect(self.screen,colors[2],rect,options[2])