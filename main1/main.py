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
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.K_UP:
                print(2)
                if z > 1:
                    z -= 1
                    new_search(x, y, z, tipe)
                    a = pygame.image.load(map_file)
            elif event.type == pygame.K_DOWN:
                if z < 20:
                    z += 1
                    new_search(x, y, z, tipe)
                    a = pygame.image.load(map_file)
        screen.blit(a, (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    draw_map()
