from collections import deque
import pygame
import random
import sys
import pygame as pg
from pygame.constants import K_1

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

        self.x = SCREEN_WDITH//2
        self.y = SCREEN_HEIGHT//2
        self.width = 20
        self.height = 20
        self.head = None
        self.speed = 20
        self.direction = None
        self.body = deque()
        self.segment = deque()
        self.head_color = pg.Color(220, 20, 60)
        self.body_color = pg.Color(57, 255, 20)
        self.outline_color = pg.Color(0, 0, 0)


    def draw_snake(self, surface):

        if len(self.body) > 0:
            for unit in self.segment:
                pg.draw.rect(surface, self.body_color,unit)
                pg.draw.rect(surface, self.outline_color, unit, 1)
        self.head = pg.Rect(self.x, self.y, self.width, self.height)
        pg.draw.rect(surface, (0,255,0), self.head)
        pg.draw.rect(surface, self.outline_color, self.head, 1)

    def snake_size(self):

        if len(self.body) != 0:
            index = len(self.body) - 1
            x = self.body[index][0]
            y = self.body[index][1]
            self.body.append([x, y])
            self.segment.append(pg.Rect(x, y, self.width, self.height))


    
    def movement(self):

        if self.direction == 'up':
            self.y -= self.speed
        if self.direction == 'down':
            self.y += self.speed
        if self.direction == 'right':
            self.x += self.speed
        if self.direction == 'left':
            self.x -= self.speed

    
        if len(self.body) > 0:
            self.body.pop()
            self.segment.pop()
        self.body.appendleft([self.x, self.y])
        self.segment.appendleft(pg.Rect(self.x, self.y, self.width, self.height))


    def hamomove(self, direction):

        if direction == 'up' and self.direction != 'down':
            self.direction = 'up'
        if direction == 'down' and self.direction != 'up':
            self.direction = 'down'
        if direction == 'right' and self.direction != 'left':
            self.direction = 'right'
        if direction == 'left' and self.direction != 'right':
            self.direction = 'left'




#Apples
class Fruit(object):
    def __init__(self):
        self.position = (0,0)
        self.color = (223,163,49)
        self.randomize_pos()
        self.x,self.y = self.position
    def randomize_pos(self):
        self.position = (random.randint(0,GRID_WIDTH-1) * GRID_SIZE, random.randint(0,GRID_HEIGHT-1) * GRID_SIZE)
        self.x,self.y = self.position
    def get_pos(self):
        return self.position
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
def main(Fruit,Snake,cycle):
    snake = Snake()
    fruit = Fruit()
    position = (int(snake.x/20), int(snake.y/20))

    
    index = cycle.index(position)

    length = len(cycle)
    run = True

   
    while run:
        FPS = 1000

        clock = pg.time.Clock()
        clock.tick(FPS)
        
       
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        
        window.fill(pg.Color(0, 0, 0))
        fruit.draw(window)
        snake.draw_snake(window)
        if snake.x == fruit.x and snake.y == fruit.y:
            fruit.randomize_pos()
            snake.snake_size()
            
        if index + 1 < length and cycle[index+1] == (position[0] + 1, position[1]):
            snake.hamomove('right')
            position = (position[0] + 1, position[1])
        elif index + 1 < length and cycle[index+1] == (position[0] - 1, position[1]):
            snake.hamomove('left')
            position = (position[0] - 1, position[1])
        elif index + 1 < length and cycle[index+1] == (position[0], position[1] + 1):
            snake.hamomove('down')
            position = (position[0], position[1] + 1)
        elif index + 1 < length and cycle[index+1] == (position[0], position[1] - 1):
            snake.hamomove('up')
            position = (position[0], position[1] - 1)

        
        if index == length - 1:
            if cycle[0] == (position[0] + 1, position[1]):
                snake.hamomove('right')
                position = (position[0] + 1, position[1])
            elif cycle[0] == (position[0] - 1, position[1]):
                snake.hamomove('left')
                position = (position[0] - 1, position[1])
            elif cycle[0] == (position[0], position[1] + 1):
                snake.hamomove('down')
                position = (position[0], position[1] + 1)
            elif cycle[0] == (position[0], position[1] - 1):
                snake.hamomove('up')
                position = (position[0], position[1] - 1)
            index = 0
        else:
            index += 1


        snake.movement()
        pg.display.update()


        
def prim_maze_generator(grid_rows, grid_columns):

    directions = dict()
    vertices = grid_rows * grid_columns

    # Creates keys for the directions dictionary
    # Note that the maze has half the width and length of the grid for the hamiltonian cycle
    for i in range(grid_rows):
        for j in range(grid_columns):
            directions[j, i] = []

    # The initial cell for maze generation is chosen randomly
    x = random.randint(0, grid_columns - 1)
    y = random.randint(0, grid_rows - 1)
    initial_cell = (x, y)

    current_cell = initial_cell

    # Stores all cells that have been visited
    visited = [initial_cell]

    # Contains all neighbouring cells to cells that have been visited
    adjacent_cells = set()

    # Generates walls in grid randomly to create a randomized maze
    while len(visited) != vertices:

        # Stores the position of the current cell in the grid
        x_position = current_cell[0]
        y_position = current_cell[1]

        # Finds adjacent cells when the current cell does not lie on the edge of the grid
        if x_position != 0 and y_position != 0 and x_position != grid_columns - 1 and y_position != grid_rows - 1:
            adjacent_cells.add((x_position, y_position - 1))
            adjacent_cells.add((x_position, y_position + 1))
            adjacent_cells.add((x_position - 1, y_position))
            adjacent_cells.add((x_position + 1, y_position))

        # Finds adjacent cells when the current cell lies in the left top corner of the grid
        elif x_position == 0 and y_position == 0:
            adjacent_cells.add((x_position + 1, y_position))
            adjacent_cells.add((x_position, y_position + 1))

        # Finds adjacent cells when the current cell lies in the bottom left corner of the grid
        elif x_position == 0 and y_position == grid_rows - 1:
            adjacent_cells.add((x_position, y_position - 1))
            adjacent_cells.add((x_position + 1, y_position))

        # Finds adjacent cells when the current cell lies in the left column of the grid
        elif x_position == 0:
            adjacent_cells.add((x_position, y_position - 1))
            adjacent_cells.add((x_position, y_position + 1))
            adjacent_cells.add((x_position + 1, y_position))

        # Finds adjacent cells when the current cell lies in the top right corner of the grid
        elif x_position == grid_columns - 1 and y_position == 0:
            adjacent_cells.add((x_position, y_position + 1))
            adjacent_cells.add((x_position - 1, y_position))

        # Finds adjacent cells when the current cell lies in the bottom right corner of the grid
        elif x_position == grid_columns - 1 and y_position == grid_rows - 1:
            adjacent_cells.add((x_position, y_position - 1))
            adjacent_cells.add((x_position - 1, y_position))

        # Finds adjacent cells when the current cell lies in the right column of the grid
        elif x_position == grid_columns - 1:
            adjacent_cells.add((x_position, y_position - 1))
            adjacent_cells.add((x_position, y_position + 1))
            adjacent_cells.add((x_position - 1, y_position))

        # Finds adjacent cells when the current cell lies in the top row of the grid
        elif y_position == 0:
            adjacent_cells.add((x_position, y_position + 1))
            adjacent_cells.add((x_position - 1, y_position))
            adjacent_cells.add((x_position + 1, y_position))

        # Finds adjacent cells when the current cell lies in the bottom row of the grid
        else:
            adjacent_cells.add((x_position, y_position - 1))
            adjacent_cells.add((x_position + 1, y_position))
            adjacent_cells.add((x_position - 1, y_position))

        # Generates a wall between two cells in the grid
        while current_cell:

            current_cell = (adjacent_cells.pop())

            # The neighbouring cell is disregarded if it is already a wall in the maze
            if current_cell not in visited:

                # The neighbouring cell is now classified as having been visited
                visited.append(current_cell)
                x = current_cell[0]
                y = current_cell[1]

                # To generate a wall, a cell adjacent to the current cell must already have been visited
                # The direction of the wall between cells is stored
                # The process is simplified by only considering a wall to be to the right or down
                if (x + 1, y) in visited:
                    directions[x, y] += ['right']
                elif (x - 1, y) in visited:
                    directions[x-1, y] += ['right']
                elif (x, y + 1) in visited:
                    directions[x, y] += ['down']
                elif (x, y - 1) in visited:
                    directions[x, y-1] += ['down']

                break

    # Provides the hamiltonian cycle generating algorithm with the direction of the walls to avoid
    return hamiltonian_cycle(grid_rows, grid_columns, directions)


# Finds a hamiltonian cycle for the snake to follow to prevent collisions with its body segments
# Note that the grid for the hamiltonian cycle is double the width and height of the grid for the maze
def hamiltonian_cycle(grid_rows, grid_columns, orientation):

    # The path for the snake is stored in a dictionary
    # The keys are the (x, y) positions in the grid
    # The values are the adjacent (x, y) positions that the snake can travel towards
    hamiltonian_graph = dict()

    # Uses the coordinates of the walls to generate available adjacent cells for each cell
    # Simplified by only considering the right and down directions
    for i in range(grid_rows):
        for j in range(grid_columns):

            # Finds available adjacent cells if current cell does not lie on an edge of the grid
            if j != grid_columns - 1 and i != grid_rows - 1 and j != 0 and i != 0:
                if 'right' in orientation[j, i]:
                    hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 2, i*2)]
                    hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 2, i*2 + 1)]
                else:
                    hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 1, i*2 + 1)]
                if 'down' in orientation[j, i]:
                    hamiltonian_graph[j*2, i*2 + 1] = [(j*2, i*2 + 2)]
                    if (j*2 + 1, i*2 + 1) in hamiltonian_graph:
                        hamiltonian_graph[j * 2 + 1, i * 2 + 1] += [(j * 2 + 1, i * 2 + 2)]
                    else:
                        hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 1, i*2 + 2)]
                else:
                    hamiltonian_graph[j*2, i*2 + 1] = [(j*2 + 1, i*2 + 1)]
                if 'down' not in orientation[j, i-1]:
                    hamiltonian_graph[j*2, i*2] = [(j*2 + 1, i*2)]
                if 'right' not in orientation[j-1, i]:
                    if (j*2, i*2) in hamiltonian_graph:
                        hamiltonian_graph[j * 2, i * 2] += [(j * 2, i * 2 + 1)]
                    else:
                        hamiltonian_graph[j*2, i*2] = [(j*2, i*2 + 1)]

            # Finds available adjacent cells if current cell is in the bottom right corner
            elif j == grid_columns - 1 and i == grid_rows - 1:
                hamiltonian_graph[j*2, i*2 + 1] = [(j*2 + 1, i*2 + 1)]
                hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 1, i*2 + 1)]
                if 'down' not in orientation[j, i-1]:
                    hamiltonian_graph[j*2, i*2] = [(j*2 + 1, i*2)]
                elif 'right' not in orientation[j-1, i]:
                    hamiltonian_graph[j*2, i*2] = [(j*2, i*2 + 1)]

            # Finds available adjacent cells if current cell is in the top right corner
            elif j == grid_columns - 1 and i == 0:
                hamiltonian_graph[j*2, i*2] = [(j*2 + 1, i*2)]
                hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 1, i*2 + 1)]
                if 'down' in orientation[j, i]:
                    hamiltonian_graph[j*2, i*2 + 1] = [(j*2, i*2 + 2)]
                    hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 1, i*2 + 2)]
                else:
                    hamiltonian_graph[j*2, i*2 + 1] = [(j*2 + 1, i*2 + 1)]
                if 'right' not in orientation[j-1, i]:
                    hamiltonian_graph[j*2, i*2] += [(j*2, i*2 + 1)]

            # Finds available adjacent cells if current cell is in the right column
            elif j == grid_columns - 1:
                hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 1, i*2 + 1)]
                if 'down' in orientation[j, i]:
                    hamiltonian_graph[j*2, i*2 + 1] = [(j*2, i*2 + 2)]
                    hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 1, i*2 + 2)]
                else:
                    hamiltonian_graph[j*2, i*2 + 1] = [(j*2 + 1, i*2 + 1)]
                if 'down' not in orientation[j, i-1]:
                    hamiltonian_graph[j*2, i*2] = [(j*2 + 1, i*2)]
                if 'right' not in orientation[j-1, i]:
                    if (j*2, i*2) in hamiltonian_graph:
                        hamiltonian_graph[j * 2, i * 2] += [(j * 2, i * 2 + 1)]
                    else:
                        hamiltonian_graph[j*2, i*2] = [(j*2, i*2 + 1)]

            # Finds available adjacent cells if current cell is in the top left corner
            elif j == 0 and i == 0:
                hamiltonian_graph[j*2, i*2] = [(j*2 + 1, i*2)]
                hamiltonian_graph[j*2, i*2] += [(j*2, i*2 + 1)]
                if 'right' in orientation[j, i]:
                    hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 2, i*2)]
                    hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 2, i*2 + 1)]
                else:
                    hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 1, i*2 + 1)]
                if 'down' in orientation[j, i]:
                    hamiltonian_graph[j*2, i*2 + 1] = [(j*2, i*2 + 2)]
                    if (j*2 + 1, i*2 + 1) in hamiltonian_graph:
                        hamiltonian_graph[j * 2 + 1, i * 2 + 1] += [(j * 2 + 1, i * 2 + 2)]
                    else:
                        hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 1, i*2 + 2)]
                else:
                    hamiltonian_graph[j*2, i*2 + 1] = [(j*2 + 1, i*2 + 1)]

            # Finds available adjacent cells if current cell is in the bottom left corner
            elif j == 0 and i == grid_rows - 1:
                hamiltonian_graph[j*2, i*2] = [(j*2, i*2 + 1)]
                hamiltonian_graph[j*2, i*2 + 1] = [(j*2 + 1, i*2 + 1)]
                if 'right' in orientation[j, i]:
                    hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 2, i*2)]
                    hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 2, i*2 + 1)]
                else:
                    hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 1, i*2 + 1)]
                if 'down' not in orientation[j, i-1]:
                    hamiltonian_graph[j * 2, i * 2] += [(j * 2 + 1, i * 2)]

            # Finds available adjacent cells if current cell is in the left corner
            elif j == 0:
                hamiltonian_graph[j*2, i*2] = [(j*2, i*2 + 1)]
                if 'right' in orientation[j, i]:
                    hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 2, i*2)]
                    hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 2, i*2 + 1)]
                else:
                    hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 1, i*2 + 1)]
                if 'down' in orientation[j, i]:
                    hamiltonian_graph[j*2, i*2 + 1] = [(j*2, i*2 + 2)]
                    if (j*2 + 1, i*2 + 1) in hamiltonian_graph:
                        hamiltonian_graph[j*2 + 1, i*2 + 1] += [(j*2 + 1, i*2 + 2)]
                    else:
                        hamiltonian_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 1, i * 2 + 2)]
                else:
                    hamiltonian_graph[j*2, i*2 + 1] = [(j*2 + 1, i*2 + 1)]
                if 'down' not in orientation[j, i-1]:
                    hamiltonian_graph[j*2, i*2] += [(j*2 + 1, i*2)]

            # Finds available adjacent cells if current cell is in the top row
            elif i == 0:
                hamiltonian_graph[j*2, i*2] = [(j*2 + 1, i*2)]
                if 'right' in orientation[j, i]:
                    hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 2, i*2)]
                    hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 2, i*2 + 1)]
                else:
                    hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 1, i*2 + 1)]
                if 'down' in orientation[j, i]:
                    hamiltonian_graph[j*2, i*2 + 1] = [(j*2, i*2 + 2)]
                    if (j*2 + 1, i*2 + 1) in hamiltonian_graph:
                        hamiltonian_graph[j * 2 + 1, i * 2 + 1] += [(j * 2 + 1, i * 2 + 2)]
                    else:
                        hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 1, i*2 + 2)]
                else:
                    hamiltonian_graph[j*2, i*2 + 1] = [(j*2 + 1, i*2 + 1)]
                if 'right' not in orientation[j-1, i]:
                    hamiltonian_graph[j*2, i*2] += [(j*2, i*2 + 1)]

            # Finds available adjacent cells if current cell is in the bottom row
            else:
                hamiltonian_graph[j*2, i*2 + 1] = [(j*2 + 1, i*2 + 1)]
                if 'right' in orientation[j, i]:
                    hamiltonian_graph[j*2 + 1, i*2 + 1] = [(j*2 + 2, i*2 + 1)]
                    hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 2, i*2)]
                else:
                    hamiltonian_graph[j*2 + 1, i*2] = [(j*2 + 1, i*2 + 1)]
                if 'down' not in orientation[j, i-1]:
                    hamiltonian_graph[j*2, i*2] = [(j*2 + 1, i*2)]
                if 'right' not in orientation[j-1, i]:
                    if (j*2, i*2) in hamiltonian_graph:
                        hamiltonian_graph[j*2, i*2] += [(j*2, i*2 + 1)]
                    else:
                        hamiltonian_graph[j * 2, i * 2] = [(j * 2, i * 2 + 1)]

    # Provides the coordinates of available adjacent cells to generate directions for the snake's movement
    return path_generator(hamiltonian_graph, grid_rows*grid_columns*4)


# Generates a path composed of coordinates for the snake to travel along
def path_generator(graph, cells):

    # The starting position for the path is at cell (0, 0)
    path = [(0, 0)]

    previous_cell = path[0]
    previous_direction = None


    while len(path) != cells:

        if previous_cell in graph and (previous_cell[0] + 1, previous_cell[1]) in graph[previous_cell] \
                and previous_direction != 'left':
            path.append((previous_cell[0] + 1, previous_cell[1]))
            previous_cell = (previous_cell[0] + 1, previous_cell[1])
            previous_direction = 'right'
        elif previous_cell in graph and (previous_cell[0], previous_cell[1] + 1) in graph[previous_cell]  \
                and previous_direction != 'up':
            path.append((previous_cell[0], previous_cell[1] + 1))
            previous_cell = (previous_cell[0], previous_cell[1] + 1)
            previous_direction = 'down'
        elif (previous_cell[0] - 1, previous_cell[1]) in graph \
                and previous_cell in graph[previous_cell[0] - 1, previous_cell[1]] and previous_direction != 'right':
            path.append((previous_cell[0] - 1, previous_cell[1]))
            previous_cell = (previous_cell[0] - 1, previous_cell[1])
            previous_direction = 'left'
        else:
            path.append((previous_cell[0], previous_cell[1] - 1))
            previous_cell = (previous_cell[0], previous_cell[1] - 1)
            previous_direction = 'up'

    # Returns the coordinates of the hamiltonian cycle path
    return path


circuit = prim_maze_generator(int(SCREEN_HEIGHT/40), int(SCREEN_WDITH/40))
pygame.init()
window = pygame.display.set_mode((SCREEN_WDITH, SCREEN_HEIGHT))
pygame.display.set_caption('SNAKE')
main(Fruit, Snake, circuit)
