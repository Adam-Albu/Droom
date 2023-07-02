import math
import pygame

# Set up screen size
res        = 1                        #0=160x120 1=360x240 4=640x480
SW         = 160*res                  #screen width
SH         = 120*res                  #screen height
SW2        = int(SW/2)                   #half of screen width
SH2        = int(SH/2)                   #half of screen height
pixelScale = 4/res                    #PyGame pixel scale
PGSW       = int(SW*pixelScale)          #PyGame window width
PGSH       = int(SH*pixelScale)          #PyGame window height

class keys:
    w, s, a, d = (0, 0, 0, 0)
    su, sd = (0, 0)
    m = 0

K = keys()

class maths:
    cos = [0.0] * 360
    sin = [0.0] * 360

M = maths()

class player:
    x, y, z = (0, 0, 0)
    a = 0
    l = 0

P = player()

def pixel(x: int, y: int, c: int) -> None:
    rgb = [0, 0, 0]
    if c == 0: rgb[0] = 255; rgb[1] = 255; rgb[2] =   0  # Yellow
    if c == 1: rgb[0] = 160; rgb[1] = 160; rgb[2] =   0  # Yellow darker
    if c == 2: rgb[0] =   0; rgb[1] = 255; rgb[2] =   0  # Green
    if c == 3: rgb[0] =   0; rgb[1] = 160; rgb[2] =   0  # Green darker
    if c == 4: rgb[0] =   0; rgb[1] = 255; rgb[2] = 255  # Cyan
    if c == 5: rgb[0] =   0; rgb[1] = 160; rgb[2] = 160  # Cyan darker
    if c == 6: rgb[0] = 160; rgb[1] = 100; rgb[2] =   0  # brown
    if c == 7: rgb[0] = 110; rgb[1] =  50; rgb[2] =   0  # brown darker
    if c == 8: rgb[0] =   0; rgb[1] =  60; rgb[2] = 130  # background

    pygame.draw.rect(screen, pygame.Color(rgb[0], rgb[1], rgb[2]), pygame.Rect(x*pixelScale, y*pixelScale, pixelScale, pixelScale))

def movePlayer() -> None:
    dx: int = M.sin[P.a] * 10.0
    dy: int = M.cos[P.a] * 10.0

    if K.a == 1 and K.m == 0:
        P.x -= dy
        P.y += dx
    
    if K.d == 1 and K.m == 0:
        P.x += dy
        P.y -= dx

    if K.w == 1 and K.m == 0:
        P.x += dx
        P.y += dy
    
    if K.s == 1 and K.m == 0:
        P.x -= dx
        P.y -= dy

    if K.su == 1 and K.m == 0:
        P.z += 4

    if K.sd == 1 and K.m == 0:
        P.z -= 4
        
    if K.a == 1 and K.m == 1:
        P.a -= 4
        if P.a < 0: P.a += 360
    
    if K.d == 1 and K.m == 1:
        P.a += 4
        if P.a > 359: P.a -= 360
    
    if K.w == 1 and K.m == 1:
        P.l -= 4

    if K.s == 1 and K.m == 1:
        P.l += 4

def clearBackground() -> None:
    for y in range(SH):
        for x in range(SW):
            pixel(x, y, 8)

def drawWall(x1: int, x2: int, b1: int, b2: int, t1: int, t2: int) -> None:
    x, y = (0, 0)
    dyb: int = b2-b1
    dyt: int = t2-t1
    dx: int  = x2-x1
    if dx == 0: dx = 1
    xs: int = x1
    for x in range(x1, x2):
        y1: int = dyb * (x - xs + 0.5) / dx + b1
        y2: int = dyt * (x - xs + 0.5) / dx + t1
        for y in range(int(y1), int(y2)):
            pixel(x, y, 0)

def draw3D() -> None:
    wx = [0] * 4
    wy = [0] * 4
    wz = [0] * 4

    CS = M.cos[P.a]
    SN = M.sin[P.a]

    # offset bottom two points by player
    x1 = 40 - P.x
    y1 = 10 - P.y

    x2 = 40 - P.x
    y2 = 290 - P.y

    # world X position
    wx[0] = x1 * CS - y1 * SN
    wx[1] = x2 * CS - y2 * SN
    wx[2] = wx[0]
    wx[3] = wx[1]

    # world Y position
    wy[0] = y1 * CS + x1 * SN
    wy[1] = y2 * CS + x2 * SN
    wy[2] = wy[0]
    wy[3] = wy[1]

    # world Z height
    wz[0] = -P.z + ((P.l * wy[0]) / 32.0)
    wz[1] = -P.z + ((P.l * wy[1]) / 32.0)
    wz[2] = wz[0] + 40
    wz[3] = wz[1] + 40

    # screen X, screen Y position
    wx[0] = wx[0] * 200 / wy[0] + SW2
    wy[0] = wz[0] * 200 / wy[0] + SH2

    wx[1] = wx[1] * 200 / wy[1] + SW2
    wy[1] = wz[1] * 200 / wy[1] + SH2

    wx[2] = wx[2] * 200 / wy[2] + SW2
    wy[2] = wz[2] * 200 / wy[2] + SH2

    wx[3] = wx[3] * 200 / wy[3] + SW2
    wy[3] = wz[3] * 200 / wy[3] + SH2

    drawWall(int(wx[0]), int(wx[1]), int(wy[0]), int(wy[1]), int(wy[2]), int(wy[3]))

def display() -> None:
    clearBackground()
    movePlayer()
    draw3D()

    screen.blit(pygame.transform.flip(screen, False, True), (0,0))
    pygame.display.flip()
    screen.blit(pygame.transform.flip(screen, False, True), (0,0))

def keysDown(key):
    if key == pygame.K_w: K.w = 1
    if key == pygame.K_s: K.s = 1
    if key == pygame.K_a: K.a = 1
    if key == pygame.K_d: K.d = 1
    if key == pygame.K_e: K.su = 1
    if key == pygame.K_q: K.sd = 1
    if key == pygame.K_m: K.m = 1

def keysUp(key):
    if key == pygame.K_w: K.w = 0
    if key == pygame.K_s: K.s = 0
    if key == pygame.K_a: K.a = 0
    if key == pygame.K_d: K.d = 0
    if key == pygame.K_e: K.su = 0
    if key == pygame.K_q: K.sd = 0
    if key == pygame.K_m: K.m = 0

def init():
    for x in range(360):
        M.cos[x] = math.cos(math.radians(x))
        M.sin[x] = math.sin(math.radians(x))

    P.x = 70
    P.y = -110
    P.z = 20
    P.a = 0
    P.l = 0

# Set up PyGame
pygame.init()
pygame.display.set_caption("Droom")
screen = pygame.display.set_mode((PGSW, PGSH))
clock = pygame.time.Clock()

init()

running = True

while running:
    clock.tick(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN: keysDown(event.key)
        if event.type == pygame.KEYUP: keysUp(event.key)

    display()