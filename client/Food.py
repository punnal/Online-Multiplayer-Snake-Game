from constants import MAX_Y, MAX_X
from random import randint

class Food:

    #initilizing
    def __init__(self, window, x, y):
        self.window = window
        self.x = x
        self.y = y
        self.fruit = '@'

    #rendering fruit
    def render(self, x , y):
        self.x = x
        self.y = y
        self.window.addstr(self.y, self.x, self.fruit)

