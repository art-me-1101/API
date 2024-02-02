import os
import sys
import pygame
import requests

map_file = 'map.png'


def new_search(coordinate, z, tipe):
    x, y = map(float, coordinate.split())
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={x},{y}&z={z}&l={tipe}"
    response = requests.get(map_request)

    if not response:
        sys.exit(1)

    global map_file
    with open(map_file, "wb") as file:
        file.write(response.content)


def user_input():
    return input(), int(input()), input()


def draw_map():
    pygame.init()
    a = pygame.image.load(map_file)
    b = a.get_rect()
    screen = pygame.display.set_mode((b.w, b.h))
    screen.blit(pygame.image.load(map_file), (0, 0))

    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    new_search(*user_input())
    draw_map()
