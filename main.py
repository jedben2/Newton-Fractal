# main.py

import pygame
import numpy as np
import time

WIDTH = 10
SPACE = 1000
zoom = 70
rect_len = 1
iterations = 10

pygame.init()
w = pygame.display.set_mode((800, 800))

xs = np.linspace(-1 * WIDTH / 2, WIDTH / 2, SPACE)
ys = np.linspace(-1 * WIDTH / 2, WIDTH / 2, SPACE)

roots = [complex(np.random.randint(-WIDTH / 2, WIDTH / 2, size=1), np.random.randint(-WIDTH, WIDTH, size=1)) for _ in range(6)]
colours = [list(np.random.choice(range(256), size=3)) for root in roots]

def f(x):
    val = 1
    for root in roots:
        val *= x - root
    return val

def df(x):
    val = 1
    for n in range(len(roots) - 1, 0, - 1):
        val *= x - roots[n - 1]
        prod = 1
        for k in range(n, len(roots), 1):
            prod *= x - roots[k]
        val += prod
    return val

def NR(x, y):
    z = complex(x, y)
    for i in range(iterations):
        try:
            z -= f(z) / df(z)
        except ZeroDivisionError:
            return z
    return z


points = []

t1 = time.time()
for x in xs:
    for y in ys:
        z = NR(x, y)
        dists = [[abs(root - z), ind] for ind, root in enumerate(roots)]
        min_dist = dists[0]
        for dist in dists:
            if dist[0] < min_dist[0]:
                min_dist = dist
        points.append([x, y, min_dist])

print(f"compute: {time.time() - t1} seconds")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            t1 = time.time()
            colours = [list(np.random.choice(range(256), size=3)) for root in roots]
            for point in points:
                pygame.draw.rect(surface=w, color=colours[point[2][1]],
                                 rect=pygame.Rect(zoom * point[0] + 400, zoom * point[1] + 400, rect_len, rect_len))
            for root in roots:
                pygame.draw.circle(surface=w, color=(0, 0, 0), center=(400 + zoom * root.real, 400 + zoom * root.imag), radius=5)
            print(f"render: {time.time() - t1} seconds")
    pygame.display.flip()
