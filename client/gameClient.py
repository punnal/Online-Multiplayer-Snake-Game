#importing stuff
import json
import sys
import threading
import socket
import curses
import Food
import Snake
from constants import HEIGHT, WIDTH, TIMEOUT
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP

class GameClient():
    #initilizing
    def __init__(self):
       # try:
            address = sys.argv[1]
            port = int(sys.argv[2])
            self.event = KEY_RIGHT
            self.dir = "right"
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    self.sock.connect((address, port))
            self.rdata = json.loads(str(self.sock.recv(2048)))
	    self.id = self.rdata["id"]
	    self.data = self.rdata["data"]	
            self.totalSnakes = len(self.data["snakes"])
            curses.initscr()
            self.score = 0;
            self.window = curses.newwin(HEIGHT, WIDTH, 0, 0)
            self.window.timeout(TIMEOUT)
            self.window.keypad(1)
            curses.noecho()
            curses.curs_set(0)
            self.window.border(0)
            self.snakes = []
            for i in range(0, self.totalSnakes):
                self.snakes.append(Snake.Snake(self.window, self.data["snakes"][i]))
            self.food = Food.Food(self.window, self.data["food"][0], self.data["food"][1])
        #except Exception as e:
        #    curses.endwin()
        #    print(e)
        #    exit()
            
    def recieveHandler(self):
        while True:
            self.data = json.loads(self.sock.recv(2048))
            if(self.data["dead"][self.id] == True or self.data["win"] == 1):
                break
    
    #Method to play game
    def play(self):
        #Game Loop
        cThread = threading.Thread(target = self.recieveHandler)
        cThread.daemon = True
        cThread.start()

        #try:
        while True:  
                #rendering
                self.window.clear()
                self.window.border(0)
                self.window.addstr(0, 5, "Score: {}" .format(self.data["scores"][self.id]))
                for i in range(0, self.totalSnakes):
                    self.snakes[i].render(self.data["snakes"][i])
                self.food.render(self.data["food"][0], self.data["food"][1])
            
                #taking Input
                self.event = self.window.getch()
                #sending input
                if self.event == KEY_UP:
                    self.dir = "up"
                if self.event == KEY_DOWN:
                    self.dir = "down"
                if self.event == KEY_LEFT:
                    self.dir = "left"
                if self.event == KEY_RIGHT:
                    self.dir = "right"
                if self.event == 27:
                    self.dir = "q"
                #sending direction
                self.sock.send(self.dir)
                if(self.data["dead"][self.id] == True or self.data["win"] == 1):
                    break
        curses.endwin()
	self.sock.close()
        if(self.data["win"] == 1):
            print("----------------------------------")
            print("          You Win!!!")
            print("        Chicken dinner!")
            print("        Your score is {}".format(self.data["scores"][self.id]))
            print("----------------------------------")
        else:
            print("--------------------------------------")
            print("             Game Over")
            print("             You Loose")
            print("         Your score is {}".format(self.data["scores"][self.id]))
            print("---------------------------------------")
        #except Exception as e:
            #print(e)
            #curses.endwin()
	    #self.sock.close() 
  	


