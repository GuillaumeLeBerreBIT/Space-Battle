import pygame, os
# Now closing pygame will cause an error, because we stil keep the while loop open >> Most secure to close pygame == sys module
# One of the commands lets you close any kind of code you have opened entirely 
from sys import exit


############################ CONSTANTS ############################
WIDTH, HEIGHT = 900, 500

# Setting up the screen for pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Set the name of the Pygame window
pygame.display.set_caption("Space Invaders")

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

WHITE = (255, 255, 255)

FPS = 60

VEL = 5

BULLET_VEL = 7
MAX_BULLETS = 3
# Create a new EVENT and check for that event and do something with it when it occurs
# Represent the number for the CUSTOM USER EVENT
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
# Font Text
pygame.font.init()
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

pygame.mixer.init()
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

# This will draw the rectangle from the (0,0) position thus need to substract the half of the width of the object
# To place the rectangle exactly in the middle of the screen
# Rect(X, Y, WIDTH, HIEGHT)
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# This will start Pygame and all sub parts needed to make a game, run images, plays sound, ...
# Always need to call first
#pygame.init()

# Due to different operating systems to not have problems with slashes use os
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))  # Removing alpha values
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))

# Need to adjust the scale of the IMAGES provided. 
# Downscaling the (width, height) of the image
# Immediatly rotating the pygame scaled imgae to face towards each other
# This one will look towards the RIGHT side of the field. 
yellow_spaceship_scaled = pygame.transform.rotate(
    pygame.transform.scale( YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
# This one looks to the LEFT field
red_spaceship_scaled = pygame.transform.rotate(pygame.transform.scale(
        RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

space_background_scaled = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # The background of the game over screen >>  Parse in tuple RGB
    # Draw the space background  
    screen.blit(space_background_scaled, (0,0))
    # This will draw a rectangle on the screen (DISPLAY, COLOR, RECTANGLE POSITION)
    pygame.draw.rect(screen, 'Black', BORDER)
    
    # These are two text objects which you want to draw on the screen
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, 'White')
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, 'White')
    
    # Want to draw the text for who won
    # Get the WIDTH of the text and subtracts from WIDTH of screen and also at a PADDING of 10 pixels
    screen.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    screen.blit(yellow_health_text, (10, 10))
    
    # Blit when u want to draw a surface on the screen. SCREEN STARTS AT TOP LEFT (0,0)
    # Using the rectangle object position >> Can be used to change the location of the object on the screen. 
    screen.blit(yellow_spaceship_scaled, (yellow.x, yellow.y))
    screen.blit(red_spaceship_scaled, (red.x, red.y))
    
    for bullet in red_bullets:
        pygame.draw.rect(screen, 'Red', bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(screen, 'Yellow', bullet)
    
    # Draw all our elements & update everything
    pygame.display.update()    # Updates display surface of everything drawn inside the while loop
        
def yellow_handle_movement(keys_pressed, yellow):
    # YELLOW SPACESHIP
    # When subtracting the current VEL of X position, if greater then 0 will move otherwise will not move any further to the left
    if keys_pressed[pygame.K_q] and yellow.x - VEL > 0:    # LEFT
        yellow.x -= VEL        # This will move the object to the left
    # Since are incrementing towards the right, do not want to pass the border in middle of screen
    # BUT the start pos of image is (0,0), so can still move over a bit need to ADD IMAGE WIDTH!
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:    # RIGHT
        yellow.x += VEL        # Moving the object to the right
    # Will check wether can not move out of the screen   
    if keys_pressed[pygame.K_z] and yellow.y - VEL > 0:    # UP
        yellow.y -= VEL        # Move the object up
    # Since problem with the figure size substract - 15 of hieght so does not go out of windows, little fix
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:    # DOWN
        yellow.y += VEL        # Moving the object down

def red_handle_movement(keys_pressed, red):
    # YELLOW SPACESHIP
    # Can only move when the X position is greater then BORDER x + width 
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:    # LEFT
        red.x -= VEL        # This will move the object to the left
    # Can only move if x below width of the screen
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:    # RIGHT
        red.x += VEL        # Moving the object to the right
    # Can  move up if the y pos is below 0
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:    # UP
        red.y -= VEL        # Move the object up
    # Can move down of the y pos is bigger then HEIGHT 
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:    # DOWN
        red.y += VEL        # Moving the object down
        
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    # 1) Move the bullets
    # 2) Check the collision of the bullets
    # 3) Remonving the bullet when colliding with character or removed from the screen
    
    for bullet in yellow_bullets:
        # Move the bullet to the right sidee (towards Red)
        bullet.x += BULLET_VEL
        # Easy way to check whether the bullet collides with the character
        if red.colliderect(bullet):
            # New event saying the red player was hit
            pygame.event.post(pygame.event.Event(RED_HIT))
            # When collided need to remove the bullet of the screen
            yellow_bullets.remove(bullet)
            
        # Need to remove th bullet when disappearing from the screen
        elif bullet.x > WIDTH: 
            # When collided need to remove the bullet of the screen
            yellow_bullets.remove(bullet)            

    for bullet in red_bullets:
        # Move the bullet to the right sidee (towards Red)
        bullet.x -= BULLET_VEL
        # Easy way to check whether the bullet collides with the character
        if yellow.colliderect(bullet):
            # New event saying the red player was hit
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            # When collided need to remove the bullet of the screen
            red_bullets.remove(bullet)
        
        # Need to remove the bullet from the list whedn of the screen as well
        elif bullet.x < 0:
            red_bullets.remove(bullet)
    

def draw_winner(text):
    # Render the font 
    draw_text = WINNER_FONT.render(text, 1, 'White')
    # This will put it directly in the middle of the screen
    screen.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, 
                            HEIGHT/2 - draw_text.get_height()/2))
    
    pygame.display.update()
    pygame.time.delay(5000)
    
# Creating the Pygame event loop that handles the main loop
# Redrawing window, checking collisions, updating score
def main():
    # Need to define the (X, Y, WIDTH, HEIGHT) to project the Rectangle
    red_rect =  pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow_rect =  pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    red_bullets =  []
    yellow_bullets = []

    red_health =  10
    yellow_health = 10
    
    # Very import issue is the FRAME RATE >> Want to keep it constant so game can be run consistently on any platform == 60 fps constant
    # Really want to create a clock object >> Handle Time & Frame Rate
    clock = pygame.time.Clock()
    
    # This is to run the code forever >> Inside this loop will run the entire game. 
    while True:
        # Telling the while loop to run not faster then 60 FPS
        clock.tick(FPS)
        
        # pygame.event.get() >> Would get all the events
        # Check for all possible events in Pygame
        for event in pygame.event.get():
            # If QUIT is an event that occurs >> Will quit Pygame
            if event.type == pygame.QUIT:
                pygame.quit()       # Closes pygame (polar pygame.init())
                exit()              # Closes the while loop
            
            # WATCH OUT FOR INDENTATION MISTAKES FOR EVENTS!!!!!!!!!!!!!!
            # Using the event type to check if any key is pressed 
            if event.type == pygame.KEYDOWN:
                # Check a specific key is pressed. -- > LCtrl pressed && Only can JUMP when player is in contact with the ground again. 
                # Also set a limit on the BULLETS can Fire at same time
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    
                    # By taking the in account the POS of the SPACESHIP and BULLET.
                    # X POS == X + WIDTH
                    # Y POS == Y + HEIGHT/2 + Need to subtract 2 for the bullet since the height is 5
                    bullet = pygame.Rect(
                        yellow_rect.x + yellow_rect.width, yellow_rect.y + yellow_rect.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    
                    # Same principle, here remove width from X pos since bullet will start on red Y == 0
                    bullet = pygame.Rect(
                        red_rect.x , red_rect.y + red_rect.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
                    
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        
        winner_text = ''
        # Checks of the health is below or equal to zero, which then is the winner
        if red_health <= 0:
            winner_text =  'Yellow Wins!'
        # Checks of the health is below or equal to zero, which then is the winner
        if yellow_health <= 0:
            winner_text = 'Red Wins!'
        
        if winner_text != '':
            draw_winner(winner_text)        # SOMEONE WON == NEED TO DISPLAY THAT WINNER
            break
              
        # This will tell what keys are currently pressed down
        # If the key stays pressed down it will register that it is being pressed.
        # >> This makes it so when continously pressed down multiple keys can move diagonallyt constantly 
        keys_pressed = pygame.key.get_pressed()
        # The movement is described inside this function
        yellow_handle_movement(keys_pressed, yellow_rect)
        red_handle_movement(keys_pressed, red_rect)
        
        handle_bullets(yellow_bullets, red_bullets, yellow_rect, red_rect)
        
        # To test can here change the position and this will move the object by continously incrementing its position. 
        #yellow_rect.x += 1
        
        # Update the X & Y position based on the arrow keys pressed
        
        # Draw the background window >> Draw first since keep Drawing on top of each other        
        draw_window(red_rect, yellow_rect, red_bullets, yellow_bullets, 
                    red_health, yellow_health)
        
    # So when the winner is decided >> Display winner text for 5 seconds >> Restart main() aka the game
    main()
                
# Making sure when calling this function only when Running this file!!
# __name__ is the name of the file & __main__ indicates it is the main file
if __name__ == "__main__":
    main()       