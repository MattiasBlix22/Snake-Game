import pygame
import random
import sys
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP 
#variables
SCREEN_WDITH = 400
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WDITH / GRID_SIZE
GRID_HEIGHT = SCREEN_WDITH / GRID_SIZE

UP = (0,-1)
DOWN = (0,1)
LEFT = (-1, 0)
RIGHT = (1,0)



#SNAKE CLASS
class Snake(object):
    def __init__(self):
        self.leangth = 2
        self.positions = [((SCREEN_WDITH/2), (SCREEN_HEIGHT/2))]
        self.direction = random.choice([UP,DOWN,LEFT,RIGHT])
        self.color = (0,255,0)
    def get_head_position(self):
        return self.positions[0]
    def turn(self, point):
        if self.leangth > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
    def move(self):
        cur = self.get_head_position()
        x,y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WDITH), (cur [1] + (y*GRID_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.leangth:
                self.positions.pop()
    def reset(self):
        self.leangth = 5
        self.positions = [((SCREEN_WDITH/2), (SCREEN_HEIGHT/2))]
        self.direction = random.choice([UP,DOWN,LEFT,RIGHT])
    def draw(self, surface):
        for position in self.positions:
            r = pygame.Rect((position[0], position[1]), (GRID_SIZE-2, GRID_SIZE-2))
            pygame.draw.rect(surface, self.color,r)
            pygame.draw.rect(surface, (93,216,228),r,1)
 
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    self.turn(UP)
                elif event.key == K_DOWN:
                    self.turn(DOWN)
                elif event.key == K_LEFT:
                    self.turn(LEFT)
                elif event.key == K_RIGHT:
                    self.turn(RIGHT)
    
        


#Apples
class Food(object):
    def __init__(self):
        self.position = (0,0)
        self.color = (223,163,49)
        self.randomize_pos()
    def randomize_pos(self):
        self.position = (random.randint(0,GRID_WIDTH-1) * GRID_SIZE, random.randint(0,GRID_HEIGHT-1) * GRID_SIZE)
        
    def draw(self,surface):
        r = pygame.Rect((self.position[0],self.position[1]), (GRID_SIZE,GRID_SIZE))
        pygame.draw.rect(surface, (255,0,0), r)
        pygame.draw.rect(surface,(255,0,0), r,1)

#Grid setup
def draw_grid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x+y) % 2 == 0:
                r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (0,0,0), r)
            else:
                 rr = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                 pygame.draw.rect(surface, (0,0,0), rr)
                
#main loop
def main():
    pygame.init()
    CCCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WDITH,SCREEN_HEIGHT),0, 32)
    pygame.display.set_caption("SNAKE")

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_grid(surface)


    snake = Snake()
    food = Food()

    
    #game loop
    while (True):
        CCCLOCK.tick(6)
        snake.handle_keys()
        draw_grid(surface)
        snake.move()

        if snake.get_head_position() == food.position:
            snake.leangth += 5
            food.randomize_pos()
        

        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0,0))
        pygame.display.update()

main()

