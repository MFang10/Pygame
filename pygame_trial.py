import pygame
import time
import random

pygame.init()
display_width = 800
display_height = 600

pause = False

black = (0,0,0)
white = (255,255,255)
red = (180,0,0)
green = (0, 180, 0)

bright_red = (200, 0, 0)
bright_green = (0, 200, 0)

block_color = (53,115,255)

car_width = 196
car_height = 174

carImg = pygame.image.load('vege.png')

gameDisplay = pygame.display.set_mode((display_width, display_height)) #w, h tuple
pygame.display.set_caption('Racing Vege')
clock = pygame.time.Clock() # we use this to set frame rate 

def things_dodged(count):
	font = pygame.font.SysFont(None, 25)
	text = font.render("Dodged: " + str(count), True, black)
	gameDisplay.blit(text, (0,0) )


def things(thingx, thingy, thingw, thingh, color):
	pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


def car(x,y):
	gameDisplay.blit(carImg,(x,y)) #(0,0) on upper left corner


def text_objects(text, font, color):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()


def message_display(text):
	largeText = pygame.font.Font('freesansbold.ttf', 80)
	textSurface, textRect = text_objects(text, largeText, black)
	textRect.center = ((display_width/2),(display_height/2))
	gameDisplay.blit(textSurface, textRect) # this is done in the background, thus update is needed

	pygame.display.update() # important!

	time.sleep(2)
	game_loop()


def crash():
	message_display('You Crashed')


def quitgame():
	pygame.quit()
	quit()


def button(msg, x, y, w, h, ic, ac, action = None): # inactive color, active color
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed() #click is a tuple (left_click, right_click, middle_click)

	if x + w > mouse[0] > x and y + h > mouse[1] > y:
		pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
		if click[0] == 1 and action != None:
			action() # Note that function reference is passed into this function
		#print("Launched")
	else:
		pygame.draw.rect(gameDisplay, ic, (x, y, w, h))	

	smallText = pygame.font.Font("freesansbold.ttf", 20)
	textSurface, textRect = text_objects(msg, smallText, white)
	textRect.center = ((x + (w/2)), (y + (h/2)))
	gameDisplay.blit(textSurface, textRect)	


def unpause():
	global pause
	pause = False


def paused():

	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.fill(white)
		largeText = pygame.font.Font('freesansbold.ttf', 80)
		textSurface, textRect = text_objects("Paused", largeText, black)
		textRect.center = ((display_width/2),(display_height/2))
		gameDisplay.blit(textSurface, textRect)


		button("Continue", 150, 450, 100, 50, green, bright_green, unpause)
		button("Quit!", 550, 450, 100, 50, red, bright_red, quitgame)

		pygame.display.update()
		clock.tick(15)


def game_intro():
	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.fill(white)
		largeText = pygame.font.Font('freesansbold.ttf', 80)
		textSurface, textRect = text_objects("Racing Vege", largeText, black)
		textRect.center = ((display_width/2),(display_height/2))
		gameDisplay.blit(textSurface, textRect)


		button("Go!", 150, 450, 100, 50, green, bright_green, game_loop)
		button("Quit!", 550, 450, 100, 50, red, bright_red, quitgame)

		pygame.display.update()
		clock.tick(15)

def game_loop():
	global pause

	x = (display_width * 0.45)
	y = (display_height * 0.4)

	x_change = 0

	thing_startx = random.randrange(0, display_width)
	thing_starty = -600
	thing_speed = 4
	thing_width = 50
	thing_height = 50
	dodged = 0
	game_exit = False


	while not game_exit:
		for event in pygame.event.get():
			#print(event)

			if event.type == pygame.QUIT: #user quits
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_change = -5
				if event.key == pygame.K_RIGHT:
					x_change = 5
				if x > (display_width - car_width) +5  and event.key == pygame.K_RIGHT: # still buggy
					x_change = 0
				if x < 0 and event.key == pygame.K_LEFT:
					x_change = 0
				if event.key == pygame.K_p:
					pause = True
					paused()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					x_change = 0

		x += x_change
			
		gameDisplay.fill(white)	


		things(thing_startx, thing_starty, thing_width, thing_height, block_color)
		thing_starty += thing_speed

		car(x,y)
		things_dodged(dodged)


		if thing_starty > display_height:
			thing_starty = 0 - thing_height
			thing_startx = random.randrange(0, display_width)
			dodged += 1
			#thing_speed+=0.5 #speed up the blocks
			#thing_width += (dodged * 1.2) #the blocks get wider

		if y < (thing_starty + thing_height) and not(y+car_height < thing_starty): # bug fix
			print('y crossover')
			if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx+thing_width:
				print("x crossover")
				crash()

			if x<thing_startx and x+car_width > thing_startx + thing_width:
				print("x crossover")
				crash()

		pygame.display.update() # param allowed for specific updates, otherwise whole surface updated
		clock.tick(60) #arg: frame rate

game_intro()
game_loop()
pygame.quit() 
quit()
