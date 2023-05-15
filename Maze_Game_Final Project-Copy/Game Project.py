from random import randrange
import time
import math
import pygame, sys
from pygame.locals import *
pygame.init()


with open("maze.txt")as f:
    contents = f.read()
contentsNew=contents.replace("\n","")
MAZE = [[contentsNew[(11*(j+1)+j)-(11-i)] for j in range(0,12)] for i in range(0,12)]
CELL=85

# Player Class
class Player:
    def __init__(self, screen):
        self.playerImg = pygame.image.load("plNew2.png")
        self.screen = screen
        self.direction = ''
        self.storedDirection = ''
        self.targetDirection = ""
        self.x = 70
        self.y = 800
        self.sourceCell = [1,10]
        self.targetCell = [1,10]
        self.speed = 2.5

    def draw(self):
        self.screen.blit(self.playerImg, (self.x, self.y))

    def moveR(self):
        self.targetDirection="right"
        responce = self.isWayClear() 
        if responce == "All free":
            self.direction = self.targetDirection
        elif responce == "Target free":
            self.storedDirection = self.targetDirection

    def moveL(self):
        self.targetDirection="left"
        responce = self.isWayClear() 
        if responce == "All free":
            self.direction = self.targetDirection
        elif responce == "Target free":
            self.storedDirection = self.targetDirection

    def moveU(self):
        self.targetDirection="up"
        responce = self.isWayClear()
        if responce == "All free":
            self.direction = self.targetDirection
        elif responce == "Target free":
            self.storedDirection = self.targetDirection

    def moveD(self):
        self.targetDirection="down"
        responce = self.isWayClear()
        if responce == "All free":
            self.direction = self.targetDirection
        elif responce == "Target free":
            self.storedDirection = self.targetDirection

    def ifInCell(self):
        if self.targetCell == self.sourceCell:
            if self.storedDirection != "":
                self.direction=self.storedDirection
                self.storedDirection = ""


    def move(self):
        if self.direction == "right":
            self.x += self.speed
        if self.direction == "left":
            self.x -= self.speed
        if self.direction == "up":
            self.y -= self.speed
        if self.direction == "down":
            self.y += self.speed
        self.draw()

    def updateGrid(self):
        if self.direction =="right":
            if self.x % 70 == 0:
                self.sourceCell[0] = int(self.x / 70)
                self.targetCell[0] = self.sourceCell[0]
            else:
                self.sourceCell[0] = math.floor(self.x/70)
                self.targetCell[0] = self.sourceCell[0] + 1
               

        elif self.direction =="left":
            if self.x % 70 == 0:
                self.sourceCell[0] = int(self.x / 70)
                self.targetCell[0] = self.sourceCell[0]
            else:
                self.sourceCell[0] = math.floor((self.x+70)/70)
                self.targetCell[0] = self.sourceCell[0] - 1
              
                
        elif self.direction =="up":
            if (self.y - 100) % 70 == 0:
                self.sourceCell[1] = int((self.y - 100) / 70)
                self.targetCell[1] = self.sourceCell[1]
            else:
                self.sourceCell[1] = math.floor((self.y - 30)/70)
                self.targetCell[1] = self.sourceCell[1] - 1
            

        elif self.direction =="down":
            if (self.y - 100)  % 70 == 0:
                self.sourceCell[1] = int((self.y - 100) / 70)
                self.targetCell[1] = self.sourceCell[1]
            else:
                self.sourceCell[1] = math.floor((self.y - 100)/70)
                self.targetCell[1] = self.sourceCell[1] + 1
            

    def isWayClear (self):
        if self.targetDirection == "right":
            if MAZE[self.sourceCell[0]+1][self.sourceCell[1]] != "x" and MAZE[self.targetCell[0]+1][self.targetCell[1]] != "x":
                return "All free"
            if MAZE[self.targetCell[0]+1][self.targetCell[1]] != 'x': 
                return "Target free" 
        elif self.targetDirection == "left":
            if MAZE[self.sourceCell[0]-1][self.sourceCell[1]] != "x" and MAZE[self.targetCell[0]-1][self.targetCell[1]] != "x":
                return "All free"
            if MAZE[self.targetCell[0]-1][self.targetCell[1]] != 'x': 
                return "Target free" 
        elif self.targetDirection == "up":
            if MAZE[self.sourceCell[0]][self.sourceCell[1]-1] != "x" and MAZE[self.targetCell[0]][self.targetCell[1]-1] != "x":
                return "All free"
            if MAZE[self.targetCell[0]][self.targetCell[1]-1] != 'x': 
                return "Target free"
        elif self.targetDirection == "down":
            if MAZE[self.sourceCell[0]][self.sourceCell[1]+1] != "x" and MAZE[self.targetCell[0]][self.targetCell[1]+1] != "x":
                return "All free"
            if MAZE[self.targetCell[0]][self.targetCell[1]+1] != 'x': 
                return "Target free" 

    def isWallAhead (self):
        if self.targetCell==self.sourceCell:
            if self.targetDirection == "right" :
                if MAZE[self.sourceCell[0]+1][self.sourceCell[1]] == 'x': 
                    self.direction=""
            if self.targetDirection == "left":
                if MAZE[self.sourceCell[0]-1][self.sourceCell[1]] == 'x':
                    self.direction="" 
            if self.targetDirection == "up":
                if MAZE[self.sourceCell[0]][self.sourceCell[1]-1] == 'x': 
                    self.direction=""
            if self.targetDirection == "down":
                if MAZE[self.sourceCell[0]][self.sourceCell[1]+1] == 'x': 
                    self.direction=""
    def boost (self):
        self.speed = 5

        pass

# Enemy Class
class Enemy:
    def __init__(self, screen, posX, posY, sourceCell, targetCell):
        self.enemyImg = pygame.image.load("enemyNew2.png")
        self.screen = screen
        self.direction = "up"
        self.sourceCell = sourceCell
        self.targetCell = targetCell
        self.y = posY
        self.x = posX
        self.speed = 2

    def draw(self):
        self.screen.blit(self.enemyImg, (self.x, self.y))

    def move(self):
        if self.direction == "right":
            self.x += self.speed
        if self.direction == "left":
            self.x -= self.speed
        if self.direction == "up":
            self.y -= self.speed
        if self.direction == "down":
            self.y += self.speed

    def updateGrid(self):
        if self.direction =="right":
            if self.x % 70 == 0:
                self.sourceCell[0] = int(self.x / 70)
                self.targetCell[0] = self.sourceCell[0]
            else:
                self.sourceCell[0] = math.floor(self.x/70)
                self.targetCell[0] = self.sourceCell[0] + 1
               

        elif self.direction =="left":

            if self.x % 70 == 0:
                self.sourceCell[0] = int(self.x / 70)
                self.targetCell[0] = self.sourceCell[0]
            else:
                self.sourceCell[0] = math.floor((self.x+70)/70)
                self.targetCell[0] = self.sourceCell[0] - 1
              
                
        elif self.direction =="up":
            if (self.y - 100) % 70 == 0:
                self.sourceCell[1] = int((self.y - 100) / 70)
                self.targetCell[1] = self.sourceCell[1]
            else:
                self.sourceCell[1] = math.floor((self.y -30)/70)
                self.targetCell[1] = self.sourceCell[1] - 1
            

        elif self.direction =="down":
            if (self.y - 100)  % 70 == 0:
                self.sourceCell[1] = int((self.y - 100) / 70)
                self.targetCell[1] = self.sourceCell[1]
            else:
                self.sourceCell[1] = math.floor((self.y - 100)/70)
                self.targetCell[1] = self.sourceCell[1] + 1

    def checkSides (self):
        freeWays=[]
        if self.targetCell == self.sourceCell:
            if self.direction == "up":
                if MAZE[self.sourceCell[0]-1][self.sourceCell[1]] != "x":
                    freeWays.append('left')
                if MAZE[self.sourceCell[0]+1][self.sourceCell[1]] != "x":
                    freeWays.append('right')
                if MAZE[self.sourceCell[0]][self.sourceCell[1]-1] != "x":
                    freeWays.append('up')

            if self.direction == "down":
                if MAZE[self.sourceCell[0]-1][self.sourceCell[1]] != "x":
                    freeWays.append('left')
                if MAZE[self.sourceCell[0]+1][self.sourceCell[1]] != "x":
                    freeWays.append('right')
                if MAZE[self.sourceCell[0]][self.sourceCell[1]+1] != "x":
                    freeWays.append('down')

            if self.direction == "left":
                if MAZE[self.sourceCell[0]][self.sourceCell[1]-1] != "x":
                    freeWays.append('up')
                if MAZE[self.sourceCell[0]][self.sourceCell[1]+1] != "x":
                    freeWays.append('down')
                if MAZE[self.sourceCell[0]-1][self.sourceCell[1]] != "x":
                    freeWays.append('left')

            if self.direction == "right":
                if MAZE[self.sourceCell[0]][self.sourceCell[1]-1] != "x":
                    freeWays.append('up')
                if MAZE[self.sourceCell[0]][self.sourceCell[1]+1] != "x":
                    freeWays.append('down')
                if MAZE[self.sourceCell[0]+1][self.sourceCell[1]] != "x":
                    freeWays.append('right')
        return freeWays 

    def desideDirection(self, freeWays):
        self.direction = freeWays[randrange(len(freeWays))]

    def atack(self):
        self.speed = 3.5
    
    def getRange(self):
        rangeR =[]
        rangeL =[]
        rangeU =[]
        rangeD =[]
        endR=False
        endL=False
        endU=False
        endD=False
        for i in range (1,5):
            if self.sourceCell[0]+i <= 11:
                if MAZE[self.sourceCell[0]+i] [self.sourceCell[1]] == "x":
                    endR = True
                if endR != True:
                    rangeR.append((self.sourceCell[0]+i, self.sourceCell[1]))

            if self.sourceCell[0]-i >= 0:
                if MAZE[self.sourceCell[0]-i] [self.sourceCell[1]] == "x":
                    endL = True
                if endL != True:
                    rangeL.append((self.sourceCell[0]-i, self.sourceCell[1]))
            if self.sourceCell[1]-i >= 0:
                if MAZE[self.sourceCell[0]] [self.sourceCell[1]-i] == "x":
                    endU = True
                if endU != True:
                    rangeU.append((self.sourceCell[0], self.sourceCell[1]-i))
            if self.sourceCell[1]+i <= 11:
                if MAZE[self.sourceCell[0]] [self.sourceCell[1]+i] == "x":
                    endD = True
                if endD != True:
                    rangeD.append((self.sourceCell[0], self.sourceCell[1]+i))    

        return rangeR, rangeL, rangeU, rangeD

    def isPlayerInRange(self, pSCell, pTCell):
        rangeR, rangeL, rangeU, rangeD = self.getRange()
        if self.targetCell == self.sourceCell:
            if tuple(pSCell) in rangeR or tuple(pTCell) in rangeR:
                self.direction='right'
                self.atack()
                return True
            else:
                self.speed = 2

            if tuple(pSCell) in rangeL or tuple(pTCell) in rangeL:
                self.direction='left'
                self.atack()
                return True
            else:
                self.speed = 2    
    
            if tuple(pSCell) in rangeU or tuple(pTCell) in rangeU:
                self.direction='up' 
                self.atack()
                return True
            else:
                self.speed = 2    
                
            if tuple(pSCell) in rangeD or tuple(pTCell) in rangeD:
                self.direction='down'
                self.atack()
                return True
            else:
                self.speed = 2

# Token Class
class Token:
    def __init__ (self, screen):
        self.screen=screen
        self.tokenImg = pygame.image.load("TokenNew2.png")
        self.cell =[0,0]
        self.y=0
        self.x=0
        self.cell, self.x, self.y = self.relocate()
    def draw(self):
        self.screen.blit(self.tokenImg, (self.x, self.y))
    def relocate (self):
        check=True
        while check:
            self.cell[0] = randrange(11)
            self.cell[1] = randrange(11)
            if MAZE[self.cell[0]][self.cell[1]] != "x" :
                self.y = (self.cell[1]*70)+100
                self.x = self.cell[0]*70
                check = False
                return self.cell, self.x, self.y 

# Game Class
class Game:
    def __init__ (self):
        self.screen = pygame.display.set_mode((840, 940))
        self.mazeImg = pygame.image.load("NewMazeImg.jpg")
        self.barImg = pygame.image.load("bar.png")
        self.menuImg = pygame.image.load("MainM.png")
        self.gOverMenu = pygame.image.load("GameOverM.png")
        self.player = Player(self.screen)
        self.player.draw()
        self.enemy1 = Enemy(self.screen, 700, 800, [10,10], [10,10])
        self.enemy1.draw()
        self.enemy2 = Enemy(self.screen, 70, 170, [1,1], [1,1])
        self.enemy2.draw()
        self.token = Token(self.screen)
        self.token.draw()
        self.playerScore = 0

    def displayScore(self):
        font = pygame.font.SysFont('Agency FB',60)
        score = font.render(f"SCORE {self.playerScore}",True,(255,0,255))
        self.screen.blit(score,(20,15))

    def game(self):
        game=True
        while game :
            self.screen.fill((19,0,43))
            self.screen.blit(self.mazeImg, (0, 100))
            self.screen.blit(self.barImg,(0,0))
            self.displayScore()
            self.token.draw()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sys.exit
                    if event.key == K_LEFT:
                        self.player.moveL()
                 
                    if event.key == K_RIGHT:
                        self.player.moveR()
                       
                    if event.key == K_UP:
                        self.player.moveU()
                       
                    if event.key == K_DOWN:
                        self.player.moveD()
                    
                elif event.type == QUIT:
                    sys.exit()
            self.run()
            if self.isCollisionE(self.player.x, self.player.y, self.enemy1.x, self.enemy1.y) == True or self.isCollisionE(self.player.x, self.player.y, self.enemy2.x, self.enemy2.y) == True:
                game = False
            time.sleep(0.001)
        self.gameOverMenu()

    def mainMenu (self):
        startButton = pygame.image.load("SButton.png")
        menu=True
        click=False
        while menu :
            self.screen.fill((19,0,43))
            self.screen.blit(self.mazeImg, (0, 100))
            self.screen.blit(self.barImg,(0,0))
            self.displayScore()
            self.screen.blit(self.menuImg,(0,0))
            self.screen.blit(startButton,(270,590))
            mx, my = pygame.mouse.get_pos()
            if (mx>=270 and mx<= 570) and (my<=710 and my>=590):
                self.screen.blit(startButton,(270,590))
                if click:
                    menu = False
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        menu = False
                if event.type == QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True 
            pygame.display.flip()
        self.game()

    def gameOverMenu (self):
        againButton = pygame.image.load("AButton.png")
        menuButton = pygame.image.load("MButton.png")
        font = pygame.font.SysFont('Agency FB',60)
        score = font.render(f"SCORE {self.playerScore}",True,(0,255,0))
        menu=True
        click=False
        while menu :
            self.screen.fill((19,0,43))
            self.screen.blit(self.mazeImg, (0, 100))
            self.screen.blit(self.barImg,(0,0))
            self.screen.blit(self.gOverMenu,(0,0))
            self.screen.blit(againButton,(460,630))
            self.screen.blit(menuButton, (80, 630))
            self.screen.blit(score,(345,790))
            mx, my = pygame.mouse.get_pos()
            if (mx>=80 and mx<= 380) and (my<=750 and my>=630):
                self.screen.blit(menuButton,(80,630))
                if click:
                    menu = False
                    distanation ="menu"
            if (mx>=460 and mx<= 760) and (my<=750 and my>=630):
                self.screen.blit(againButton,(460,630))
                if click:
                    menu = False
                    distanation ="game"
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        menu = False
                if event.type == QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True 
            pygame.display.flip()
        self.reset()
        if distanation == "menu":
            self.mainMenu()
        if distanation == "game":
            self.game()

    def run (self):
        self.player.isWallAhead()
        self.player.ifInCell()
        self.player.move()
        self.player.updateGrid()

        self.enemy1.draw()
        self.enemy2.draw()
        freeWays = self.enemy1.checkSides()
        if self.enemy1.isPlayerInRange(self.player.sourceCell, self.player.targetCell) != True:
            if len(freeWays) != 0:
                self.enemy1.desideDirection(freeWays)
        self.enemy1.move()
        self.enemy1.updateGrid()

        freeWays = self.enemy2.checkSides()
        if self.enemy2.isPlayerInRange(self.player.sourceCell, self.player.targetCell) != True:
            if len(freeWays) != 0:
                self.enemy2.desideDirection(freeWays)
        self.enemy2.move()
        self.enemy2.updateGrid()

        if self.isCollisionT(self.player.x, self.player.y, self.token.x, self.token.y) == True:
            self.playerScore+=1
            self.token.relocate()
            self.token.draw()
        pygame.display.flip()

    def isCollisionT(self, xP, yP, xT, yT):
        if xP >= xT - 35 and xP < xT + 35:
            if yP >= yT - 35 and yP < yT + 35:
                return True

    def isCollisionE(self, xP, yP, xE, yE):
        if xP >= xE -15 and xP < xE + 15:
            if yP >= yE - 15 and yP < yE + 15:
                return True

    def reset(self):
        self.player.x=70
        self.player.y=800
        self.player.sourceCell=[1,10]
        self.player.targetCell=[1,10]
        self.player.direction = ""
        self.player.storedDirection = ""
        self.player.targetDirection = ""

        self.enemy1.x=700
        self.enemy1.y=800
        self.enemy1.sourceCell=[10,10]
        self.enemy1.targetCell=[10,10]

        self.enemy2.x=70
        self.enemy2.y=170
        self.enemy2.sourceCell=[1,1]
        self.enemy2.targetCell=[1,1]

        self.token.cell, self.token.x, self.token.y = self.token.relocate()
        self.playerScore = 0


game=Game()
game.mainMenu()