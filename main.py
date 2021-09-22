import pygame
import sys
from player import Player
from platforms import Platforms
from score import Score
from spikes import Spikes
from gamestate import Gamestate
from intro import Intro

#initializing pygame
pygame.init()

#set up
WIDTH = 500
HEIGHT = 700
title = 'Dropper'
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(title)
clock = pygame.time.Clock()


#LOADING ASSETS

#for background
bg = pygame.image.load('images/bg.jpg')
bg = pygame.transform.scale(bg,(500,700))
bg_rect = bg.get_rect(topleft = (0,0))

#for initial platform for player to stand at the start
initplat = pygame.image.load('images/platform_2.png')
initplat = pygame.transform.scale(initplat, (200, 35))
initplat_rect = initplat.get_rect(center = (WIDTH/2,250))

#game over and background music
over = pygame.mixer.Sound('sounds/game_over.mp3')
bgm = pygame.mixer.Sound('sounds/Melody.mp3')
bgm.play(loops = -1,fade_ms=2000)

#setting frequency of platform spawn
spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_timer,500)

#initial values
start_time = 0
score = 0
high_score = 0
intro = True
running = False

#creating objects
stat = Score(screen)
start = Intro(screen,bg,bg_rect)

#creating sprites
player = pygame.sprite.GroupSingle()
player.add(Player())
Player = player.sprite
platforms = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
for i in [-10,120,250,380]:
	spike_group.add(Spikes(i,-15))


#controlling the flow of the game states
def state():
	global running, intro,score
	if intro:
		intro = start.draw_intro()
		#pressing SPACE would make intro = FALSE, running the game.
		if not intro:
			reset_score()
			running = True

	elif running:
		over.stop()
		for platform in platforms.sprites():
			Platform = platform.rect
			if path_blocked(Platform):
				Player.block_movement()
			if on_platform(Platform):
				Player.rect.bottom = Platform.top

		#draw background
		screen.blit(bg,bg_rect)
			
		#initial platform
		initplat_rect.y -= 1
		screen.blit(initplat,initplat_rect)
		if player.sprite.rect.colliderect(initplat_rect):
			player.sprite.rect.bottom = initplat_rect.top

		#draw platforms
		platforms.draw(screen)
		player.draw(screen)

		#spikes at the top
		spike_group.draw(screen)

		score = stat.update_score(score,start_time)
		if score > stat.get_hs():		
			stat.new_highscore()

		player.update()
		platforms.update()

		#check if game is over
		running = game_over()

	#if gameover
	elif not running:
		#music
		bgm.fadeout(1000)
		over.play(loops = -1, fade_ms=1900)

		#reset numbers
		reset_score()
		stat.display_highscore(high_score)

		#reset player position
		Player.reset()
		initplat_rect.center = (250,250)

		#clear all platforms
		platforms.empty()

def reset_score():
	global score, start_time
	score = 0
	start_time = pygame.time.get_ticks()//750


#checking if player goes out of bounds
def game_over():
	global high_score
	if HEIGHT < player.sprite.rect.top or pygame.sprite.spritecollide(player.sprite,spike_group,False):
		high_score = stat.save_highscore(score,high_score)
		return False
	return True

#checking if player is colliding with platform, if yes, dont let the player move further
def path_blocked(pf):
	if player.sprite.rect.colliderect(pf) and not on_platform(pf):
		if abs(pf.left - player.sprite.rect.right) < 10:
			return True
		if abs(pf.right - player.sprite.rect.left) < 10:
			return True
	return False

#checking if player is standing on platform, if yes, do not apply gravity
def on_platform(platform):
	if Player.rect.colliderect(platform):
		if abs(platform.top - Player.rect.bottom) < 20 and ((platform.left < Player.rect.right) and (Player.rect.left < platform.right)):
			return True
	return False

#gameloop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if event.type == spawn_timer:
			if running:
				platforms.add(Platforms())

		if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
			bgm.play(loops = -1)
			running = True

	state()
	pygame.display.flip()
	clock.tick(60)