#importing stuff
import json
import sys
import time
import threading
import socket
import Food
import Snake
from constants import HEIGHT, WIDTH, TIMEOUT
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP


class GameManager:
    #initializing
    def __init__(self):
        try:
            address = sys.argv[1]
            port = int(sys.argv[2])
            self.event = KEY_RIGHT
            self.dir = "right"
            self.totalSnakes = int(sys.argv[3])
            self.connections = []
            self.addresses = []
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((address, port))
            self.sock.listen(1)
            self.snakes = []
            self.data = {"win": 0, "dead": [], "snakes": [], "food": [], "scores": [],}
            for i in range(0, self.totalSnakes):
                self.snakes.append(Snake.Snake(i+i))
                self.data["scores"].append(0)
                self.data["dead"].append(False)
                self.data["snakes"].append(self.snakes[i].getBody())
            self.food = Food.Food()
            self.data["food"] = self.food.getCor()

        except Exception as e:
            print(e)
            self.sock.close()
            exit()

    def clientThread(self, c, a, i):
        try:
            while(True):
                #checking if snake is dead
                if(self.data["dead"][i] == True):
                    self.connections.remove(c)
                    print(str(a[0]) + ':' + str(a[1]) + ' Eliminated')
                    c.close()
                    break
                if(self.data["win"] == 1):
                    self.connections.remove(c)
                    print(str(a[0]) + ':' + str(a[1]) + ' Won!!!!!')
                    c.close()
                    break
                #taking Input
                #print("Recieving input from client {}: {}".format(i, a[1]))
                try:
                    self.dir = c.recv(1024)
                except:
                    self.connections.remove(c)
                    print(str(a[0]) + ':' + str(a[1]) + ' disconnected')
                    c.close()
                    break
                if self.dir == "up":
                    self.event = KEY_UP
                if self.dir == "down":
                    self.event = KEY_DOWN
                if self.dir == "left":
                    self.event = KEY_LEFT
                if self.dir == "right":
                    self.event = KEY_RIGHT
                if self.dir == "q":
                    self.event = 27
                #print("recieved {}".format(self.event))
                #handling input
                if self.event == 27:
                    self.data["dead"][i] = True
                    break
                elif self.event in [KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP]:
                    self.snakes[i].changeDir(self.event)

                
        except Exception as e:
            print(e)
            print(self.data)
            self.sock.close()


    #Method to play game
    def play(self):
        print("waiting for snakes")
        while(self.totalSnakes != len(self.connections)):
            c, a = self.sock.accept()   
            self.connections.append(c)
            self.addresses.append(a)
            print(str(a[0]) + ':' + str(a[1]) + ' connected')
        for i in range(0, self.totalSnakes):
            print("sending initial info to client {}".format(i) )
            self.connections[i].send(bytes(json.dumps({"id": i, "data": self.data})))
            cThread = threading.Thread(target = self.clientThread, args = (self.connections[i], self.addresses[i], i))
            cThread.daemon = True
            cThread.start()

        #Game Loop
        try:
            while True:  
                for i in range(0, self.totalSnakes):
                    if(self.data["dead"][i] == False):
                        #checking if eaten food
                        if(self.snakes[i].eaten(self.food.x, self.food.y)):
                            self.snakes[i].grow()
                            self.food.update()
                            self.data["scores"][i] += 1

                        #updating snake
                        self.snakes[i].updateSnake()  
                    
                        #updating data
                        self.data["snakes"][i] = self.snakes[i].getBody()
                        self.data["food"] = self.food.getCor()
                        #checking if snake is dead
                for i in range(0, self.totalSnakes):
                    if(self.data["dead"][i] == False):
                        if(self.snakes[i].isDead(self.data['snakes'])):
                            self.data['dead'][i] = True
                        if(len(self.connections) == 1):
                            self.data['win'] = 1

                for i in range(0, self.totalSnakes):
                    if(self.data["dead"][i] == True):
                        self.data['snakes'][i] = []
                for c in self.connections:
                    #sending data
                    #print("Sending Data to client")
                    c.send(json.dumps(self.data)) 
                if(len(self.connections) == 0):
                    break
                time.sleep(1)
            self.sock.close()
            self.gameOver()
        except Exception as e:
            self.sock.close()
            print(e)
        
        

    def gameOver(self):
        print "Game Over\n"


