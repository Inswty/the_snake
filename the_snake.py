from random import choice, randrange

import pygame as pg

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

# Карта направлений:
TURN_MAP = {
    # Если змейка движется ВВЕРХ, можно пойти ВЛЕВО или ВПРАВО
    (UP, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,

    # Если змейка движется ВНИЗ, можно пойти ВЛЕВО или ВПРАВО
    (DOWN, pg.K_LEFT): LEFT,
    (DOWN, pg.K_RIGHT): RIGHT,

    # Если змейка движется ВЛЕВО, можно пойти ВВЕРХ или ВНИЗ
    (LEFT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,

    # Если змейка движется ВПРАВО, можно пойти ВВЕРХ или ВНИЗ
    (RIGHT, pg.K_UP): UP,
    (RIGHT, pg.K_DOWN): DOWN,
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет тела змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет головы
SNAKE_HEAD_COLOR = (0, 200, 0)

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс, содержит общие атрибуты игровых объектов."""

    def __init__(self, color=BOARD_BACKGROUND_COLOR):
        self.position = (
            (SCREEN_WIDTH // 2 - GRID_SIZE), (SCREEN_HEIGHT // 2 - GRID_SIZE)
        )
        self.body_color = color

    def draw(self):
        """Метод должен быть реализован в подклассе."""
        raise NotImplementedError(
            f'Метод draw() не реализован в классе {self.__class__.__name__}.'
        )

    def draw_rect(self, position, body_color, border_color=None):
        """Отрисовает элемент змейки."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        if border_color:
            pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Описывает яблоко и действия с ним."""

    def __init__(self, color=APPLE_COLOR, occupied_positions=None):
        super().__init__(color)
        # Если occupied_positions равно None или пусто ([], '', 0, и т.п.)
        #  — используется []:
        self.randomize_position(occupied_positions or [])

    def randomize_position(self, occupied_positions):
        """Выбирает случайную свободную позицию на игровом поле."""
        while True:
            self.position = (
                randrange(0, SCREEN_WIDTH, GRID_SIZE),
                randrange(0, SCREEN_HEIGHT, GRID_SIZE),
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        self.draw_rect(self.position, self.body_color, BORDER_COLOR)


class Snake(GameObject):
    """Описывает змейку и её поведение.
    Управляет движением, отрисовкой. Обрабатывает действия пользователя.
    """

    def __init__(self, color=SNAKE_COLOR, head_color=SNAKE_HEAD_COLOR):
        super().__init__(color)
        self.head_color = head_color
        self.speed = 10  # Начальная скорость змейки.
        self.reset()
        self.direction = RIGHT

    def update_direction(self, new_direction):
        """Метод обновления направления после нажатия на кнопку."""
        if new_direction:
            self.direction = new_direction

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции).
        Добавляет новую голову в начало списка positions, удаляет
        последний элемент, если длина змейки не увеличилась.
        """
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        # Добавляем голову с новыми координатами.
        self.positions.insert(0, (
            # Назначение новых координат и телепортация через границы экрана.
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        ))
        # Если змейка не съела яблоко — удаляем последний сегмент.
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        # Отрисовка головы.
        self.draw_rect(self.get_head_position(), self.head_color, BORDER_COLOR)

        # Отрисовка глаз
        eye_radius = 3
        offset = 5
        pos_x, pos_y = self.get_head_position()

        eye_offsets = {
            # Если движется вправо.
            RIGHT: [(GRID_SIZE - offset, offset),
                    (GRID_SIZE - offset, GRID_SIZE - offset)],
            # Если движется влево.
            LEFT: [(offset, offset),
                   (offset, GRID_SIZE - offset)],
            # Если движется вверх.
            UP: [(offset, offset),
                 (GRID_SIZE - offset, offset)],
            # Если движется вниз.
            DOWN: [(offset, GRID_SIZE - offset),
                   (GRID_SIZE - offset, GRID_SIZE - offset)],
        }
        # Глаза на голове в соответсвии с направлением.
        for dx, dy in eye_offsets.get(self.direction, []):
            pg.draw.circle(screen, BOARD_BACKGROUND_COLOR,
                           (pos_x + dx, pos_y + dy), eye_radius)

        # Голова становится телом.
        if len(self.positions) > 1:
            self.draw_rect(self.positions[1], self.body_color)

        # Затирание последнего сегмента.
        if self.last:
            self.draw_rect(self.last, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.last = None


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        # Выход по Esc или закрытие окна.
        if (event.type == pg.QUIT
                or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)):
            pg.quit()
            raise SystemExit

        if event.type == pg.KEYDOWN:
            # Возвращаем новое направление, если значение есть в словаре.
            # Если в словаре значения нет, возвращается None.
            new_direction = TURN_MAP.get(
                (game_object.direction, event.key))

            # Регулировка скорости.
            if event.key in (pg.K_PLUS, pg.K_EQUALS):
                game_object.speed = min(game_object.speed + 2, 30)  # Макс 30.
            elif event.key == pg.K_MINUS:
                game_object.speed = max(game_object.speed - 2, 6)  # Мин 6.
            return new_direction


def main():
    """Основной игровой цикл."""
    # Инициализация pygame:
    pg.init()
    # Создаём экземпляры классов.
    snake = Snake(SNAKE_COLOR, SNAKE_HEAD_COLOR)
    apple = Apple(APPLE_COLOR, snake.positions)

    while True:
        clock.tick(snake.speed)
        # Обновляем заголовок окна с текущей скоростью.
        pg.display.set_caption(
            f'Змейка | Текущая скорость: {snake.speed} | '
            f'Изменить скорость: (+, -) | Выйти: (Esc)'
        )
        # Обработка событий клавиш.
        new_direction = handle_keys(snake)
        # Обновление направления движения змейки.
        snake.update_direction(new_direction)
        # Движение (модификация списка).
        snake.move()
        # Проверка употребления яблока внутрь змейки:
        if snake.get_head_position() == apple.position:
            # Координаты головы совпали с координатами яблока.
            # Увеличиваем длину.
            snake.length += 1
            # Перемещаем яблоко в свободное место.
            apple.randomize_position(snake.positions)
        # Проверка столкновения с хвостом.
        elif snake.get_head_position() in snake.positions[4:]:
            # Наезд на хвост. Перезапуск.
            snake.reset()  # Сброс змейки.
            screen.fill(BOARD_BACKGROUND_COLOR)  # Очищаем весь экран.
            apple.randomize_position(snake.positions)  # Перемещаем яблоко.

        # Отрисовка змейки.
        snake.draw()
        # Отрисовка яблока.
        apple.draw()
        # Обновление экрана.
        pg.display.update()


if __name__ == '__main__':
    main()
