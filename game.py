import pygame
import os
pygame.font.init()          #this initializes the pygame font library
pygame.mixer.init()      #initialising the sound effect library in python.

WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First game")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0, 0)
YELLOW = (255, 255, 0)
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)            #(x position[starting from the middle, substracting half of the width], y position = 0[from the top to the bottom], width, height [of the screen])
HEALTH_FONT = pygame.font.SysFont("Arial", 30)  #font of the health. (name of the font, size)
WINNER_FONT = pygame.font.SysFont("Arial", 100)
FPS = 60                #Frames per second. It will define how quickly or frames per second we want our game to update at.
VEL = 5              #since we are using it multiple times
BULLET_VEL = 7              #to determine how fast the bullets will be fired
MAX_BULLETS = 10           #setting the max number of bullets the players can shoot
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 70, 55
YELLOW_HIT = pygame.USEREVENT + 1       #creating an event. It represents the number for a custom event
RED_HIT = pygame.USEREVENT + 2          #+2 because otherwise it would be the same event that YELLOW_HIT since thw would have the same representing number
# Importing spaceships and resizing and rotating the images.
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))      #importing the spaceship
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)                     
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png")) 
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)  
#importing background
SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space1.png")), (WIDTH, HEIGHT))
#importing sounds. .Sound instead of load for sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):           #the position will be defined in the main method
        WIN.blit(SPACE, (0, 0))              #always draw the background first. Blit it's going to copy the contents of one Surface onto another Surface. (Block transfer)
        pygame.draw.rect(WIN, BLACK, BORDER)      #drawing a rectangle (surface you are drawing onto, colour, passing my rectangle previously defined[BORDER])        
        red_health_text = HEALTH_FONT.render("Score: " + str(red_health), 1, WHITE)          #using the defined fond to render some text. (text, anti aliasing /always 1/, colour)
        yellow_health_text = HEALTH_FONT.render("Score: " + str(yellow_health), 1, WHITE)    #drawinf the score before the spaceships so the overlap it
        WIN.blit(red_health_text, (785 , 10))      #position of the score. Best way to do it: (WIDTH - red_health_text.get_width() - 10)   --> this gets width of the text and substract that from thw width of the screen, so it is right at the edge and -10 so it has a 10px pad from the edge
        WIN.blit(yellow_health_text, (10, 10))        
        WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))           #yellow is a pygame.Rect rectangle                       #blit() when you want to draw a surface onto the screen, then you define the position (it draws from the top left corner)
        WIN.blit(RED_SPACESHIP, (red.x, red.y))                     #red is a pygame.Rect rectangle 
        
        for bullet in red_bullets:                            #looping through and drawing the bullets onto the screen
            pygame.draw.rect(WIN, RED, bullet)
        for bullet in yellow_bullets:                            #looping through and drawing the bullets onto the screen
            pygame.draw.rect(WIN, YELLOW, bullet)
        pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):    #easier to see 
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:     #left   #it won't let the spaceship move below 0
        yellow.x -= VEL           #you substract values as you move closer to 0,0 (top left)
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x + 15:     #right   #check the width of the image(spaceship), so the width of the image is not on top of the border
        yellow.x += VEL                          #you add values as you move further to 0,0 (top left)
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:     #up
        yellow.y -= VEL 
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:     #down  #only height because it gives us the height of the screen and -15 so it doesn't moves down the screen
        yellow.y += VEL 

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:     #left   #checking if it's greater than the border.x + border.width
        red.x -= VEL           #you substract values as you move closer to 0,0 (top left)
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:     #right   #the movement to the right relies on the width of the screen 
        red.x += VEL                          #you add values as you move further to 0,0 (top left)
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:     #up
        red.y -= VEL 
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:     #down
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):          #this will move the bullets, it will handle the colission of the them, and handle removing the bullets when they get oddthe screen or collide with the spaceship
    for bullet in yellow_bullets:                       #looping through the yellow bullets to check if they collide or go off
        bullet.x += BULLET_VEL                 #moving the bullet
        if red.colliderect(bullet):        #checking if there is a collision with the other player, passing the bullet. colliderect() only works if both objects are rectangles
            pygame.event.post(pygame.event.Event(RED_HIT))    #making a new event that says the red player was hit
            yellow_bullets.remove(bullet)                #removing the bullet when it hits the other player
        elif bullet.x > WIDTH:           #elif so we don't potentially remove the bullet twice
            yellow_bullets.remove(bullet)               #removing the bullet when it goes off the screen
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))   #when you post an event it gets added to the pygame.event.get() function
            red_bullets.remove(bullet)
        elif bullet.x < 0:            #when it's off the screen we are substracting the velocity
            red_bullets.remove(bullet) 

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))   #positioning the text in the middle od the screen. get_width will get the width of text (how wide we waant the text to be) and /2 so it takes whatever half of the width and substract it from the x and it'll be perfectly in the middle of the screen
    pygame.display.update()
    pygame.time.delay(5000)   #we are going to show who won for 5 seconds and then we are going to restart the game

def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)                 #define the position/rectangle that represents the spaceship (x position, y position, the width and height I want my rectangle to be at)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets = []                  #a list of all the bullets. To create a bullet,  we add one to the list and we will draw these bullets in their x and y position and we will move them in the direction they were fired
    yellow_bullets = []                 
    red_health = 10
    yellow_health = 10
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)                #It controls the speed of the while loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()         #it will stop when pressing the X. 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()

            if event.type == pygame.KEYDOWN:                         #to detect if a key is physically pressed down or released.
                if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 + 4, 10, 5)      #creating a rectangle that's add to the position we want it to be fired from. the bullet is placed. The bullet is placed at the edge of the body of the spaceship(its x position + its width, we take y position -the top left hand corner of the image- and we add the height/2 so it comes from the middle of the image, then the width and height of the bullet(10 and 5 pxls)) 
                    yellow_bullets.append(bullet)   #we append the bullet into the list
                    BULLET_FIRE.play()                   #using sounds previously loaded
                if event.key == pygame.K_KP_ENTER and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 + 4, 10, 5)     #we don't add the width. Since it is facing to the left(0, 0) and we want the bullets to come out of the left side.
                    red_bullets.append(bullet)
                    BULLET_FIRE.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()        #using sounds previously loaded
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins!"
        if yellow_health <= 0:
            winner_text = "Red wins!"
        if winner_text != "":
            draw_winner(winner_text)   #it'll draw the winner_text, it will pause for 5 seconds, and it'll start again
            break              

        keys_pressed = pygame.key.get_pressed()             #every time the while loop is running and we reach this line it will tell us what keys are currently being pressed down
        yellow_handle_movement(keys_pressed, yellow)        #calling the function
        red_handle_movement(keys_pressed, red)              #calling the function
        handle_bullets(yellow_bullets, red_bullets, yellow, red)      #
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)  

    main() #instead of pygame.quit() to restart the game whenever there's a winner

if __name__ == "__main__":        #we are only running this function if we run this file directly
    main()


#// instead of / because you cannot have floating points when you create a rectangle. 2 slashes for integer division