import pyxel

pyxel.init(200,200)

ballx = 100
bally = 0
vx = 0.866    
vy = 0.5 
padx = 100
a=-1

def update():
    global ballx, bally, vx, vy, padx, a
    ballx += vx
    bally += vy
    padx = pyxel.mouse_x
    if ballx >= 200:
        vx = a*vx
    if ballx <= 0:
        vx = a*vx
    if bally >= 200:
        ballx = 100
        bally = 0

def draw():
    global ballx, bally, vx, vy, padx
    pyxel.cls(7)
    pyxel.circ(ballx, bally, 10, 6)
    pyxel.rect(padx-20, 195, 40, 5, 14)

pyxel.run(update, draw)