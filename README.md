# Online-Multiplayer-Snake-Game
Programmed using socket programming and threading in python

## server.py
  - Connect with all the clients
  - Start the game and spawn a snake for each player on the board
  - Communicate the positions and moves of each player to every other player
  - The command for starting the server should be as follows:
    - python3 server.py *IP address* *port* *number of players*
    - E.g python3 server.py 192.168.5.5 2000 5
    - E.g python3 server.py 127.0.0.1 2000 3

## client.py
  - Connect with the server
  - Display the board and all of the players and their positions in     real time once the game starts by receiving this information from     the server
  - The command for starting the client should be as follows:
    - python3 client.py *IP address* *port*
    - E.g python3 client.py 192.168.5.5 2000
    - E.g python3 client..py 127.0.0.1 2000
    
## Rules
1. When the game starts, all players will have a snake spawn in a     random position on the
board.
2. Each player will be able to move their snake in in four directions (up, down, left or right)
using their arrow keys.
3. If a snake collides with the border of the stage, it gets eliminated.
4. If a snake (A) collides with another snake (B) from the side, then snake A gets eliminated
while snake B survives.
5. If two snakes have a head-on collision, they both get eliminated (if these were the last
two snakes, then nobody wins).
6. The last snake alive wins the game.
