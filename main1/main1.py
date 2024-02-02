import os
import sys
import pygame
import requests

map_file = 'map.png'


def new_search(x, y, z, tipe):
    api_server = "http://static-maps.yandex.ru/1.x/"
    params = {
        'll': ','.join([str(i) for i in (x, y)]),
        'z': str(z),
        'l': tipe
    }
    response = requests.get(api_server, params)

    if not response:
        sys.exit(1)

    global map_file
    with open(map_file, "wb") as file:
        file.write(response.content)


def user_input():
    return input(), int(input()), input()


def draw_map():
    coordinate, z, tipe = user_input()
    x, y = map(float, coordinate.split())
    new_search(x, y, z, tipe)
    pygame.init()
    a = pygame.image.load(map_file)
    b = a.get_rect()
    screen = pygame.display.set_mode((b.w, b.h))
    screen.blit(pygame.image.load(map_file), (0, 0))
    screen.blit(a, (0, 0))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    draw_map()