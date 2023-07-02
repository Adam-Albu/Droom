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
    if K.a == 1 and K.m == 0: print("left")
    if K.d == 1 and K.m == 0: print("right")
    if K.w == 1 and K.m == 0: print("up")
    if K.s == 1 and K.m == 0: print("down")

    if K.a == 1 and K.m == 1: print("look left")
    if K.d == 1 and K.m == 1: print("look right")
    if K.w == 1 and K.m == 1: print("look up")
    if K.s == 1 and K.m == 1: print("look down")

def clearBackground() -> None:
    for y in range(SH):
        for x in range(SW):
            pixel(x, y, 8)

tick: int = 0

def draw3D() -> None:
    global tick
    x, y, c = (0, 0, 0)
    for y in range(SH2):
        for x in range(SW2):
            pixel(x, y, c)
            c += 1
            if c > 8: c = 0
    tick += 1
    if tick > 20: tick = 0
    pixel(SW2, SH2+tick, 0)

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