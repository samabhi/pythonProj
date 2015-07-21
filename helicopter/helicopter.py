import pygame
import time
from random import randint

black = ( 0 , 0 , 0 )
white = (255,255,255)
red   = (225, 0 , 0 )

def score(count):
	font = pygame.font.Font('freesansbold.ttf', 20)
	text = font.render('Score: ' + str(count), True, black)
	surface.blit(text, [0, 0])

def upper_block_collision(x, x_pos, y, y_pos, b_height, b_width, gap):
	if x + img_width > x_pos:
		if x < x_pos + b_width:
			#print('possibly within boundaries of x')
			if y < b_height:
				#print('y crossover UPPER')
				if x - img_width < b_width + x_pos:
					return True

def lower_block_collision(x, x_pos, y, y_pos, b_height, b_width, gap):
	if x + img_width > x_pos:
		#print('x crossover')
		if y + img_height > b_height + gap:
		#print('y crossover')
			if x < b_width + x_pos:
			#print('game over lower')
				return True

def boundary_collision(y):
	if y > surfaceHeight - 75 or y < 0:
		return True

def blocks(x_pos, y_pos, b_width, b_height, gap):
	pygame.draw.rect(surface, black, [x_pos, y_pos, b_width, b_height])
	pygame.draw.rect(surface, black, [x_pos, y_pos + b_height + gap, b_width, surfaceHeight])

def replay_or_quit():
	for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

		elif event.type == pygame.KEYDOWN:
			continue

		return event.key

	return None

def makeTextObjs(text, font):
	textSurface = font.render(text, True, red)
	return textSurface, textSurface.get_rect()

def msgSurface(text):
	smallText = pygame.font.Font('freesansbold.ttf', 20)
	largeText = pygame.font.Font('freesansbold.ttf', 150)

	titleTextSurf, titleTextRect = makeTextObjs(text, largeText)
	titleTextRect.center = surfaceWidth / 2, surfaceHeight / 2
	surface.blit(titleTextSurf, titleTextRect)

	typTextSurf, typTextRect = makeTextObjs('Press any key to continue!', smallText)
	typTextRect.center = surfaceWidth / 2, ((surfaceHeight / 2) + 100)
	surface.blit(typTextSurf, typTextRect)

	pygame.display.update()
	time.sleep(1)

	while replay_or_quit() == None:
		clock.tick()

	main()

def gameOver():
	msgSurface('Kaboom!')

def helicopter(x, y, image):
	surface.blit(img, (x,y))

pygame.init()

surfaceWidth = 1100
surfaceHeight = 700

img_height = 67
img_width  = 105

surface = pygame.display.set_mode((surfaceWidth,surfaceHeight))
pygame.display.set_caption('Helicopter')
clock = pygame.time.Clock()

img = pygame.image.load('heliport.png')

def main():
	x = 75
	y = (surfaceHeight / 2) + (img_height / 2)
	y_move = 1

	x_pos = surfaceWidth
	y_pos = 1

	b_width    = 100
	b_height   = randint(0,  (surfaceHeight / 2))
	gap        = img_height * 3
	block_move = 4

	current_score = 0

	game_over = False

	while not game_over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_over = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					y_move = -5
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP:
					y_move = 5

		y += y_move

		surface.fill(white)
		helicopter(x, y, img)

		score(current_score)

		blocks(x_pos, y_pos, b_width, b_height, gap)
		x_pos -= block_move

		if boundary_collision(y):
			gameOver()

		if x_pos < (-1 * b_width):
			x_pos = surfaceWidth
			b_height = randint(0, surfaceHeight / 2)
			current_score += 1

		if upper_block_collision(x, x_pos, y, y_pos, b_height, b_width, gap):
			gameOver()

		if lower_block_collision(x, x_pos, y, y_pos, b_height, b_width, gap):
			gameOver()

		if 3 <= current_score < 5:
			block_move = 5
			gap = img_height * 2.8

		if 5 <= current_score < 10:
			block_move = 6
			gap = img_height * 2.6

		if 10 <= current_score < 15:
			block_move = 8
			gap = img_height * 2.4

		pygame.display.update()
		clock.tick(60)

main()
pygame.quit()
quit()	