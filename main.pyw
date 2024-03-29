import pygame, sys
from player import Player
from platforms import Platforms
from spikes import Spikes
from text import Text

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
initplat_rect = initplat.get_rect(midbottom = (WIDTH/2,300))

#game over and background music
over = pygame.mixer.Sound('sounds/game_over.mp3')
bgm = pygame.mixer.Sound('sounds/Melody.mp3')
bgm.play(loops = -1,fade_ms=2000)

#initial values
start_time = 0
score = 0
intro = True
running = False
speed = 2

#setting frequency of platform spawn
spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_timer,800)

speedup_timer = pygame.USEREVENT + 2
pygame.time.set_timer(speedup_timer,2000)

#creating text display object
text = Text(screen,bg,bg_rect)

#creating sprites
player = pygame.sprite.GroupSingle()
player.add(Player())
Player = player.sprite
platforms = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
for i in [-10,120,250,380]:
	spike_group.add(Spikes(i,-15))

def speedup():
	global speed
	speed += 0.1
	for i in platforms.sprites():
		i.speed = speed

def reset_score():
	global score, start_time
	score = 0
	start_time = pygame.time.get_ticks()//750


#checking if player goes out of bounds
def game_over():
	if HEIGHT < Player.rect.top or pygame.sprite.spritecollide(Player,spike_group,False):
		text.save_highscore(score,text.get_hs())
		return False
	return True

#checking if player is colliding with platform, if yes, dont let the player move further
def path_blocked(platform):
	if Player.rect.colliderect(platform) and not on_platform(platform):
		if abs(platform.left - Player.rect.right) < 10:
			return True
		if abs(platform.right - Player.rect.left) < 10:
			return True
	return False

#checking if player is standing on platform, if yes, do not apply gravity
def on_platform(platform):
	if Player.rect.colliderect(platform):
		if abs(platform.top - Player.rect.bottom) < 20 and ((platform.left < Player.rect.right) and (Player.rect.left < platform.right)):
			return True
	return False

#controlling the flow of the game states
def gamestate():
	global running, intro,score, speed
	if intro:
		text.display_intro()
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
		if Player.rect.colliderect(initplat_rect):
			Player.rect.bottom = initplat_rect.top

		#draw platforms
		platforms.draw(screen)
		player.draw(screen)

		#spikes at the top
		spike_group.draw(screen)

		score = text.display_score(score,start_time)
		if score > text.get_hs():		
			text.new_highscore()

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
		text.display_highscore()
		speed = 2

		#reset player position
		Player.reset()
		initplat_rect.center = (250,250)

		#clear all platforms
		platforms.empty()

#gameloop
while True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
			
		if running:
			if event.type == spawn_timer:
				platforms.add(Platforms(speed))
				if int(speed) == 3:
					pygame.time.set_timer(spawn_timer,600)
				if int(speed) == 4:
					pygame.time.set_timer(spawn_timer,500)

			if event.type == speedup_timer:
				if speed < 5:
					speedup()
				else:
					pygame.time.set_timer(speedup_timer,0)

		if not running:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				# bgm.play(loops = -1)
				pygame.time.set_timer(spawn_timer,700)
				intro = False
				running = True

	gamestate()
	pygame.display.flip()
	clock.tick(60)