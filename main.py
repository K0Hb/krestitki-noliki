import pygame
import random
from typing import List, Tuple

LENGTH = 10  # (N x N)field
SCREEN_SIZE = 100 * LENGTH  # ширина/длина окна
SIZE_ONE_CELL = SCREEN_SIZE // LENGTH
QUANITY_CHARS = 5  # кол-во символов для победы


def draw_grid(scr: pygame.Surface) -> None:
    '''Прорисовка поля'''
    line = 100
    for x in range(10):
        pygame.draw.line(scr, (0, 0, 0), (line, 0), (line, SCREEN_SIZE), 3)
        pygame.draw.line(scr, (0, 0, 0), (0, line), (SCREEN_SIZE, line), 3)
        line += SIZE_ONE_CELL


def draw_tic_tac_toe(scr: pygame.Surface, itmes: List) -> None:
    '''Прорисовка крестиков и ноликов'''
    for i in range(LENGTH):
        for j in range(LENGTH):
            if itmes[i][j] == '0':
                radius = SIZE_ONE_CELL // 2
                pygame.draw.circle(
                    scr, (255, 0, 0),
                    (j * SIZE_ONE_CELL + radius, i * SIZE_ONE_CELL + radius),
                    radius * 0.95)
            elif itmes[i][j] == 'x':
                length_line = SIZE_ONE_CELL * 0.95
                gap_to_line = SIZE_ONE_CELL * 0.05
                pygame.draw.line(
                    scr, (0, 0, 255),
                    (j * SIZE_ONE_CELL + gap_to_line, i * SIZE_ONE_CELL + gap_to_line),
                    (j * SIZE_ONE_CELL + length_line, i * SIZE_ONE_CELL + length_line),
                    3)
                pygame.draw.line(
                    scr, (0, 0, 255),
                    (j * SIZE_ONE_CELL + length_line, i * SIZE_ONE_CELL + gap_to_line),
                    (j * SIZE_ONE_CELL + gap_to_line, i * SIZE_ONE_CELL + length_line),
                    3)


def change_i_j(x: int, i: int, j: int, vertical: bool = False) -> Tuple:
    '''Изменение координат в соответсвии проверочной оси'''
    if vertical:
        i = x
        return i, j
    j = x
    return i, j


def check_hrznt_vrtcl(fd: List, symbol: str, i: int, j: int, vertical=False) -> bool:
    """Проверка на условия победы по горизонтали и вертикали"""
    count = 0
    check_symbol = None
    for x in range(LENGTH):
        i, j = change_i_j(x, i, j, vertical)
        if check_symbol != fd[i][j]:
            check_symbol = fd[i][j]
            count = 0
        elif check_symbol == fd[i][j]:
            count += 1
            if count == QUANITY_CHARS - 1 and check_symbol == symbol:
                return True
    return False


def check_loss_main_diagonal(fd: List, i: int, j: int) -> bool:
    """Проверка на условия победы по диагонали( ⇘ )"""
    result_1 = 1
    i_up = i - 1
    j_up = j - 1
    while result_1 != QUANITY_CHARS and i_up >= 0 and j_up >= 0:
        if fd[i][j] == fd[i_up][j_up]:
            result_1 += 1
            i_up -= 1
            j_up -= 1
        else:
            break
    i_down = i + 1
    j_down = i + 1
    result_2 = 1
    while result_2 != QUANITY_CHARS and i_down <= (LENGTH - 1) and j_down <= (LENGTH - 1):
        if fd[i][j] == fd[i_down][j_down]:
            result_2 += 1
            i_down += 1
            j_down += 1
        else:
            break
    result = max(result_1, result_2)
    if result >= 5:
        return True
    else:
        return False


def check_loss_side_diagonal(fd: List, i: int, j: int) -> bool:
    """Проверка на условия победы по диагонали( ⇙ )"""
    result_1 = 1
    i_up = i - 1
    j_up = j + 1
    while result_1 != QUANITY_CHARS and i_up >= 0 and j_up <= (LENGTH - 1):
        if fd[i][j] == fd[i_up][j_up]:
            result_1 += 1
            i_up -= 1
            j_up += 1
        else:
            break
    i_down = i + 1
    j_down = j - 1
    result_2 = 1
    while result_2 != QUANITY_CHARS and i_down <= (LENGTH - 1) and j_down >= 0:
        if fd[i][j] == fd[i_down][j_down]:
            result_2 += 1
            i_down += 1
            j_down -= 1
        else:
            break
    result = max(result_1, result_2)
    if result >= 5:
        return True
    else:
        return False


def get_win_check(fd: list, symbol: str, i_j: Tuple = None) -> bool:
    '''Поочердная проверка осей на условия победы'''
    i, j = i_j[0], i_j[1]
    horizont = check_hrznt_vrtcl(fd, symbol, i, j)
    vertical = check_hrznt_vrtcl(fd, symbol, i, j, True)
    diagonal1 = check_loss_main_diagonal(fd, i, j)
    diagonal2 = check_loss_side_diagonal(fd, i, j)

    return any([horizont, vertical, diagonal1, diagonal2])


def main_loop() -> None:
    '''Основной цикл игровой логики и прорисовки поля с событиями'''
    pygame.init()
    window = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))  # размер окна
    screen = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption('обратные крестики нолики')  # названия
    screen.fill((255, 255, 255))  # цвет

    field = [[''] * 10 for x in range(LENGTH)]  # поле

    mainloop = True
    game_over = False

    while mainloop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pos = pygame.mouse.get_pos()
                if field[pos[1] // SIZE_ONE_CELL][pos[0] // SIZE_ONE_CELL] == '':
                    field[pos[1] // SIZE_ONE_CELL][pos[0] // SIZE_ONE_CELL] = 'x'
                    x, y = random.randint(0, LENGTH - 1), random.randint(0, LENGTH - 1)
                    while field[x][y] != '':
                        x, y = random.randint(0, LENGTH - 1), random.randint(0, LENGTH - 1)
                    field[x][y] = '0'
                    player_move = (pos[1] // SIZE_ONE_CELL, pos[0] // SIZE_ONE_CELL)
                    bot_move = (x, y)
                player_win = get_win_check(field, 'x', player_move)
                bot_win = get_win_check(field, '0', bot_move)
                if player_win or bot_win:
                    game_over = True
                    if player_win:
                        pygame.display.set_caption('Вы победили')
                    else:
                        pygame.display.set_caption('Вы проиграли')

        draw_tic_tac_toe(screen, field)
        draw_grid(screen)
        window.blit(screen, (0, 0))
        pygame.display.update()


if __name__ == '__main__':
    main_loop()
