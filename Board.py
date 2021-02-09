import numpy as np
from PIL import Image, ImageGrab
import PIL
import random
from copy import copy, deepcopy

class Board:
    def __init__(self):
        self.boardArr = np.zeros((4, 4))
    
    def getNewBoard(self):
        boardscreenshot = Image.open('screenshots\screen.jpg')
        self.boardArr[0][0] = self.getTileVal(boardscreenshot.getpixel((30, 30)))
        self.boardArr[0][1] = self.getTileVal(boardscreenshot.getpixel((167, 30)))
        self.boardArr[0][2] = self.getTileVal(boardscreenshot.getpixel((306, 30)))
        self.boardArr[0][3] = self.getTileVal(boardscreenshot.getpixel((440, 30)))

        self.boardArr[1][0] = self.getTileVal(boardscreenshot.getpixel((30, 166)))
        self.boardArr[1][1] = self.getTileVal(boardscreenshot.getpixel((166, 166)))
        self.boardArr[1][2] = self.getTileVal(boardscreenshot.getpixel((306, 166)))
        self.boardArr[1][3] = self.getTileVal(boardscreenshot.getpixel((440, 166)))

        self.boardArr[2][0] = self.getTileVal(boardscreenshot.getpixel((30, 305)))
        self.boardArr[2][1] = self.getTileVal(boardscreenshot.getpixel((166, 305)))
        self.boardArr[2][2] = self.getTileVal(boardscreenshot.getpixel((306, 305)))
        self.boardArr[2][3] = self.getTileVal(boardscreenshot.getpixel((440, 305)))

        self.boardArr[3][0] = self.getTileVal(boardscreenshot.getpixel((30, 444)))
        self.boardArr[3][1] = self.getTileVal(boardscreenshot.getpixel((166, 444)))
        self.boardArr[3][2] = self.getTileVal(boardscreenshot.getpixel((306, 444)))
        self.boardArr[3][3] = self.getTileVal(boardscreenshot.getpixel((440, 444)))

    def getTileVal(self, rgb_val):
        if self.isCloseTo(rgb_val,(205, 193, 179)):
            return 0
        elif self.isCloseTo(rgb_val,(238, 228, 218)):
            return 2
        elif self.isCloseTo(rgb_val, (237, 225, 203)):
            return 4
        elif self.isCloseTo(rgb_val, (243, 178, 122)):
            return 8
        elif self.isCloseTo(rgb_val, (247, 149, 100)):
            return 16
        elif self.isCloseTo(rgb_val, (247, 124, 95)):
            return 32
        elif self.isCloseTo(rgb_val, (247, 95, 59)):
            return 64
        elif self.isCloseTo(rgb_val, (237, 208, 115)):
            return 128
        elif self.isCloseTo(rgb_val, (237, 204, 98)):
            return 256
        elif self.isCloseTo(rgb_val, (237, 201, 80)):
            return 512
        elif self.isCloseTo(rgb_val, (237, 197, 63)):
            return 1024
        elif self.isCloseTo(rgb_val, (237, 194, 46)):
            return 2048
        else: return -1

    def isCloseTo(self, rgb_val, target_val):
        if rgb_val[0] < target_val[0] - 5 or rgb_val[0] > target_val[0] + 5:
            return False
        if rgb_val[1] < target_val[1] - 5 or rgb_val[1] > target_val[1] + 5:
            return False
        if rgb_val[2] < target_val[2] - 5 or rgb_val[2] > target_val[2] + 5:
            return False
        return True
    
    #each time the board changes, we need to spawn a new square
    def spawnNewSquare(self):
        #90% chance new num is 2, 10% chance new num is 4
        newVal = 2
        if random.randint(0, 10) == 0:
            newVal = 4
        #randomize spawn location
        #of course, we don't want to spawn it in a square that already contains a value
        r = random.randint(0, 3)
        c = random.randint(0, 3)
        while (self.boardArr[r][c] != 0):
            r = random.randint(0, 3)
            c = random.randint(0, 3)
        self.boardArr[r][c] = newVal

    #write the code for the input keys up down left right
    def moveUp(self):
        #we only spawn a new square if the board changes, so we'll make a copy to check that
        copy = deepcopy(self.boardArr)
        score = 0

        for col in range(4):
            #merge
            #only one possibility where we have two tile merges
            if self.boardArr[0][col] == self.boardArr[1][col] and self.boardArr[2][col] == self.boardArr[3][col]:
                self.boardArr[0][col] *= 2
                self.boardArr[1][col] = 0
                self.boardArr[2][col] *= 2
                self.boardArr[3][col] = 0
                score += self.boardArr[0][col] + self.boardArr[2][col]
            #when there's only one tile merge, we can keep track of the most recent non-zero tile and then check if it matches the next one
            else:
                prevRow = 0
                for row in range(1, 4):
                    if (self.boardArr[row][col] != 0):
                        if (self.boardArr[row][col] == self.boardArr[prevRow][col]):
                            self.boardArr[prevRow][col] *= 2
                            self.boardArr[row][col] = 0
                            score += self.boardArr[prevRow][col]
                            break
                        prevRow = row

            #move everything in place
            #we keep track of the first tile with value zero, and we exchange it with the next non-zero tile
            rowWithZero = -1
            if self.boardArr[0][col] == 0:
                rowWithZero = 0
            for row in range(1,4,1):
                if self.boardArr[row][col] == 0 and rowWithZero == -1:
                    rowWithZero = row
                if self.boardArr[row][col] != 0 and rowWithZero != -1:
                    self.boardArr[rowWithZero][col] = self.boardArr[row][col]
                    self.boardArr[row][col] = 0
                    rowWithZero = rowWithZero + 1

        if (self.boardArr != copy).all():
            self.spawnNewSquare()
        return score

    def moveDown(self):
        #we can just flip the board, move it up, then flip it again
        #this uses mroe time, but I'm lazy and this is less code lol
        self.boardArr = np.flipud(self.boardArr)
        score = self.moveUp()
        self.boardArr = np.flipud(self.boardArr)
        return score

    def moveLeft(self):
        #we can rotate the board clockwise, move up, then rotate the board back
        self.boardArr = np.rot90(self.boardArr, 3)
        score = self.moveUp()
        self.boardArr = np.rot90(self.boardArr, 1)
        return score

    def moveRight(self):
        #we can rotate the board CCW, move up, then rotate the board back
        self.boardArr = np.rot90(self.boardArr, 1)
        score = self.moveUp()
        self.boardArr = np.rot90(self.boardArr, 3)
        return score

    def move(self, m):
        if m == 'w':
           return  self.moveUp()
        if m == 'a':
           return self.moveLeft()
        if m == 's':
            return self.moveDown() 
        if m == 'd':
            return self.moveRight()
        

    def findBestMove(self):
        """ print('up: ', self.moveUp())
        print('down: ', self.moveDown())
        print('left: ', self.moveLeft())
        print('right: ', self.moveRight()) """
        #we stored the score of each move as the total of the values of the tiles that were merged
        #for this generation, we are finding the move that combines the most tiles and the highest value tiles
        """ if max(self.moveUp(False), self.moveDown(False), self.moveLeft(False), self.moveRight(False)) == self.moveUp():
            self = self.moveUp()
            return 'w'
        elif max(self.moveUp(), self.moveDown(), self.moveLeft(), self.moveRight()) == self.moveDown():
            self = self.moveDown()
            return 's'
        elif max(self.moveUp(), self.moveDown(), self.moveLeft(), self.moveRight()) == self.moveLeft():
            self = self.moveLeft()
            return 'a'
        else: 
            self = self.moveRight()
            return 'd' """
        
        #this generation goes 2 moves into the future, making the most and highest tile merges as possible
        copy = deepcopy(self.boardArr)
        moves = ['w', 'a', 's', 'd']
        maxScore = 0
        bestMove = moves[random.randint(0, 3)]

        for move1 in moves:
            for move2 in moves:
                for move3 in moves:
                    for move4 in moves:
                        score = 0
                        score = self.move(move1) * 1.75
                        score += self.move(move2) * 1.5
                        score += self.move(move3) * 1.25
                        score += self.move(move4)

                        #print (move1, ' ', move2, ' ', score)
                        if score > maxScore:
                            bestMove = move1
                            maxScore = score
                        self.boardArr = deepcopy(copy)
        print('best move: ', bestMove)
        return bestMove

""" board = Board()
board.getNewBoard()
print(board.boardArr)
print(board.findBestMove()) """