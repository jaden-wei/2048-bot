from PIL import Image, ImageGrab
import PIL
import cv2
import numpy as np
import os
import os.path
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from Board import *
import sys


def openPage():
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get('https://play2048.co/')
    print('page opened')
    time.sleep(1)
    return driver

# takes a screenshot of the 3gameboard, saves it as a jpg


def captureScreen():
    screen = ImageGrab.grab(bbox=(569, 407, 1137, 975))
    screen = screen.save('screen.jpg', 'JPEG')


def main(argv):
    driver = openPage()

    running = True
    gameNum = 0
    totalMoves = 0
    while running:
        # create our board in the program
        board = Board()
        # capture the screen and save it into the matrix
        screen = captureScreen()
        board.getNewBoard()

        body = driver.find_element_by_xpath('/html/body')\

        # we put the depth we want in the get best move paraemeter
        # the higher this number is, the slower the program will run
        print('move number: ', totalMoves)

        start = time.time()

        if totalMoves < 400:
            body.send_keys(board.simpleGetBestMove(20))
        else:
            body.send_keys(board.getBestMove(50, 8))

        end = time.time()

        print('move took    ', end - start, ' seconds')

        totalMoves += 1
        time.sleep(0.25)

        # try again when we die lmfao
        button = driver.find_element_by_xpath(
            '/html/body/div[1]/div[3]/div[1]/div')
        if button.is_displayed():
            if button.text == 'Try again':
                totalMoves = 0
                screen = ImageGrab.grab(bbox=(569, 407, 1137, 975))
                screen = screen.save(
                    'screenshots/gameOver' + str(gameNum) + '.jpg', 'JPEG')
                gameNum += 1
            button.click()


if __name__ == '__main__':
    main(sys.argv)
