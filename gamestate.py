import pygame
import sys
from platforms import Platforms

class Gamestate():
	def __init__(self):
		self.state = 'main_game'


	def state_manager(self):
		if self.state == 'main_game':
			self.main_game()
		elif self.state == 'intro':
			self.intro()


	def intro(self):
		pass

	def main_game(self,screen,player,platforms,spawn_timer,bg,bg_rect,spike_group,initplat,initplat_rect,start_time,stat,score,high_score,running,can_move,can_stand,check_collisions,on_platform,game_over):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

			if event.type == spawn_timer:
				platforms.add(Platforms())

			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				bgm.play(-1)
				running = True

		if running:
			# over.stop()
			for platform in platforms.sprites():
				can_stand = on_platform(platform.rect)
				can_move = check_collisions(platform.rect)
				if can_move == False:
					player.sprite.dont_move()
				if can_stand:
					if(platform.rect.left<player.sprite.rect.right) and (player.sprite.rect.left<platform.rect.right):
						player.sprite.move_up(platform.rect)

			screen.blit(bg,bg_rect)

			initplat_rect.y -= 1
			screen.blit(initplat,initplat_rect)
			if player.sprite.rect.colliderect(initplat_rect):
				player.sprite.rect.bottom = initplat_rect.top
			platforms.draw(screen)
			player.draw(screen)

			spike_group.draw(screen)
			score = stat.update_score(score,start_time)

			player.update()
			platforms.update()

			running = game_over()

		else:
			#music
			bgm.fadeout(1000)
			over.play(loops = -1, fade_ms=1900)

			score = 0
			start_time = pygame.time.get_ticks()//750
			stat.display_highscore(high_score)

			#reset player
			player.sprite.reset()
			initplat_rect.center = (250,250)
			platforms.empty()

		pygame.display.flip()
		
