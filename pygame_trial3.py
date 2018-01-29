import pygame
import time
import math

pygame.init()
display_width = 1000
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (180,0,0)
green = (0, 180, 0)
blue = (0, 0, 255)
bright_green = (0, 200, 0)
bright_red = (0, 200, 0)

bullet1_color = bullet2_color = (30, 30, 30)
bullet1_radius = bullet2_radius = 4

pause = False
#end = True

player1_img = pygame.image.load('broccoli.png')
player2_img = pygame.image.load('carrot.png')

player1_img_orig = player1_img
player2_img_orig = player2_img

player1_width = 107 
player1_height = 89
player2_width = 84
player2_height = 111

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Battleground')
clock = pygame.time.Clock()


def bullet(bulletx, bullety, bulletu, bulletv):
	global bullet1_color, bullet2_color, bullet1_radius, bullet2_radius
	pygame.draw.circle(gameDisplay, bullet1_color, (math.ceil(bulletx), math.ceil(bullety)), bullet1_radius)
	pygame.draw.circle(gameDisplay, bullet2_color, (math.ceil(bulletu), math.ceil(bulletv)), bullet2_radius)



def players(x, y, u, v):
	gameDisplay.blit(player1_img, (x,y))
	gameDisplay.blit(player2_img, (u,v))


def text_objects(text, font, color):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()


def message_display(text, timesleep):
	largeText = pygame.font.Font('freesansbold.ttf', 80)
	textSurface, textRect = text_objects(text, largeText, red)
	textRect.center = ((display_width/2),(display_height/2))
	gameDisplay.blit(textSurface, textRect) # this is done in the background, thus update is needed

	pygame.display.update() # important!

	time.sleep(timesleep)
	#game_loop() #change to pause


def score(name, count, x, y, color):
	font = pygame.font.SysFont(None, 25)
	text = font.render(name + ": " + str(count), True, color)
	gameDisplay.blit(text, (x,y) )


def hit():
	message_display('Ah!', 0)


#referred to stackoverflow
def rotate(img, orig_x, orig_y, angle):
	global gameDisplay
	center = (orig_x/2, orig_y/2)
	rObj = pygame.transform.rotate(img, angle%360)
	size = rObj.get_size()
	hSize = [n/2 for n in size]
	pos = (center[0]-hSize[0],center[1]-hSize[1])

	#gameDisplay.blit(rObj, pos)
	return rObj


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


		button("Continue", 250, 450, 100, 50, green, bright_green, unpause)
		button("Quit!", 650, 450, 100, 50, red, bright_red, quitgame)

		pygame.display.update()
		clock.tick(15)


def end(winner_num):
	global player1_img, player2_img

	gameDisplay.fill(white)

	if winner_num == 1:
		gameDisplay.blit(pygame.image.load("broccolichicken.png"), (display_width/2 - 150, 65))
	else:
		gameDisplay.blit(pygame.image.load("carrotchicken.png"), (display_width/2 - 100, 85))

	largeText = pygame.font.Font('freesansbold.ttf', 40)
	textSurface, textRect = text_objects("Winner Winner, Chicken's Dinner!", largeText, black)
	textRect.center = ((display_width/2),(display_height/2))
	gameDisplay.blit(textSurface, textRect)	

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitgame()

		button("Play Again", 250, 450, 150, 50, green, bright_green, game_loop)
		button("Quit!", 650, 450, 100, 50, red, bright_red, quitgame)

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
		textSurface, textRect = text_objects("Battleground", largeText, black)
		textRect.center = ((display_width/2),(display_height/2))
		gameDisplay.blit(textSurface, textRect)


		button("Go!", 250, 450, 100, 50, green, bright_green, game_loop)
		button("Quit!", 650, 450, 100, 50, red, bright_red, quitgame)

		pygame.display.update()
		clock.tick(15)	


def game_loop():

	global player1_img
	global player2_img
	global pause

	x = (display_width * 0.01)
	y = (display_height * 0.7)
	u = (display_width * 0.7)
	v = (display_height * 0.1)

	x_change =0
	y_change = 0
	u_change =0
	v_change = 0

	game_exit = False

	shoot1 = False
	shoot2 = False

	angle1 = 0
	angle2 = 0

	bullet1_speed = 20
	bullet2_speed = 20

	player1_score = 0
	player2_score = 0

	inc_1 = 0
	inc_2 = 0

	benchmark = 10

	bullet_startx = math.ceil(x) + player1_width
	bullet_starty = math.ceil(y) + math.ceil(player1_height/2) + 8
	bullet_startu = math.ceil(u)
	bullet_startv = math.ceil(v) + math.ceil(player2_height/2) + 15

	while not game_exit:
		for event in pygame.event.get():
			#print(event)

			if event.type == pygame.QUIT: #user quits
				quitgame()
			#--------------------------------------------------- Player1 commands -----------------------------------------------------------------

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_change = -5
				if event.key == pygame.K_RIGHT:
					x_change = 5
				if x > (display_width - player1_width) +5  and event.key == pygame.K_RIGHT: # still buggy
					x_change = 0
				if x < 0 and event.key == pygame.K_LEFT:
					x_change = 0

				if event.key == pygame.K_UP:
					y_change = -5
				if event.key == pygame.K_DOWN:
					y_change = 5
				if y > (display_height - player1_height) +5  and event.key == pygame.K_DOWN: # still buggy
					y_change = 0
				if y < 0 and event.key == pygame.K_UP:
					y_change = 0
					'''
				if event.key == pygame.K_p:
					pause = True
					pause()
	'''
				if event.key == pygame.K_SPACE:
					shoot1 = True

				if event.key == pygame.K_n:
					angle1 += 10
					player1_img = rotate(player1_img_orig, x, y, angle1)

				if event.key == pygame.K_m:
					angle1 -=10
					player1_img = rotate(player1_img_orig, x, y, angle1)


				# ------------------------------------------- Player2 commands  -----------------------------------------------------
						
				if event.key == pygame.K_f:
					u_change = -5
				if event.key == pygame.K_h:
					u_change = 5
				if u > (display_width - player2_width) +5  and event.key == pygame.K_h: # still buggy
					u_change = 0
				if u < 0 and event.key == pygame.K_f:
					u_change = 0

				if event.key == pygame.K_t:
					v_change = -5
				if event.key == pygame.K_g:
					v_change = 5
				if v > (display_height - player2_height) +5  and event.key == pygame.K_g: # still buggy
					v_change = 0
				if v < 0 and event.key == pygame.K_t:
					v_change = 0

				if event.key == pygame.K_TAB:
					shoot2 = True

				if event.key == pygame.K_q:
					angle2 += 10
					player2_img = rotate(player2_img_orig, u, v, angle2)

				if event.key == pygame.K_w:
					angle2 -=10
					player2_img = rotate(player2_img_orig, u, v, angle2)

				if event.key == pygame.K_p:
					pause = True
					paused()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					x_change = 0

				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					y_change = 0

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_f or event.key == pygame.K_h:
					u_change = 0

				if event.key == pygame.K_t or event.key == pygame.K_g:
					v_change = 0

		x += x_change
		y += y_change
		u += u_change
		v += v_change

		gameDisplay.fill(white)

		bullet(bullet_startx, bullet_starty, bullet_startu, bullet_startv)

		speed_ratio1 = (bullet_starty - (y + player1_height/2)) / (bullet_startx - (x + player1_width/2))
		speed_ratio2 = (bullet_startv - (v + player2_height/2)) / (bullet_startu - (u + player2_width/2))

		#-------------- Bullet1 speed computation----------------

		if shoot1 == True and not ((bullet_startx > display_width) or (bullet_starty > display_height) or (bullet_startx < 0) or (bullet_starty < 0)):
			print('shoot1')
			if not (90 < angle1 <= 270):
				bullet_startx += bullet1_speed / (math.sqrt(1 + speed_ratio1**2))
				bullet_starty += bullet1_speed / (math.sqrt(1 + speed_ratio1**2)) * speed_ratio1
			elif (90 < angle1 < 180): 
				bullet_startx -= bullet1_speed / (math.sqrt(1 + speed_ratio1**2))
				bullet_starty += bullet1_speed / (math.sqrt(1 + speed_ratio1**2)) * (-speed_ratio1)
			else:
				speed_ratio1 = -speed_ratio1
				bullet_startx -= bullet1_speed / (math.sqrt(1 + speed_ratio1**2))
				bullet_starty += bullet1_speed / (math.sqrt(1 + speed_ratio1**2)) * speed_ratio1				


		else: 
			shoot1 = False
			inc_1 = 0
			#----------------------------- Bullet1 position computation ------------------------
			angle1_rad = -(math.pi/180) * angle1

			bullet_startx += math.ceil(x)+player1_width
			bullet_starty += math.ceil(y)+player1_height/2 + 8

			bullet_startx = (player1_width/2)*math.cos(angle1_rad) - 8 * math.sin(angle1_rad) #factored in rotation
			bullet_starty = 8 * math.cos(angle1_rad) + (player1_width/2)*math.sin(angle1_rad)

			bullet_startx += math.ceil(x)+player1_width/2
			bullet_starty += math.ceil(y)+player1_height/2



		#--------------------------- Bullet2 speed computation ------------------------------ 

		if shoot2 == True and not ((bullet_startu > display_width) or (bullet_startv > display_height) or (bullet_startu < 0) or (bullet_startv < 0)):
			print('shoot2')
			if (90 < angle2 < 270):
				bullet_startu += bullet2_speed / (math.sqrt(1 + speed_ratio2**2))
				bullet_startv += bullet2_speed / (math.sqrt(1 + speed_ratio2**2)) * speed_ratio2
			elif (270 <= angle2 < 360): 
				bullet_startu -= bullet2_speed / (math.sqrt(1 + speed_ratio2**2))
				bullet_startv -= bullet2_speed / (math.sqrt(1 + speed_ratio2**2)) * (-speed_ratio2)
			else:
				speed_ratio2 = -speed_ratio2
				bullet_startu -= bullet2_speed / (math.sqrt(1 + speed_ratio2**2))
				bullet_startv += bullet2_speed / (math.sqrt(1 + speed_ratio2**2)) * speed_ratio2				


		else: 
			shoot2 = False
			inc_2 = 0
			#----------------------------- Bullet2 position computation ------------------------
			# Bug fix required, recompute bullet path
			#bullet_startu = math.ceil(u)
			#bullet_startv = math.ceil(v) + math.ceil(player2_height/2)

			angle2_rad = -(math.pi/180) * angle2

			bullet_startu = (- player2_width/2)*math.cos(angle2_rad) - 15 * math.sin(angle2_rad) #factored in rotation
			bullet_startv = 15 * math.cos(angle2_rad) + (- player2_width/2)*math.sin(angle2_rad)

			bullet_startu += math.ceil(u)+player2_width/2
			bullet_startv += math.ceil(v)+player2_height/2


		# ---------------------------------- Player1 hits Player2-------------------------------------------------

		if bullet_starty > v and not(bullet_starty + bullet1_radius > v + player2_height) or bullet_starty < v and not (bullet_starty+bullet1_radius < v): # bug fix
			#print('y crossover')
			#if bullet_startx < u and bullet_startx + bullet1_radius > u:
				#print('x crossover')
				#hit()

			#elif bullet_startx < u + player2_width and bullet_startx + bullet1_radius > u + player2_width:
				#print('x crossover')
				#hit()

			if bullet_startx > u and bullet_startx + bullet1_radius < u + player2_width:
				print('x crossover')
				if inc_1 == 0:
					inc_1 = 1
					player1_score += inc_1
					if player1_score == benchmark :
						end(1)
				
				hit()

		# ---------------------------------- Player2 hits Player1-------------------------------------------------

		if bullet_startv > y and not(bullet_startv + bullet2_radius > y + player1_height) or bullet_startv < y and not (bullet_startv + bullet2_radius < y): # bug fix
			#print('v crossover')
			#if bullet_startu < x and bullet_startu + bullet2_radius > x:
				#print('u crossover')
				#hit()

			#elif bullet_startu < x + player1_width and bullet_startu + bullet2_radius > x + player1_width:
				#print('u crossover')
				#hit()

			if bullet_startu > x and bullet_startu + bullet2_radius < x + player1_width:
				print('u crossover')
				if inc_2 == 0:
					inc_2 = 1
					player2_score+= inc_2
					if player2_score == benchmark:
						end(2)

				hit()

		score("Player1", player1_score, 0, 0, blue)
		score("Player2", player2_score, 100, 0, red)
		players(x, y, u, v)

		pygame.display.update()
		clock.tick(60)

game_intro()
game_loop()
quitgame()
