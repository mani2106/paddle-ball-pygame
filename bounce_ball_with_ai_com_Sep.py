import pygame
import random

white = (0, 0, 0)
black = (255, 255, 255)
blue =  (0, 0, 255)



class ai(pygame.sprite.Sprite):
    width = 10
    height = 75
    my_joystick = None
    def __init__(self, x, y):
        super().__init__() 
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self):
        self.rect.y=ball.rect.y
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > screen_height - self.height:
            self.rect.y = screen_height - self.height





class Player(pygame.sprite.Sprite):
    width = 10
    height = 75
    my_joystick = None
    def __init__(self, x, y, joystick_no):
        super().__init__() 
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(white)
        self.score=0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        joystick_count = pygame.joystick.get_count()
        if joystick_count < joystick_no+1:
            print ("Error, I didn't find enough joysticks. Found ", joystick_count)
        else:
            self.my_joystick = pygame.joystick.Joystick(joystick_no)
            self.my_joystick.init()
        

    def update(self):
        if self.my_joystick != None:
            vert_axis_pos = self.my_joystick.get_axis(1)   
            self.rect.y = self.rect.y+vert_axis_pos*10
            if self.rect.y < 0:
                self.rect.y = 0
            if self.rect.y > screen_height - self.height:
                self.rect.y = screen_height - self.height

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill((blue))

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    
class Ball(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    walls = None
    def __init__(self, x, y, walls):
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill(white)
        self.score=0
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        
        self.walls = walls
        
    def update(self):
        old_x = self.rect.x
        new_x = old_x + self.change_x
        self.rect.x = new_x
        collide = pygame.sprite.spritecollide(self, self.walls, False)
        if collide:
            self.score+=1
            pygame.mixer.music.load('click.wav')
            pygame.mixer.music.play()
            self.rect.x = old_x
            self.change_x *= -1

        old_y = self.rect.y
        new_y = old_y + self.change_y
        self.rect.y = new_y
        collide = pygame.sprite.spritecollide(self, self.walls, False)
        if collide:
            pygame.mixer.music.load('laser5.ogg')
            pygame.mixer.music.play()
            self.rect.y = old_y
            self.change_y *= -1
            
        if self.rect.x < -20 or self.rect.x > screen_width + 20:
            self.change_x = 0
            self.change_y = 0



pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption('Bounce')
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)

wall_list = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
movingsprites = pygame.sprite.Group()

player1 = Player(10, screen_height / 2,0)
all_sprites.add(player1)
wall_list.add(player1)
movingsprites.add(player1)

player2 = ai(screen_width - 20, screen_height / 2)
all_sprites.add(player2)
wall_list.add(player2)
movingsprites.add(player2)

wall = Wall(0, 0, screen_width, 10) 
wall_list.add(wall)
all_sprites.add(wall)

wall = Wall(0, screen_height - 10, screen_width, screen_height) 
wall_list.add(wall)
all_sprites.add(wall)

ball = Ball( -50, -50, wall_list )
movingsprites.add(ball)
all_sprites.add(ball)

clock = pygame.time.Clock()

done = False
diff=int(input("Welcome to the Game\nChoose Difficulty:\n1.EASY\n2.MEDIUM\n3.HARD\n"))
while not done:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            if ball.change_y == 0:
                ball.rect.x = screen_width/2
                ball.rect.y = random.randrange(10, screen_height - 15)
                ball.change_y = random.randrange(-5, 6)
                ball.change_x =  random.randrange(5, 10)
                if( random.randrange(2) == 0 ):
                    ball.change_x *= -1
                        
    movingsprites.update()
    screen.fill(black)
    all_sprites.draw(screen)
    pygame.display.flip()
    if(diff==2):
        clock.tick(50)
    elif(diff==1):
        clock.tick(20)
    elif(diff==3):
        clock.tick(90)
    else:
        clock.tick(25)

pygame.quit()
print("Congrats your score: ",ball.score)
