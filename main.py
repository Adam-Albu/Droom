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

    # world Y position
    wy[0] = y1 * CS + x1 * SN
    wy[1] = y2 * CS + x2 * SN

    # world Z height
    wz[0] = -P.z + ((P.l * wy[0]) / 32.0)
    wz[1] = -P.z + ((P.l * wy[1]) / 32.0)

    # screen X, screen Y position
    wx[0] = wx[0] * 200 / wy[0] + SW2
    wy[0] = wz[0] * 200 / wy[0] + SH2

    wx[1] = wx[1] * 200 / wy[1] + SW2
    wy[1] = wz[1] * 200 / wy[1] + SH2

    # draw points
    # if wx[0] > 0 and wx[0] < SW and wy[0] > 0 and wy[0] < SH:
    pixel(int(wx[0]), int(wy[0]), 0)
    # if wx[1] > 0 and wx[1] < SW and wy[1] > 0 and wy[1] < SH:
    pixel(int(wx[1]), int(wy[1]), 0)

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
    if key == pygame.K_m: K.m = 1

def keysUp(key):
    if key == pygame.K_w: K.w = 0
    if key == pygame.K_s: K.s = 0
    if key == pygame.K_a: K.a = 0
    if key == pygame.K_d: K.d = 0
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