import pygame
from score import Score

class Intro():
	def __init__(self, screen, background_surf,background_rect):
		self.screen = screen
		self.background_surface = background_surf
		self.background_rect = background_rect
		self.sub_font = pygame.font.Font('fonts/Thaleahfat.ttf',50)
		self.title_font = pygame.font.Font('fonts/Thaleahfat.ttf',100)
		self.colors = {'blue':(111,196,169),'black': (0,0,0), 'red': (255,0,0),'white': (255,255,255)}

	def draw_intro(self):
		score = Score(self.screen)
		self.screen.blit(self.background_surface, self.background_rect)

		highscore = self.draw_text(self.sub_font,'High Score: ',self.colors['white'],250,100,score.get_hs())
		self.draw_outline((self.colors['red'],self.colors['black'],self.colors['blue']),highscore[1],(0,15,5))
		self.screen.blit(*highscore)

		title = self.draw_text(self.title_font,'Drop!',self.colors['white'],250,350)
		self.draw_outline((self.colors['red'],self.colors['black'],self.colors['blue']),title[1],(0,15,5))
		self.screen.blit(*title)

		start = self.draw_text(self.sub_font,'Press SPACE to start',self.colors['white'],250,550)
		self.draw_outline((self.colors['red'],self.colors['black'],self.colors['blue']),start[1],(0,15,5))
		self.screen.blit(*start)

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