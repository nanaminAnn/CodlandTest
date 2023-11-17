import pygame
from pygame import *
import sys
import random
#import time

pygame.init()

# Размеры окна
width, height = 500, 500

# Константы цветов RGB
BLACK = (0 , 0 , 0)
WHITE = (255 , 255 , 255)
GREY = (200, 200, 200)

#задам шрифт
front = font.SysFont('monospace', 36) 

#класс для меню
class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._callbacks = []
        self._current_option_index = 0

    def append_option (self, option, callback):
        self._option_surfaces.append(front.render(option, True, (0,0,0)))
        self._callbacks.append(callback)

    def switch(self, diraction):
        self._current_option_index = max (0, min(self._current_option_index + diraction, len(self._option_surfaces) - 1))

    def select(self):
        self._callbacks[self._current_option_index]()

    def draw(self, surf, x, y, option_y_padding):
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if i == self._current_option_index:
                draw.rect(surf, (154, 205, 50), option_rect)
            surf.blit(option, option_rect)

#создание игровых функций

# 1 уровень, созерцание
def contemplation_function():
    clock = pygame.time.Clock()
    # Создаем окно
    root = pygame.display.set_mode((500 , 500))
    pygame.display.set_caption("Game of Life. Сontemplation")
    # 2х мерный список с помощью генераторных выражений
    cells = [[random.choice([0 , 1]) for j in range(root.get_width() // 20)] for i in range(root.get_height() // 20)]

    # Функция определения кол-ва соседей
    def near(pos: list , system=[[-1 , -1] , [-1 , 0] , [-1 , 1] , [0 , -1] , [0 , 1] , [1 , -1] , [1 , 0] , [1 , 1]]):
        count = 0
        for i in system:
            if cells[(pos[0] + i[0]) % len(cells)][(pos[1] + i[1]) % len(cells[0])]:
                count += 1
        return count

    # Основной цикл
    while 1:
        # Заполняем экран белым цветом
        root.fill(WHITE)

        # Рисуем сетку
        for i in range(0 , root.get_height() // 20):
            pygame.draw.line(root , GREY , (0 , i * 20) , (root.get_width() , i * 20))
        for j in range(0 , root.get_width() // 20):
            pygame.draw.line(root , GREY , (j * 20 , 0) , (j * 20 , root.get_height()))
    # Нужно чтобы виндовс не думал что программа "не отвечает"
        for i in pygame.event.get():
            if i.type == QUIT:
                quit()
        # Проходимся по всем клеткам

        for i in range(0 , len(cells)):
            for j in range(0 , len(cells[i])):
#                print(cells[i][j],i,j)
                pygame.draw.rect(root , (0, 255 * cells[i][j] % 256 , 0) , [i * 20 , j * 20 , 20 , 20])
        # Обновляем экран
        pygame.display.update()
        cells2 = [[0 for j in range(len(cells[0]))] for i in range(len(cells))]
        for i in range(len(cells)):
            for j in range(len(cells[0])):
                if cells[i][j]:
                    if near([i , j]) not in (2 , 3):
                        cells2[i][j] = 0
                        continue
                    cells2[i][j] = 1
                    continue
                if near([i , j]) == 3:
                    cells2[i][j] = 1
                    continue
                cells2[i][j] = 0
        cells = cells2 

        pygame.display.update()
        clock.tick(30)

# 2 уровень, средний
def average_function():
    root = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Game of Life. Average")
    cells = [[0 for j in range(root.get_width() // 20)] for i in range(root.get_height() // 20)]

    # Функция определения кол-ва соседей
    def near(pos: list , system=[[-1 , -1] , [-1 , 0] , [-1 , 1] , [0 , -1] , [0 , 1] , [1 , -1] , [1 , 0] , [1 , 1]]):
        count = 0
        for i in system:
            if cells[(pos[0] + i[0]) % len(cells)][(pos[1] + i[1]) % len(cells[0])]:
                count += 1
        return count

    running = True
    drawing = False
    autoplay = False  # Флаг для автоматического обновления

    clock = pygame.time.Clock()

    while running:
        root.fill(WHITE)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                drawing = True
            elif event.type == MOUSEBUTTONUP:
                drawing = False
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    autoplay = not autoplay  # Изменение флага при нажатии вправо

        if autoplay:
            # Обновление клеток
            cells2 = [[0 for j in range(len(cells[0]))] for i in range(len(cells))]
            for i in range(len(cells)):
                for j in range(len(cells[0])):
                    if cells[i][j]:
                        if near([i, j]) not in (2, 3):
                            cells2[i][j] = 0
                            continue
                        cells2[i][j] = 1
                        continue
                    if near([i, j]) == 3:
                        cells2[i][j] = 1
                        continue
                    cells2[i][j] = 0
            cells = cells2

        # Обработка рисования клеток при нажатии мыши
        if drawing:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            cell_x, cell_y = mouse_x // 20, mouse_y // 20
            if 0 <= cell_x < len(cells) and 0 <= cell_y < len(cells[0]):
                cells[cell_x][cell_y] = 1

        # Рисование клеток
        for i in range(len(cells)):
            for j in range(len(cells[i])):
                pygame.draw.rect(root, (0, 255 * cells[i][j] % 256 , 0), [i * 20, j * 20, 20, 20])

        pygame.display.update()
        clock.tick(30)  # Ограничение скорости обновления (10 кадров в секунду)






# Создание окна меню
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hello, this is the Game of Life. Select difficulty level")

#заполнение меню           
menu = Menu()
menu.append_option('contemplation', contemplation_function)
menu.append_option('average', average_function)
menu.append_option('hard', lambda: print ('hallo3'))
menu.append_option('exit', quit)

running = True

# игровой цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == pygame.K_UP:
                menu.switch(-1)
            elif event.key == pygame.K_DOWN:
                menu.switch(1)
            elif event.key == pygame.K_RIGHT:
                menu.select()

    screen.fill(WHITE)

    menu.draw(screen , 100 , 100, 75)

    # Обновление окна
    pygame.display.flip()

# Завершение работы Pygame и выход из программы
pygame.quit()
sys.exit()