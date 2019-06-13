# Importing stuff
from constants import SNAKE_X, SNAKE_Y, INIT_SNAKE_LENGHT, MAX_X, MAX_Y
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
from copy import deepcopy
from random import randint

class Snake:
    # Initilizing
    def __init__(self, n):
        self.snakeBody = []
        self.length = INIT_SNAKE_LENGHT
        self.direction = KEY_RIGHT
        self.head = 'o'
        self.tail = '+'
        self.x = randint(INIT_SNAKE_LENGHT, MAX_X - INIT_SNAKE_LENGHT)
        self.y = randint(INIT_SNAKE_LENGHT, MAX_Y - INIT_SNAKE_LENGHT)
        self.snakeBody.append([self.head, self.x, self.y])
        for i in range(self.length):
            self.snakeBody.append([self.tail, self.x-i, self.y])
        # Reverse movment dictionary
        self.rev = {
        KEY_RIGHT: KEY_LEFT,
        KEY_LEFT:KEY_RIGHT,
        KEY_DOWN: KEY_UP,
        KEY_UP: KEY_DOWN}    
    
    # get snake body
    def getBody(self):
        return self.snakeBody

    # Changing snake direction
    def changeDir(self, dir):
        if (self.rev.get(self.direction) == dir):
            return
        else:
            self.direction = dir

    # Checks if snake has eaten food
    def eaten(self, x, y):
        if(self.snakeBody[0][1] == x and self.snakeBody[0][2] == y ):
            return True
        else:
            return False

    # Increase size of tail by 1
    def grow(self):
        self.length += 1
        self.snakeBody.append([self.tail, 0, 0])

    # Helper function. change cordinates of entire snake according to input
    def moveSnake(self, change_x, change_y):
        #dealing with body
        for i in range(1, self.length+1):
            self.snakeBody[-1*i][2] = self.snakeBody[(-1*i)-1][2]
            self.snakeBody[-1*i][1] = self.snakeBody[(-1*i)-1][1]
        
        #dealing with head
        self.snakeBody[0][2] = self.snakeBody[0][2] + change_y
        self.snakeBody[0][1] = self.snakeBody[0][1] + change_x 

    # updating snake with time. ie moving it
    def updateSnake(self):
        if self.direction == KEY_UP:
            self.moveSnake(0, -1)
        elif self.direction == KEY_DOWN:
            self.moveSnake(0, 1)
        elif self.direction == KEY_RIGHT:
            self.moveSnake(1, 0)
        elif self.direction == KEY_LEFT:
            self.moveSnake(-1, 0)
    
    # Checking if snake is dead 
    def isDead(self, bodies):
        cbodies = deepcopy(bodies)
        cbodies.remove(self.snakeBody)
        #case where snake hit itself
        self.snakeBody[0][0] = self.tail
        if self.snakeBody[0] in self.snakeBody[1:]:
            return True
        #case if snake hit another snake
        for body in cbodies:
            if [] != body:
                body[0][0] = self.tail
                if(self.snakeBody[0] in body):
                    return True

        #case where snake hit the wall
        if self.snakeBody[0][1] == 0 or self.snakeBody[0][1] == MAX_X+1 or self.snakeBody[0][2] == 0 or self.snakeBody[0][2] == MAX_Y+1:
            return True
        
        else:
            self.snakeBody[0][0] = self.head
            return False
