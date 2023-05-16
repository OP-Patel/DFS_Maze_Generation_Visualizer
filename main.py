import pygame
from random import choice
import pygame_gui
pygame.init()

class Cell:
    def __init__(self, x, y): #base vars
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.thickness = 2
    def current_cell(self): #draws the current cell/starting position
        x, y = self.x * tile, self.y * tile
        pygame.draw.rect(screen, (179, 122, 223), (x + 2, y + 2, tile - 2, tile - 2))
    def draw(self): #visually represent a cell of the maze by drawing its visited state
        x, y = self.x * tile, self.y * tile
        if self.visited:
            pygame.draw.rect(screen, (238,226, 229), (x, y, tile, tile))
        walls = ['top', 'right', 'bottom', 'left']
        for wall in walls: #iterates through the four sides of the cell and draws lines if needed
            if self.walls[wall]:
                if wall == 'top':
                    pygame.draw.line(screen, pygame.Color('black'), (x, y), (x + tile, y), self.thickness)
                elif wall == 'right':
                    pygame.draw.line(screen, pygame.Color('black'), (x + tile, y), (x + tile, y + tile), self.thickness)
                elif wall == 'bottom':
                    pygame.draw.line(screen, pygame.Color('black'), (x + tile, y + tile), (x, y + tile), self.thickness)
                elif wall == 'left':
                    pygame.draw.line(screen, pygame.Color('black'), (x, y + tile), (x, y), self.thickness)
    def check_cell(self, x, y): #retrieve cell at a position (x,y) on the grid, and sees if it is valid
        return self.grid_cells[x + y * cols] if 0 <= x < cols and 0 <= y < rows else False
    def check_neighbors(self): #stores the neighboring cells of the current cell that have not been visited yet in list
        self.grid_cells = grid_cells
        neighbors = [cell for cell in [self.check_cell(self.x, self.y - 1), self.check_cell(self.x + 1, self.y),
                                       self.check_cell(self.x, self.y + 1), self.check_cell(self.x - 1, self.y)]
                                       if cell and not cell.visited]
        return choice(neighbors) if neighbors else False #returns a randomly chosen cell from list
def remove_walls(current_cell, next_cell): #updates the wall information between the current cell and the next cell
    dx, dy = current_cell.x - next_cell.x, current_cell.y - next_cell.y #calculating relative positions
    if dx == 1:
        current_cell.walls['left'], next_cell.walls['right'] = False, False #left of current, and right of new, wall is removed
    elif dx == -1:
        current_cell.walls['right'], next_cell.walls['left'] = False, False
    if dy == 1:
        current_cell.walls['top'], next_cell.walls['bottom'] = False, False
    elif dy == -1:
        current_cell.walls['bottom'], next_cell.walls['top'] = False, False


#Basic vars
screen_size = (1000,600) #tuple of screen size
screen_width = 1000  #screen width
screen_height = 600  #screen height
tile = 40  #tiles constant
cols, rows = screen_width // tile, screen_height // tile  #initialize the dimensions of the cols and rows of maze
all_visited = False #initalization of the visited var
clock = pygame.time.Clock() #clock to track time
stack = [] #empty stack
state = "Cover_Page" #initial visualization state


#title font and text
title_font = pygame.font.Font('/Users/ompatel/Downloads/Fira_Code/static/FiraCode-Regular.ttf', 40)
title = title_font.render('DFS MAZE GENERATION VISUALIZER', True, (255, 125, 138))
title_rect = title.get_rect(center=(500, 75))

#slider to adjust speed of visualization using pygame gui
slider_rect = pygame.Rect((327,200), (350,60))
manager = pygame_gui.UIManager((screen_width, screen_height))
slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(slider_rect,
                                                                     start_value=30,
                                                                     value_range=(30, 300),
                                                                     visible= 1)
#value the current slider is at
slider_value_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((675, 215), (50, 30)),
                                                 text=str(slider.get_current_value()))

#slider header "SPEED" label
slider_header = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((430, 155), (150, 50)),
                                                 text= 'SPEED')

#creator tag label
creator_tag = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((-25, 0), (200, 50)),
                                                 text= 'CREATOR: OM PATEL')

#basic screen creation
screen = pygame.display.set_mode((screen_width, screen_height)) #init the game screen
pygame.display.set_caption("DFS") #set caption

#buttons to begin visualization or quit the application
visualize_button_rect = pygame.Rect((255, 300),(500, 100))
visualize_button = pygame_gui.elements.UIButton(visualize_button_rect,
                                      text='VISUALIZE')

quit_button_rect = pygame.Rect((381, 400),(250, 70))
quit_button = pygame_gui.elements.UIButton(quit_button_rect,
                                      text='QUIT')

#create a UI manager to utilize pygame gui
ui_manager = pygame_gui.UIManager(screen_size)

#sets the first instance of the current cell to index zero of the gridded maze
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]

run = True  #run variable for game loop
while run:  #main game run loop
    screen.fill((100,68,124)) #BG
    if state == "Cover_Page":

        screen.blit(title, title_rect)
        pygame.draw.rect(screen, (0, 0, 0), visualize_button_rect)

        #enabling the Ui and the buttons for pygame gui
        manager.draw_ui(screen)
        slider.enable()
        slider_value_label.set_text(str(slider.get_current_value()))
        FPS = slider.get_current_value()

        #gridded cells, and setting current_cell to be first
        grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
        current_cell = grid_cells[0]
        stack = []

    if state == "Visualize":
        #check if they are all visited and current position is at the inital one
        all_visited = all(cell.visited for cell in grid_cells)
        if all_visited == True and current_cell == grid_cells[0]:
            #if true, reset the state to the cover page
            FPS = 30
            state = "Cover_Page"
        screen.fill((88, 73, 86)) #BG
        [cell.draw() for cell in grid_cells] #drawing the grid of the maze on the screen
        current_cell.visited = True #marks the current_cell as visited
        current_cell.current_cell() #current cell is highlighted on maze
        next_cell = current_cell.check_neighbors() #determine the next cell to visit
        if next_cell: #if there is an unvisited neighboring cell remaining
            stack.append(current_cell) #current cell pushed to stack
            next_cell.visited = True #next cell is now visited
            remove_walls(current_cell, next_cell) #remove walls between current and next
            current_cell = next_cell #the current cell is now the next cell
        elif stack: #if there is no valid neighboring cells
            current_cell = stack.pop() #pop the top cell of the stack (allows to go back and uncover other unvisited cells)
        pygame.display.flip()

    for event in pygame.event.get(): #event handler
        if event.type == pygame.QUIT:
            run = False
        manager.process_events(event) #pygame gui handler
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == visualize_button:
                state = "Visualize"
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == quit_button:
               run = False

    delta_time = clock.tick(FPS) / 1000.0 #time between frames
    manager.update(delta_time) #updates gui manager
    pygame.display.flip() #updates display

pygame.quit()
