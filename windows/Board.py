import numpy as np
from PIL import Image, ImageGrab
import PIL
import random
from copy import copy, deepcopy
import math
import multiprocessing

class Board:
    def __init__(self):
        self.boardArr = np.zeros((4, 4))
    
    def getNewBoard(self):
        boardscreenshot = Image.open('screen.jpg')
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
        elif self.isCloseTo(rgb_val, (60,58,51)):
            return 4096
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
        change = False
        for col in range(4):
            #merge
            #only one possibility where we have two tile merges
            if self.boardArr[0][col] == self.boardArr[1][col] and self.boardArr[2][col] == self.boardArr[3][col]:
                change = True
                self.boardArr[0][col] *= 2
                self.boardArr[1][col] = 0
                self.boardArr[2][col] *= 2
                self.boardArr[3][col] = 0
            #when there's only one tile merge, we can keep track of the most recent non-zero tile and then check if it matches the next one
            else:
                prevRow = 0
                for row in range(1, 4):
                    if (self.boardArr[row][col] != 0):
                        if (self.boardArr[row][col] == self.boardArr[prevRow][col]):
                            change = True
                            self.boardArr[prevRow][col] *= 2
                            self.boardArr[row][col] = 0
                            break
                        prevRow = row
            #move everything in place
            #we keep track of the first tile with value zero, and we exchange it with the next non-zero tile
            rowWithZero = -1
            if self.boardArr[0][col] == 0:
                rowWithZero = 0
            for row in range(1,4):
                if self.boardArr[row][col] == 0 and rowWithZero == -1:
                    rowWithZero = row
                if self.boardArr[row][col] != 0 and rowWithZero != -1:
                    change = True
                    self.boardArr[rowWithZero][col] = self.boardArr[row][col]
                    self.boardArr[row][col] = 0
                    rowWithZero = rowWithZero + 1
        if change:
            self.spawnNewSquare()

    def moveDown(self):
        #we can just flip the board, move it up, then flip it again
        #this uses mroe time, but I'm lazy and this is less code lol
        self.boardArr = np.flipud(self.boardArr)
        self.moveUp()
        self.boardArr = np.flipud(self.boardArr)

    def moveLeft(self):
        #we can rotate the board clockwise, move up, then rotate the board back
        self.boardArr = np.rot90(self.boardArr, 3)
        self.moveUp()
        self.boardArr = np.rot90(self.boardArr, 1)

    def moveRight(self):
        #we can rotate the board CCW, move up, then rotate the board back
        self.boardArr = np.rot90(self.boardArr, 1)
        self.moveUp()
        self.boardArr = np.rot90(self.boardArr, 3)

    def move(self, m):
        if m == 'w':
           self.moveUp()
        elif m == 'a':
           self.moveLeft()
        elif m == 's':
            self.moveDown() 
        elif m == 'd':
            self.moveRight()
    
    #i think this should optimize it more (we'll check if the move changes and if it doesnt, we save thousands of calculations)
    def boardChanges(self, move):
        copy = deepcopy(self)
        copy.move(move)
        if (copy.boardArr == self.boardArr).all():
            return False
        return True

    #check if we have lost lol
    def stillMovesLeft(self):
        for row in range(4):
            for col in range(4):
                if (self.boardArr[row][col] == 0):
                    return True
                if (row < 3 and col < 3):
                    if (self.boardArr[row][col] == self.boardArr[row+1][col] or self.boardArr[row][col] == self.boardArr[row][col+1]):
                        return True
                if (row == 3 and col < 3):
                    if (self.boardArr[row][col] == self.boardArr[row][col+1]):
                        return True
                if (row < 3 and col == 3):
                    if (self.boardArr[row][col] == self.boardArr[row+1][col]):
                        return True
        return False

    #probably didn't need another function for this, but whatever
    def getScore(self):
        return self.boardArr.sum()

    def getAverageScore(self, depth):
        total = 0
        moves = ['w', 'a', 's', 'd']

        for i in range(depth):
            copy = deepcopy(self)
            while copy.stillMovesLeft():
                copy.move(moves[random.randint(0,3)])
            total += copy.getScore()
        return total/depth

    def getBestMove(self, depth, procNum):
        maxScore = 0
        bestMove = 'a'
        moves = ['w', 'a', 's', 'd']
        for move in moves:
            if self.boardChanges(move):
                copy = deepcopy(self)
                copy.move(str(move))
                total = 0
                pool = multiprocessing.Pool(processes=procNum)
                data = [depth] * procNum
                for num in pool.map(copy.getAverageScore, data):
                    total += num
                total /= procNum
                if total > maxScore:
                    bestMove = move
                    maxScore = total
        print('best move:   ', bestMove)
        return bestMove

    def simpleGetBestMove(self, depth):
        maxScore = 0
        bestMove = 'a'
        moves = ['w', 'a', 's', 'd']
        for move in moves:
            if self.boardChanges(move):
                copy = deepcopy(self)
                copy.move(str(move))
                avg = copy.getAverageScore(depth)
                if avg > maxScore:
                    bestMove = str(move)
                    maxScore = avg
        print('best move:   ', bestMove)
        return bestMove