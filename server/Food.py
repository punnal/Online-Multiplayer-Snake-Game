from constants import MAX_Y, MAX_X
from random import randint

class Food:

    #initilizing
    def __init__(self):
        self.x = randint(1, MAX_X)
        self.y = randint(1, MAX_Y)
        self.fruit = '@'
    
    #get cordinates
    def getCor(self):
        return [self.x, self.y]

    #Updating food loctaion
    def update(self):
        self.x = randint(1, MAX_X)
        self.y = randint(1, MAX_Y)
