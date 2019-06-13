# Importing stuff
from constants import SNAKE_X, SNAKE_Y, INIT_SNAKE_LENGHT, MAX_X, MAX_Y
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP

class Snake:
    # Initilizing
    def __init__(self, window, body):
        self.window = window
        self.snakeBody = []
        self.length = INIT_SNAKE_LENGHT
        self.direction = KEY_RIGHT
        self.head = 'o'
        self.tail = '+'
        self.snakeBody = body

    # Rendering the snake
    def render(self, body):
        self.snakeBody = body
        for i in range(0,len(self.snakeBody)):
            self.window.addstr(self.snakeBody[i][2], self.snakeBody[i][1], self.snakeBody[i][0])


