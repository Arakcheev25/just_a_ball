import webbrowser
import pygame
import sys
import random
import pygame_menu

pygame.init()


class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < SIZE_BLOCK and 0 <= self.y < SIZE_BLOCK

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def about():
    return webbrowser.open('https://t.me/Arakcheev_Ruslan')


SNAKE_COLOR = (0, 101, 0)
FRAME_COLOR = (0, 155, 155)
WHITE = (255, 255, 255)
BLUE = (104, 237, 208)
RED = (255, 0, 0)
BLACK = (9, 9, 9)
SIZE_BLOCK = 20
COUNT_BLOCK = 20
MARGIN = 1
HEADER_MARGIN = 70
HEADER_COLOR = (0, 204, 155)
size = (SIZE_BLOCK * COUNT_BLOCK + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCK,
        SIZE_BLOCK * COUNT_BLOCK + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCK + HEADER_MARGIN)

screen = pygame.display.set_mode(size)


def start_the_game():
    def get_draw_random_emply_block():
        x = random.randint(0, COUNT_BLOCK - 1)
        y = random.randint(0, COUNT_BLOCK - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, COUNT_BLOCK - 1)
            empty_block.y = random.randint(0, COUNT_BLOCK - 1)
        return empty_block

    def draw_block(colors, row, column):  # задаем параметры кледки
        pygame.draw.rect(screen, colors, (SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                          HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                                          SIZE_BLOCK,
                                          SIZE_BLOCK))

    d_row = 0
    d_col = 1
    total = 0
    speed = 1

    pygame.display.set_caption('Snake Game')  # зоголовок нашей проги
    timer = pygame.time.Clock()

    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    apple = get_draw_random_emply_block()

    while True:

        for event in pygame.event.get():  # обработка всех событий
            if event.type == pygame.QUIT:  # если тип события выход ->
                print('exit')
                pygame.quit()
                sys.exit()  # -> выход
            elif event.type == pygame.KEYDOWN:  # если тип события клавиатура
                if event.key == pygame.K_w and d_col != 0:  # если событие нажание на "w"
                    d_row = -1
                    d_col = 0
                if event.key == pygame.K_s and d_col != 0:
                    d_row = 1
                    d_col = 0
                if event.key == pygame.K_a and d_row != 0:
                    d_row = 0
                    d_col = -1
                if event.key == pygame.K_d and d_row != 0:
                    d_row = 0
                    d_col = 1

        screen.fill(FRAME_COLOR)  # наполняем переменную screen цветом
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

        courier_total = pygame.font.SysFont('Courier New', 36)
        courier_speed = pygame.font.SysFont('Courier New', 20)
        text_total = courier_total.render(f'Total: {total}', 0, BLACK)
        text_speed = courier_speed.render(f'Speed: {speed}', 0, BLACK)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK, SIZE_BLOCK + 50))

        for row in range(COUNT_BLOCK):
            for column in range(COUNT_BLOCK):
                if (row + column) % 2 == 0:
                    colors = BLUE
                else:
                    colors = WHITE
                draw_block(colors, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            print('exit')
            break
            # pygame.quit()
            # sys.exit()

        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        if apple == head:
            total += 1
            speed = total // 5 + 1
            snake_blocks.append(apple)
            apple = get_draw_random_emply_block()

        new_head = SnakeBlock(head.x + d_row, head.y + d_col)
        if new_head in snake_blocks[:-1]:
            print('Game Over! Snake crashed into itself')
            print('exit')
            break
        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        pygame.display.flip()  # обновляет содержимое основного окна игры
        timer.tick(4 + speed)


main_theme = pygame_menu.themes.THEME_ORANGE.copy()
main_theme = main_theme.set_background_color_opacity(1)

menu = pygame_menu.Menu(f'Snake game! ', size[0], size[1],
                        theme=pygame_menu.themes.THEME_ORANGE)

menu.add.text_input('Имя: ', default='Игрок 1')
menu.add.button('Играть', start_the_game)
menu.add.button('Выход', pygame_menu.events.EXIT)
menu.add.button('Поддержать проект', about)
while True:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()