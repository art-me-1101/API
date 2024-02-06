import os
import pygame
import requests

map_file = 'map.png'
size = (600, 400)
win = (1200, 400)
map_mode = ['map', 'sat', 'sat,skl']
cur_mode = 0
point = ''


def new_search(x, y, w, h):
    global size, map_mode, cur_mode, point
    api_server = "http://static-maps.yandex.ru/1.x/"
    params = {
        'll': ','.join([str(i) for i in (x, y)]),
        'spn': ','.join(list(map(str, (w, h)))),
        'l': map_mode[cur_mode],
        'size': ','.join(list(map(str, size)))
    }
    if point:
        params['pt'] = point
    response = requests.get(api_server, params)
    if not response:
        return 1
    global map_file
    with open(map_file, "wb") as file:
        file.write(response.content)


def find_place_by_name(name, x, y):
    global point
    api_server = "http://geocode-maps.yandex.ru/1.x/"
    params = {
        'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
        'geocode': name,
        'format': 'json',
        'll': ','.join(list(map(str, (x, y))))
    }
    response = requests.get(api_server, params)
    if not response:
        return None
    response_json = response.json()
    a = response_json['response']['GeoObjectCollection']['featureMember']
    if len(a) > 0:
        locate = a[0]['GeoObject']['Point']['pos']
        x, y = map(float, locate.split())
        b = a[0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
        point = f'{x},{y},pm2rdl'
        return (x, y), b
    return None


def draw_map():
    global cur_mode, point
    adres_text = []
    x, y = 41.158318, 56.914098
    w, h = 0.006, 0.004
    pygame.init()
    screen = pygame.display.set_mode(win)
    font1 = pygame.font.Font(None, 23)
    change_mode = font1.render('сменить режим', True, (0, 0, 0))
    chenge_mode_rect = pygame.rect.Rect(620, 20, change_mode.get_width(), change_mode.get_height())
    font2 = pygame.font.Font(None, 25)
    chenge_mode_box = pygame.rect.Rect(615, 15, change_mode.get_width() + 10, change_mode.get_height() + 7)
    del_point = font1.render('сброс поискового результата', True, (0, 0, 0))
    del_point_box = pygame.rect.Rect(750, 15, del_point.get_width() + 10, del_point.get_height() + 10)
    xdp, ydp = del_point_box.x + (del_point_box.w - del_point.get_width()) // 2, del_point_box.y + (
                del_point_box.h - del_point.get_height()) // 2
    seach_box = pygame.rect.Rect(615, 50, 400, 30)
    cur_search = False
    search_text = ''
    search_text_visual = font2.render(search_text, True, (0, 0, 0))
    search_button_box = pygame.rect.Rect(1015, 50, 100, 30)
    search_button_text = font2.render('Найти', True, (0, 0, 0))
    x_sbt, y_sbt = search_button_box.x + (
            search_button_box.w - search_button_text.get_width()) // 2, search_button_box.y + (
                           search_button_box.h - search_button_text.get_height()) // 2,
    if new_search(x, y, w, h) == 1:
        return None
    a = pygame.image.load(map_file)
    screen.blit(a, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if seach_box.collidepoint(*event.pos):
                        cur_search = True
                    else:
                        cur_search = False
                    if chenge_mode_box.collidepoint(*event.pos):
                        cur_mode = (cur_mode + 1) % len(map_mode)
                        if new_search(x, y, w, h) != 1:
                            a = pygame.image.load(map_file)
                    elif search_button_box.collidepoint(*event.pos) and search_text:
                        f = find_place_by_name(search_text, x, y)
                        if f is not None:
                            coordinates = f[0]
                            adres = 'Адрес: ' + ', '.join(f[1].split(','))
                            c = len(adres.split()[0])
                            q = adres.split()[0]
                            for i in adres.split()[1:]:
                                if c + len(i) + 1 > 30:
                                    adres_text.append(q)
                                    q = ''
                                    c = 0
                                else:
                                    q += ' '
                                c += len(i)
                                q += i
                            adres_text.append(q)
                            x, y = coordinates
                            if new_search(x, y, w, h) == 1:
                                print('error')
                            a = pygame.image.load(map_file)
                        search_text = ''
                        search_text_visual = font2.render(search_text, True, (0, 0, 0))
                    elif del_point_box.collidepoint(*event.pos):
                        point = ''
                        if new_search(x, y, w, h) == 1:
                            print('error')
                        a = pygame.image.load(map_file)
                        adres_text = []
            elif event.type == pygame.KEYDOWN:
                if cur_search:
                    if event.key == pygame.K_BACKSPACE:
                        search_text = search_text[:-1]
                    else:
                        search_text += event.unicode
                search_text_visual = font2.render(search_text, True, (0, 0, 0))
                while search_text_visual.get_width() >= seach_box.width - 5:
                    search_text = search_text[:-1]
                    search_text_visual = font2.render(search_text, True, (0, 0, 0))
                if event.key == pygame.K_PAGEUP:
                    if h > 0.0005:
                        h /= 2
                        w /= 2
                        if new_search(x, y, w, h) == 1:
                            print('error')
                        a = pygame.image.load(map_file)
                elif event.key == pygame.K_PAGEDOWN:
                    if h < 90:
                        h *= 2
                        w *= 2
                        if new_search(x, y, w, h) == 1:
                            print('error')
                        a = pygame.image.load(map_file)
                elif event.key == pygame.K_UP:
                    y = (y + h) % 90
                    if new_search(x, y, w, h) == 1:
                        print('error')
                    a = pygame.image.load(map_file)
                elif event.key == pygame.K_DOWN:
                    y = (y - h) % 90
                    if new_search(x, y, w, h) == 1:
                        print('error')
                    a = pygame.image.load(map_file)
                elif event.key == pygame.K_LEFT:
                    x = (x - w) % 180
                    if new_search(x, y, w, h) == 1:
                        print('error')
                    a = pygame.image.load(map_file)
                elif event.key == pygame.K_RIGHT:
                    x = (x + w) % 180
                    if new_search(x, y, w, h) == 1:
                        print('error')
                    a = pygame.image.load(map_file)
        screen.fill((255, 255, 255))
        screen.blit(a, (0, 0))
        screen.blit(change_mode, chenge_mode_rect)
        pygame.draw.rect(screen, (0, 0, 0), chenge_mode_box, 1)
        if not cur_search:
            screen.fill((230, 230, 230), seach_box)
        pygame.draw.rect(screen, (0, 0, 0), del_point_box, 1)
        screen.blit(del_point, (xdp, ydp))
        pygame.draw.rect(screen, (0, 0, 0), seach_box, 1)
        pygame.draw.rect(screen, (0, 0, 0), search_button_box, 1)
        screen.blit(search_button_text, (x_sbt, y_sbt))
        screen.blit(search_text_visual, (seach_box.x + 5, seach_box.y + 6))
        font3 = pygame.font.Font(None, 30)
        text_coord = 150
        for line in adres_text:
            string_rendered = font3.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 630
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    draw_map()
