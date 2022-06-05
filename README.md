# 2048-bot

This program opens a Chrome browser with https://play2048.co/ and sends the best moves. The script usually hits the 2048 tile with occasionaly 4096 tiles. Chromedriver must be set up properly for the program to run. This link may help with the setup https://blog.testproject.io/2019/07/16/installing-selenium-webdriver-using-python-chrome/.

### Main.py

This file holds the main loop for the program. It handles opening the browser and sending the best moves through Selenium and Chromedriver. Within the loop, we take screenshots and update our board in each move with funcitons in Board.py.

### Board.py

This file holds the functions for parsing our board from a screenshot, the logics of the game, as well as our algorithm for finding the best move.

Here is a video where I demo the program: **https://www.youtube.com/watch?v=FQzfe-a-pUY**
