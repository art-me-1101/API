import os
import pygame
import requests

map_file = 'map.png'
size = (600, 400)


def new_search(x, y, w, h, tipe):
    global size
    api_server = "http://static-maps.yandex.ru/1.x/"
    params = {
        'll': ','.join([str(i) for i in (x, y)]),
        'spn': ','.join(list(map(str, (w, h)))),
        'l': tipe,
        'size': ','.join(list(map(str, size)))
    }
    response = requests.get(api_server, params)

    if not response:
        return 1

    global map_file
    with open(map_file, "wb") as file:
        file.write(response.content)


def user_input():
    return input(), input()


def draw_map():
    coordinate, tipe = user_input()
    y, x = map(float, coordinate.split())
    w, h = 0.6, 0.4
    if new_search(x, y, w, h, tipe) == 1:
        return None
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    if h > 0.0005:
                        h /= 2
                        w /= 2
                        if new_search(x, y, w, h, tipe) != 1:
                            a = pygame.image.load(map_file)
                elif event.key == pygame.K_PAGEDOWN:
                    if h < 90:
                        h *= 2
                        w *= 2
                        if new_search(x, y, w, h, tipe) != 1:
                            a = pygame.image.load(map_file)
                elif event.key == pygame.K_UP:
                    y = (y + h) % 90
                    if new_search(x, y, w, h, tipe) != 1:
                        a = pygame.image.load(map_file)
                elif event.key == pygame.K_DOWN:
                    y = (y - h) % 90
                    if new_search(x, y, w, h, tipe) != 1:
                        a = pygame.image.load(map_file)
                elif event.key == pygame.K_LEFT:
                    x = (x - w) % 180
                    if new_search(x, y, w, h, tipe) != 1:
                        a = pygame.image.load(map_file)
                elif event.key == pygame.K_RIGHT:
                    x = (x + w) % 180
                    if new_search(x, y, w, h, tipe) != 1:
                        a = pygame.image.load(map_file)
        screen.blit(a, (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    draw_map()
