import pygame
import random
import math
import sys
import time
from pygame.locals import *
from time import sleep

screen_y = 600
screen_x = 560
adj = screen_y - screen_x

clock = pygame.time.Clock()

green = (60, 179, 113)
red = (255, 0, 0)
blue = (0, 0, 250)
black = (0, 0, 0)
white = (255, 255, 255)
grey = (205, 205, 193)
yellow = (255, 200, 0)
light_red = (200, 0, 0)
move_val = ((1, 0), (0, 1), (-1, 0), (0, -1))

block_width = 20
grid_w = screen_x // block_width
grid_h = (screen_y - adj) // block_width
fps = 10

diff = ["","easy","normal","hard","insane"]
# display the difficulty
inf = 100000
# for direction 0 - up 1 - down 2 - right 3 - left

def generate_grids():
	game_grid = [[0 for i in range(grid_w)] for j in range(grid_h)]
	for i in range(grid_w):
		for j in range(grid_h):
			if i * j % 5 == 1:
				game_grid[i][j] = 1
			if i * j // 15 == 1 and i % 5 != 0:
				game_grid[i][j] = 2
			if (i * j // 30 == 8 or i * j // 30 == 1) and i % 5 != 0:
				game_grid[i][j] = 2
			if (i * j // 14 == 2 or i * j // 76 == 2) and i % 5 != 0:
				game_grid[i][j] = 1

			if i * j % 25 == 1:
				game_grid[i][j] = 9
	game_grid[grid_w//2][grid_h//2] = 8
	return game_grid

def cal_dis(x1, y1, x2, y2):
	return math.sqrt((x1 - x1) ** 2 + (y1 - y2) ** 2)

def cal_ang(x1, y1, x2, y2):
	if x1 - x2 == 0:
		if y1 - y2 >= 0:
			return 0.5 * math.pi
		else:
			return -0.5 * math.pi
	return math.atan((y1 - y2) / (x1 - x2))

def get_the_tower(lst, x, y):
	for tower in lst:
		if tower.x == x and tower.y == y:
			return tower

def check(xx, yy):
	return xx < grid_h - 1 and xx >= 0 and yy < grid_w - 1 and yy >= 0

def apmin(a, b):
	if a < b:
		return a
	return b

class bombSprite(pygame.sprite.Sprite):
	def __init__(self, x, y, direction, speed, power, ver = 1):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('bomb.png', 'yellow')
		self.rect = self.image.get_rect()
		self.speed = speed
		self.x = x
		self.y = y
		self.rect.center = (x, y)
		self.is_hit = False
		self.power = power
		self.direction = direction
		self.cnt = 0
		self.ver = ver
		self.id = pygame.time.get_ticks()
	def update(self):
		if self.cnt == 10:
			self.is_hit = True
		self.cnt += 1
		self.x -= self.speed * math.cos(self.direction) * self.ver
		self.y -= self.speed * math.sin(self.direction) * self.ver
		self.rect.center = (self.x, self.y)

class Tower(object):
	def __init__(self, x, y, level):
		self.x = x
		self.y = y
		self.level = level
		self.bomb_list = pygame.sprite.Group()
		self.id = pygame.time.get_ticks()
		self.freq_cnt = 0

	def freq_update(self, player):
		if self.freq_cnt >= 20 - self.level:
			self.freq_cnt = 0
		else: 
			self.freq_cnt += player.difficulty

def caldis(sx, sy, game_grid):
	dis = [[0 for i in range(grid_w)] for j in range(grid_h)]
	vis = [[0 for i in range(grid_w)] for j in range(grid_h)]
	found = False
	for x in range(grid_w):
		for y in range(grid_h):
			dis[x][y] = inf

	dis[grid_w//2][grid_h//2] = 0
	queue = [(grid_w//2, grid_h//2)]

	while len(queue) != 0:
		head = queue[0]
		vis.append(head)
		cur_x = head[0]
		cur_y = head[1]
		for moves in move_val:
			xx = cur_x + moves[0]
			yy = cur_y + moves[1]
			if check(xx, yy) and ((xx, yy) not in vis) and game_grid[xx][yy] == 0 and dis[xx][yy] > dis[cur_x][cur_y] + 1:
				queue.append((xx, yy))
				dis[xx][yy] = dis[cur_x][cur_y] + 1
		queue.pop(0)
	return dis

class ballonSprite(pygame.sprite.Sprite):
	Max_health = 500
	Min_health = 200
	Moving_speed = 2

	def __init__(self, x, y, speed):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('ballon.png', 'yellow')
		self.rect = self.image.get_rect()
		self.speed = self.Moving_speed
		self.rect.x = x 
		self.rect.y = y 
		self.gets_in = False	
		self.id = pygame.time.get_ticks()
		self.health = random.randint(300, 1000)
		self.previos_dire = -1

	def get_position(self, game_grid):
		return (self.rect.x, self.rect.y)

	def find_way(self, game_grid):
		# find the way to the palace
		cur_y = (self.rect.y - adj) // block_width
		cur_x = self.rect.x // block_width 
		direction = 0
		dis_lst = caldis(cur_x, cur_y, game_grid)
		ans = -1
		for moves in move_val:
			xx = cur_x + moves[0]
			yy = cur_y + moves[1]
			if check(xx, yy) and (game_grid[xx][yy] == 0 or game_grid[xx][yy] == 8) and dis_lst[xx][yy] < dis_lst[cur_x][cur_y]:
				ans = direction
			direction += 1
		if ans == -1:
			for moves in move_val:
				xx = cur_x + moves[0]
				yy = cur_y + moves[1]
				if check(xx, yy) and(game_grid[xx][yy] == 0 or game_grid[xx][yy] == 8):
					ans = direction
				direction += 1
		return ans

	def update(self, game_grid):
		direction = 0
		if self.rect.x % block_width == 0 and self.rect.y % block_width == 0:
			direction = self.find_way(game_grid)
			self.previos_dire = direction
		direction = self.previos_dire
		if direction == 0:
			self.rect.x += self.speed
		elif direction == 1:
			self.rect.y += self.speed
		elif direction == 2:
			self.rect.x -= self.speed
		elif direction == 3:
			self.rect.y -= self.speed
		cur_y = (self.rect.y - adj) // block_width
		cur_x = self.rect.x // block_width
		if cur_x == grid_w // 2 and cur_y == grid_h // 2:
			self.gets_in = True
		if self.health == 0:
			self.is_dead = True

class Player(object):
	def __init__(self, total_kill, user_level):
		self.total_kill = total_kill
		self.user_level = user_level
		self.difficulty = 1

	def upgrade(self):
		if self.total_kill == self.user_level * 20:
			self.user_level += 1
			self.total_kill = 0
		
def generate_puts(game_grid, list_put):
	for col in range(grid_w):
		for row in [1, grid_h - 2]:
			if game_grid[col][row] == 0:
				list_put.append((row, col))

	for col in [1, grid_w - 2]:
		for row in range(grid_h):
			if game_grid[col][row] == 0:
				list_put.append((row, col))

def generate_bombs(tower_list, ballon_list, bomb_list, player):
	for tower in tower_list:
			cnt = 0
			if tower.freq_cnt == 0:
				trans_x = tower.x * block_width
				trans_y = tower.y * block_width + adj
				for ballon in ballon_list:
					if cnt >= player.difficulty:
						break
					if cal_dis(ballon.rect.x, ballon.rect.y, trans_x, trans_y) <= 50:
						angle = cal_ang(ballon.rect.x, ballon.rect.y, trans_x, trans_y)
						if ballon.rect.x > trans_x:
							bomb_t = bombSprite(trans_x, trans_y, angle, tower.level * 10, tower.level * 200, -1)
						else:
							bomb_t = bombSprite(trans_x, trans_y, angle, tower.level * 10, tower.level * 200)
						bomb_list.add(bomb_t)
						cnt += 1
			tower.freq_update(player)

def generate_ballon(player, list_put, ballon_list):
	limit = apmin(player.user_level ** 3, 1000)
	for i in range(limit):
		index = random.randint(0, len(list_put) - 1)
		cur_x = list_put[index][0] * block_width
		cur_y = list_put[index][1] * block_width + adj
		ballon = ballonSprite(cur_x, cur_y, player.user_level * 0.05)
		ballon_list.add(ballon)

def generate_text_in_game(screen, font, player, store):
	text = font.render('Your balance is: ' + str(store.balance) + ' Your Difficulty: ' + diff[player.difficulty], False, red)
	text_user_level = font.render('Your level is: ' + str(player.user_level) + '  Total kill: ' + str(player.total_kill), False, blue)
	text_rect = text.get_rect()
	text_user_level_rect = text_user_level.get_rect()
	text_rect.center = (screen_x//2, 10)
	text_user_level_rect.center = (screen_x//2, 30)
	screen.blit(text, text_rect)
	screen.blit(text_user_level, text_user_level_rect)

def deal_with_click_left(tower_list, store, game_grid, tower_limit):
	cur_x = (pygame.mouse.get_pos()[1]  - adj)// block_width
	cur_y = pygame.mouse.get_pos()[0] // block_width
	if store.balance > 0 and len(tower_list) <= tower_limit:
		if game_grid[cur_x][cur_y]  == 1:
			game_grid[cur_x][cur_y] = 3
			tower_list.append(Tower(cur_y, cur_x, 1))
			store.transaction(-100)
		elif game_grid[cur_x][cur_y] <= 6 and game_grid[cur_x][cur_y] >= 3:
			game_grid[cur_x][cur_y] += 1
			tower = get_the_tower(tower_list, cur_y, cur_x)
			tower.level += 1
			store.transaction((-100) * tower.level)

def deal_with_click_right(tower_list, game_grid, store, player):
	cur_x = (pygame.mouse.get_pos()[1]  - adj)// block_width
	cur_y = (pygame.mouse.get_pos()[0]) // block_width
	if store.balance >= 0:
		if game_grid[cur_x][cur_y]  >= 3 and game_grid[cur_x][cur_y] <= 7:
			if player.difficulty == 4 or player.difficulty == 3:
				game_grid[cur_x][cur_y] = 9
			else:
				game_grid[cur_x][cur_y] = 1
			tower = get_the_tower(tower_list, cur_y, cur_x)
			store.transaction(50 * tower.level)
			tower_list.remove(tower)

def display_help(screen):
	help = pygame.image.load("help.png")
	screen.blit(help, (0, 0))
	pygame.display.flip()
	time.sleep(5)

def checkForKeyPress(player = None, screen = None):
	if len(pygame.event.get(QUIT)) > 0:
		pygame.quit()
		sys.exit()

	keyUpEvents = pygame.event.get(KEYUP)
	if len(keyUpEvents) == 0:
		return None

	key_pressed = keyUpEvents[0].key
	if player != None:
		if key_pressed == K_1:			#easy level
			player.difficulty = 1
		elif key_pressed == K_2:		#normal level
			player.difficulty = 2
		elif key_pressed == K_3:
			player.difficulty = 3		#hard level
		elif key_pressed == K_4:
			player.difficulty = 4		#insane level
		elif key_pressed == K_h:
			display_help(screen)
		elif key_pressed == K_ESCAPE:
			pygame.quit()
			sys.exit()
	elif key_pressed == K_ESCAPE:
		pygame.quit()
		sys.exit()

	return key_pressed

def showOver(screen):
	cnt = 5
	font = pygame.font.Font('C:\Windows\Fonts\Arial.ttf', 30)
	text = font.render('Your fort is taken by the enemy!', False, black)
	text_rect = text.get_rect()
	text_rect.center = (screen_x // 2, screen_y // 2)
	screen.blit(text, text_rect)
	pygame.display.flip()	
	clock.tick(1)
	while cnt > 0:
		screen.fill(white)
		text = font.render('Press any key to continue or exit after ' + str(cnt), False, black)
		text_rect = text.get_rect()
		text_rect.center = (screen_x // 2, screen_y // 2 + 50)
		screen.blit(text, text_rect)
		cnt -= 1
		clock.tick(1)
		if checkForKeyPress():
		    pygame.event.get() 
		    #print(checkForKeyPress())
		    return 
		pygame.display.flip()
	pygame.quit()
	sys.exit()

def showStartScreen(screen, player):
	titleFont = pygame.font.Font('C:\Windows\Fonts\Arial.ttf', 90)
	level_font = pygame.font.Font('C:\Windows\Fonts\Arial.ttf', 30)
	explain_font = pygame.font.Font('C:\Windows\Fonts\Arial.ttf', 15)
    # mark = pygame.image.load("mole.png")

	titleSurf1 = titleFont.render('Fort Defence!', True, black, blue)
	levelSurf1 = level_font.render('An easy game - press 1', True, green)
	explainSurf1 = explain_font.render('-> Infinite tower construction', True, green)
	levelSurf2 = level_font.render('A normal game - press 2', True, yellow)
	explainSurf2 = explain_font.render('-> Limited but sufficient tower construction', True, yellow)
	levelSurf3 = level_font.render('A difficult game - press 3', True, blue)
	explainSurf3 = explain_font.render('-> Challening limits, faster pace', True, blue)
	levelSurf4 = level_font.render('An insane game - press 4', True, red)
	explainSurf4 = explain_font.render(' -> Get crazy! Get insane!', True, red)

	helpSurf = explain_font.render('Need Help? - press h', True, light_red) 

	while True:
		screen.fill(white)
		screen.blit(titleSurf1, [0, 100, 560, 200])
		rects = []
		for i in range(4):
			rects.append([150, 300 + 70 * i, 560, 50])
			rects.append([150, 350 + 70 * i, 560, 20])
		rects.append([10, 220, 200, 20])
		rects.append([10, 250, 200, 20])
		screen.blit(levelSurf1, rects[0])
		screen.blit(explainSurf1, rects[1])
		screen.blit(levelSurf2, rects[2])
		screen.blit(explainSurf2, rects[3])
		screen.blit(levelSurf3, rects[4])
		screen.blit(explainSurf3, rects[5])
		screen.blit(levelSurf4, rects[6])
		screen.blit(explainSurf4, rects[7])
		screen.blit(helpSurf, rects[8])
		result = checkForKeyPress(player, screen)
		if result != K_h and result:
			pygame.event.get() 
			return 

		pygame.display.flip()

def generate_map(game_grid, screen):
	for row in range(grid_h):
		for col in range(grid_w):
			if(game_grid[row][col] == 0):
				color = yellow
			elif(game_grid[row][col] == 1):
				color = green
			elif(game_grid[row][col] == 2):
				color = blue
			elif(game_grid[row][col] == 3):
				fort1 = pygame.image.load("level1.png")
				screen.blit(fort1, (col * block_width, adj + row* block_width))
				continue
			elif(game_grid[row][col] == 4):
				fort2 = pygame.image.load("level2.png")
				screen.blit(fort2, (col * block_width, adj + row* block_width))
				continue
			elif(game_grid[row][col] == 5):
				fort3 = pygame.image.load("level3.png")
				screen.blit(fort3, (col * block_width, adj + row* block_width))
				continue
			elif(game_grid[row][col] == 6):
				fort4 = pygame.image.load("level4.png")
				screen.blit(fort4, (col * block_width, adj + row* block_width))
				continue
			elif(game_grid[row][col] == 7):
				fort5 = pygame.image.load("level5.png")
				screen.blit(fort5, (col * block_width, adj + row* block_width))
				continue
			elif(game_grid[row][col] == 9):
				color = black
			elif(game_grid[row][col] == 8):
				fort = pygame.image.load("fort.png")
				screen.blit(fort, (col * block_width, adj + row* block_width))
				continue
			else:
				color = blue
			pygame.draw.rect(screen, color, (col * block_width, adj + row* block_width, block_width, block_width))

class shop(object):
	def __init__(self, balance):
		self.balance = balance

	def transaction(self, amount):
		if self.balance + amount < 0:
			print("Insufficient Funds!")
		else:
			self.balance += amount

def run():
	pygame.init()
	game_grid = generate_grids()
	screen = pygame.display.set_mode((screen_x, screen_y))
	store = shop(500)
	pygame.display.set_caption('Fort defence')
	player = Player(0, 1)
	ballon_list = []
	tower_list = []
	bomb_list = []
	list_put = []		# the available grids to generate balloons
	is_over = False
	font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 20)
	clock = pygame.time.Clock()
	ballon_list = pygame.sprite.Group() 
	bomb_list = pygame.sprite.Group()  
	time_wait = 0
	tower_limit = inf

	generate_puts(game_grid, list_put)
	showStartScreen(screen, player)

	if player.difficulty != 1:
		tower_limit = int(1000 * math.exp(-player.difficulty))
	while True:
		player.upgrade()
		time_wait += 1
		if time_wait == int((200 - player.user_level ** 2) * math.exp(-player.difficulty)):
			time_wait = 0
			generate_ballon(player, list_put, ballon_list)

		screen.fill(white)

		generate_map(game_grid, screen)
		generate_bombs(tower_list, ballon_list, bomb_list, player)
		for bomb in bomb_list:			
			if bomb.is_hit:
				bomb_list.remove(bomb)

		for bomb in bomb_list:
			for ballon in ballon_list:
				if bomb.rect.colliderect(ballon.rect):
					ballon.health -=  (bomb.power // player.difficulty)
					bomb.is_hit = True
			if not check(bomb.rect.x // block_width, (bomb.rect.y - adj) // block_width):
				bomb.is_hit = True
		
		bomb_list.draw(screen)
		bomb_list.update()
		ballon_list.draw(screen)
		ballon_list.update(game_grid)		
		
		generate_text_in_game(screen, font, player, store)

		for ballon in ballon_list:
			if ballon.gets_in == True:
				is_over = True
				break
			elif ballon.health <= 0:
				ballon_list.remove(ballon)
				store.transaction(25 * player.user_level // player.difficulty)
				player.total_kill += 1
		
		if is_over == True:
			showOver(screen)
			break
	
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYUP and event.key == K_ESCAPE:
				pygame.event.post(pygame.event.Event(QUIT))
			elif pygame.mouse.get_pressed()[0]:
				deal_with_click_left(tower_list, store, game_grid, tower_limit)
			elif pygame.mouse.get_pressed()[2]:
				deal_with_click_right(tower_list, game_grid, store, player)
		pygame.display.flip()
		clock.tick(fps)

def main():
	while True:
		run()

if __name__ == "__main__":
	main()


		