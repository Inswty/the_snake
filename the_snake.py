from random import choice, randint, randrange

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    '''Базовый класс, содержит общие атрибуты игровых объектов
    и заготовку метода для отрисовки объекта на игровом поле — draw.
    '''

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = ()

    def draw(self):
        pass


class Apple(GameObject):
    '''Описывает яблоко и действия с ним.'''

    def __init__(self):
        super().__init__()
        self.body_color = (255, 0, 0)

    def randomize_position(self):
        '''Устанавливает случайное положение яблока на игровом поле.'''
        self.position = (
            randrange(0, SCREEN_WIDTH, GRID_SIZE),
            randrange(0, SCREEN_HEIGHT, GRID_SIZE),
        )

    def draw(self):
        '''Отрисовывает яблоко на игровом поле.'''
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    '''Описывает змейку и её поведение, управляет её движением, отрисовкой,
    а также обрабатывает действия пользователя.
    '''
    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = self.position
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)

    def update_direction(self):
        '''Метод обновления направления после нажатия на кнопку.'''
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        '''Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions и удаляя
        последний элемент, если длина змейки не увеличилась.
        '''
        match self.direction:
            case 'RIGHT':
                # Не достигнута пр.границы поля?
                if self.positions[0][0] != SCREEN_WIDTH - 20:
                    # Продолжаем движение:
                    self.positions.insert(
                        0, (self.positions[0][0] + 20, self.positions[0][1])
                    )
                    self.positions.pop()
                else:
                    # Если граница достигнута, появляемся слева:
                    self.positions.insert(
                        0, (0, self.positions[0][1])
                    )
                    self.positions.pop()
            case 'LEFT':
                # Не достигнута пр.границы поля?
                if self.positions[0][0] != 0:
                    # Продолжаем движение:
                    self.positions.insert(
                        0, (self.positions[0][0] - 20, self.positions[0][1])
                    )
                    self.positions.pop()
                else:
                    # Если граница достигнута, появляемся права:
                    self.positions.insert(
                        0, (SCREEN_WIDTH - 20, self.positions[0][1])
                    )
                    self.positions.pop()
            case 'UP':
                # Не достигнута верхняя граница поля?
                if self.positions[0][1] != 0:
                    # Продолжаем движение:
                    self.positions.insert(
                        0, (self.positions[0][0], self.positions[0][1] - 20)
                    )
                    self.positions.pop()
                else:
                    # Если граница достигнута, появляемся снизу:
                    self.positions.insert(
                        0, (self.positions[0][0], SCREEN_HEIGHT - 20)
                    )
                    self.positions.pop()
            case 'DOWN':
                # Не достигнута пр.границы поля?
                if self.positions[0][1] != SCREEN_HEIGHT - 20:
                    # Продолжаем движение:
                    self.positions.insert(
                        0, (self.positions[0][0], self.positions[0][1] + 20)
                    )
                else:
                    # Если граница достигнута, появляемся сверху:
                    self.positions.insert(
                        0, (self.positions[0][0], 0)
                    )
                    self.positions.pop()

    def draw(self) -> None:
        '''Отрисовывает змейку на экране, затирая след.'''
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self) -> tuple:
        '''Возвращает позицию головы змейки
        (первый элемент в списке positions).
        '''
        return self.position[0]

    def reset(self) -> None:
        '''Сбрасывает змейку в начальное состояние.'''
        self.positions = self.position
        self.direction = RIGHT


def handle_keys(game_object):
    '''Функция обработки действий пользователя'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # Обработка событий клавиш.
        handle_keys(snake)
        # Обновление направления движения змейки.
        snake.update_direction()
        # Движение (модификация списка).
        snake.move()
        # Проверка употребления яблока внутрь змейки:
        if snake.get_head_position() == apple.position:
            # Координаты головы совпали с координатами яблока.
            # Увеличиваем длину.
            
            # Перемещаем яблоко.
            apple.randomize_position()
        # Проверка столкновения змейки с собой.
        if snake.get_head_position() in snake.positions:
            # Наезд на хвост. Перезапуск.
            snake.reset()
        # Отрисовка змейки.
        snake.draw()
        # Отрисовка яблока.
        apple.draw()
        # Обновление экрана.
        pygame.display.update()


if __name__ == '__main__':
    main()


#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
