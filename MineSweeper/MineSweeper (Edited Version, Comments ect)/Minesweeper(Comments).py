#Grid Size   X
#Guarantee Safe Zone
#Modidy Sprites?
#Restart at any time
#Reveal one flag 

import pygame
import random
pygame.init()

bg_color = (192, 192, 192)#Generate colour of the background
grid_color = (128, 128, 128)#Generate colour of the grid

#Variable for the width and height of the grid 
game_width = 10  # Change this to increase size
game_height = 10  # Change this to increase size

#The number of mines that are hidden in the grid
numMine = 9  # Number of mines
#Size of the grid
grid_size = 32  # Size of grid (WARNING: macke sure to change the images dimension as well)

#Sizes of border of the window
border = 16  # Top border
top_border = 100  # Left, Right, Bottom border
#Sizes of the windows
display_width = grid_size * game_width + border * 2  # Display width
display_height = grid_size * game_height + border + top_border  # Display height
#Create the game window
gameDisplay = pygame.display.set_mode((display_width, display_height))  # Create display
#Create a timer for the game
timer = pygame.time.Clock()  # Create timer
#Set the name of the window to "Minesweeper"
pygame.display.set_caption("Minesweeper")  # S Set the caption of window

# Import files
#Import the Image files from the Sprite Folder
spr_emptyGrid = pygame.image.load("Sprites/empty.png")
spr_flag = pygame.image.load("Sprites/flag.png")
spr_grid = pygame.image.load("Sprites/Grid.png")
spr_grid1 = pygame.image.load("Sprites/grid1.png")
spr_grid2 = pygame.image.load("Sprites/grid2.png")
spr_grid3 = pygame.image.load("Sprites/grid3.png")
spr_grid4 = pygame.image.load("Sprites/grid4.png")
spr_grid5 = pygame.image.load("Sprites/grid5.png")
spr_grid6 = pygame.image.load("Sprites/grid6.png")
spr_grid7 = pygame.image.load("Sprites/grid7.png")
spr_grid8 = pygame.image.load("Sprites/grid8.png")
spr_grid7 = pygame.image.load("Sprites/grid7.png")
spr_mine = pygame.image.load("Sprites/mine.png")
spr_mineClicked = pygame.image.load("Sprites/mineClicked.png")
spr_mineFalse = pygame.image.load("Sprites/mineFalse.png")


# Create global values 
#Create the matrices for the grid and the mine positions on said grid
grid = []  # The main grid
mines = []  # Pos of the mines


# Create funtion to draw texts

def drawText(txt, s, yOff=0):
    #Create a font for the game
    screen_text = pygame.font.SysFont("Calibri", s, True).render(txt, True, (0, 0, 0))
    #Create a rectangle for the text
    rect = screen_text.get_rect()
    #Generate the size of the rectangle
    rect.center = (game_width * grid_size / 2 + border, game_height * grid_size / 2 + top_border + yOff)
    #Display the text
    gameDisplay.blit(screen_text, rect)


# Create class grid
class Grid:
    #Initialize the creation of the grid
    def __init__(self, xGrid, yGrid, type):
        
        #Initialize the minesweeper grid and all it's values (posx, posy, clicked, mine ect)
        self.xGrid = xGrid  # X pos of grid
        self.yGrid = yGrid  # Y pos of grid
        self.clicked = False  # Boolean var to check if the grid has been clicked
        self.mineClicked = False  # Bool var to check if the grid is clicked and its a mine
        self.mineFalse = False  # Bool var to check if the player flagged the wrong grid
        self.flag = False  # Bool var to check if player flagged the grid
        # Create rectObject to handle drawing and collisions
        self.rect = pygame.Rect(border + self.xGrid * grid_size, top_border + self.yGrid * grid_size, grid_size, grid_size)
        self.val = type  # Value of the grid, -1 is mine

    def drawGrid(self):
        # Draw the grid according to bool variables and value of grid
        #Check if the space is mineFalse (not a mine but flagged as one) (Only appears at the end of the game)
        if self.mineFalse:
            #Draw the "tile" as a mineFalse sprite
            gameDisplay.blit(spr_mineFalse, self.rect)
        else:
            #Check if the "tile" has been clicked
            if self.clicked:
                #Check if the "tile" is a mine
                if self.val == -1:
                    #Check if the "tile" has been clicked (as a mine)
                    if self.mineClicked:
                        #Draw the "tile" as a mine that have been clicked
                        gameDisplay.blit(spr_mineClicked, self.rect)
                    else:
                        #Draw the "tile" as a mine (revealed once game is over)
                        gameDisplay.blit(spr_mine, self.rect)
                else:
                    #Check the value of the "tile" (corresponds to number of mines around it) and display the image with number (once clicked)
                    if self.val == 0:
                        gameDisplay.blit(spr_emptyGrid, self.rect)
                    elif self.val == 1:
                        gameDisplay.blit(spr_grid1, self.rect)
                    elif self.val == 2:
                        gameDisplay.blit(spr_grid2, self.rect)
                    elif self.val == 3:
                        gameDisplay.blit(spr_grid3, self.rect)
                    elif self.val == 4:
                        gameDisplay.blit(spr_grid4, self.rect)
                    elif self.val == 5:
                        gameDisplay.blit(spr_grid5, self.rect)
                    elif self.val == 6:
                        gameDisplay.blit(spr_grid6, self.rect)
                    elif self.val == 7:
                        gameDisplay.blit(spr_grid7, self.rect)
                    elif self.val == 8:
                        gameDisplay.blit(spr_grid8, self.rect)

            else:
                #Check if the player has flagged the "tile"
                if self.flag:\
                    #Draw the "tile" as a flag (once flagged)
                    gameDisplay.blit(spr_flag, self.rect)
                else:
                    #Draw the "tile" (not revealed) 
                    gameDisplay.blit(spr_grid, self.rect)

#Once the game is lost it reveals the bombs and and empty tiles(With no number)
    def revealGrid(self): 
        #Make the "tiles" value clicked (revealed)
        self.clicked = True
        #Auto reveal if it's a 0
        #Check if the value of the "tile" clicked is 0
        if self.val == 0:
            for x in range(-1, 2):
                #Check if the "tiles" beside the one clicked are valid game "tiles" on the x axis(not below 0 or more than the width/not out of the map)
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                         #Check if the "tiles" beside the one clicked are valid game "tiles" on the y axis(not below 0 or more than the width/not out of the map)
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            #Check if the grid beside it has been clicked 
                            if not grid[self.yGrid + y][self.xGrid + x].clicked:
                                #Recursive function to check if the "tiles" beside it are revealed and or are equal to 0
                                grid[self.yGrid + y][self.xGrid + x].revealGrid()
        #Check if the "tile" is a mine
        elif self.val == -1:
            # Auto reveal all mines if it's a mine
            for m in mines:     
                #Verify if the "tiles" with mines on them have not been clicked/revealed
                if not grid[m[1]][m[0]].clicked:
                    #Recursive function to reveal all the mines on the board
                    grid[m[1]][m[0]].revealGrid()
    #Initialize the function that assigns the "tile" value
    def updateValue(self):
        # Update the value when all grid is generated
        #Check if the "tile" is not a mine
        if self.val != -1:
            #Look around the "tile" and count the number of mines around it and assign that value to it 
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if grid[self.yGrid + y][self.xGrid + x].val == -1:
                                self.val += 1

#Initialize the function for the game loop (Game startup)
def gameLoop():
    gameState = "Playing"  # Game state
    mineLeft = numMine  # Number of mine left
    global grid  # Access global var
    grid = []
    global mines
    t = 0  # Set time to 0

    # Generating mines
    mines = [[random.randrange(0, game_width),
              random.randrange(0, game_height)]]

    for c in range(numMine - 1):
        pos = [random.randrange(0, game_width),
               random.randrange(0, game_height)]
        same = True
        while same:
            for i in range(len(mines)):
                if pos == mines[i]:
                    pos = [random.randrange(0, game_width), random.randrange(0, game_height)]
                    break
                if i == len(mines) - 1:
                    same = False
        mines.append(pos)

    # Generating entire grid
    for j in range(game_height):
        line = []
        for i in range(game_width):
            if [i, j] in mines:
                line.append(Grid(i, j, -1))
            else:
                line.append(Grid(i, j, 0))
        grid.append(line)

    # Update of the grid
    for i in grid:
        for j in i:
            j.updateValue()

    # Main Loop
    while gameState != "Exit":
        # Reset screen
        gameDisplay.fill(bg_color)

        # User inputs
        for event in pygame.event.get():
            # Check if player close window
            if event.type == pygame.QUIT:
                gameState = "Exit"
            # Check if play restart
            if gameState == "Game Over" or gameState == "Win":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        gameLoop()
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    for i in grid:
                        for j in i:
                            if j.rect.collidepoint(event.pos):
                                if event.button == 1:
                                    # If player left clicked of the grid
                                    j.revealGrid()
                                    # Toggle flag off
                                    if j.flag:
                                        mineLeft += 1
                                        j.falg = False
                                    # If it's a mine
                                    if j.val == -1:
                                        gameState = "Game Over"
                                        j.mineClicked = True
                                elif event.button == 3:
                                    # If the player right clicked
                                    if not j.clicked:
                                        if j.flag:
                                            j.flag = False
                                            mineLeft += 1
                                        else:
                                            j.flag = True
                                            mineLeft -= 1

        # Check if won
        w = True
        for i in grid:
            for j in i:
                j.drawGrid()
                if j.val != -1 and not j.clicked:
                    w = False
        if w and gameState != "Exit":
            gameState = "Win"

        # Draw Texts
        if gameState != "Game Over" and gameState != "Win":
            t += 1
        elif gameState == "Game Over":
            drawText("Game Over!", 50)
            drawText("R to restart", 35, 50)
            for i in grid:
                for j in i:
                    if j.flag and j.val != -1:
                        j.mineFalse = True
        else:
            drawText("You WON!", 50)
            drawText("R to restart", 35, 50)
        # Draw time
        s = str(t // 15)
        screen_text = pygame.font.SysFont("Calibri", 50).render(s, True, (0, 0, 0))
        gameDisplay.blit(screen_text, (border, border))
        # Draw mine left
        screen_text = pygame.font.SysFont("Calibri", 50).render(mineLeft.__str__(), True, (0, 0, 0))
        gameDisplay.blit(screen_text, (display_width - border - 50, border))

        pygame.display.update()  # Update screen

        timer.tick(15)  # Tick fps


gameLoop()
pygame.quit()
quit()
