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

PATH = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(PATH)
driver.get('https://play2048.co/')
print('page opened')
time.sleep(1)

def captureScreen():
    screen = ImageGrab.grab(bbox = (569, 407, 1137, 975))
    screen = screen.save('screenshots/screen.jpg', 'JPEG')

""" def setPreviousState():
    if os.path.exists('screenshots\prev_screen.jpg'):
        os.remove('screenshots\prev_screen.jpg')
    os.rename('screenshots\screen.jpg', 'screenshots\prev_screen.jpg') """

""" def noChange():
    img1 = cv2.imread('screenshots\prev_screen.jpg')
    img2 = cv2.imread('screenshots\screen.jpg')
    difference = cv2.subtract(img1, img2)
    if not np.any(difference):
        return True
    return False """

def main():
    running = True
    gameNum = 0
    while running:
        #create our board in the program
        board = Board()
        #capture the screen and save it into the matrix
        screen = captureScreen()
        board.getNewBoard()


        body = driver.find_element_by_xpath('/html/body')\
    
        body.send_keys(board.findBestMove())
        time.sleep(0.3)

        #try again when we die lmfao
        button = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div')
        if button.is_displayed():
            screen = ImageGrab.grab(bbox = (569, 407, 1137, 975))
            screen = screen.save('screenshots/gameOver' + str(gameNum) + '.jpg', 'JPEG')
            gameNum += 1
            button.click()
        
        

if __name__ == '__main__':
    main()






