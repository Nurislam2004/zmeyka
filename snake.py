import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")

# Константы для направлений
DIRECTIONS = {
    pygame.K_UP: (0, -GRID_SIZE),
    pygame.K_DOWN: (0, GRID_SIZE),
    pygame.K_LEFT: (-GRID_SIZE, 0),
    pygame.K_RIGHT: (GRID_SIZE, 0)
}

# Константы для центральной позиции
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Класс GameObject
class GameObject:
    """Базовый класс для всех игровых объектов."""
    def __init__(self, position, body_color):
        """
        Инициализация объекта.
        :param position: Кортеж (x, y) с координатами объекта.
        :param body_color: Цвет объекта в формате RGB.
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """
        Отрисовка объекта на игровом поле.
        :param surface: Поверхность для отрисовки.
        """
        pass

# Класс Apple
class Apple(GameObject):
    """Класс, описывающий яблоко."""
    def __init__(self, snake_positions):
        """
        Инициализация яблока с случайной позицией и красным цветом.
        :param snake_positions: Список позиций змейки, чтобы избежать наложения.
        """
        super().__init__(self.randomize_position(snake_positions), APPLE_COLOR)

    def randomize_position(self, snake_positions):
        """
        Генерация случайной позиции яблока на игровом поле, избегая змейки.
        :param snake_positions: Список позиций змейки.
        :return: Кортеж (x, y) с координатами яблока.
        """
        while True:
            position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if position not in snake_positions:
                return position

    def draw(self, surface):
        """
        Отрисовка яблока на игровом поле.
        :param surface: Поверхность для отрисовки.
        """
        pygame.draw.rect(surface, self.body_color,
                         (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

# Класс Snake
class Snake(GameObject):
    """Класс, описывающий змейку."""
    def __init__(self):
        """Инициализация змейки с начальной позицией, зелёным цветом и длиной 1."""
        super().__init__(CENTER, SNAKE_COLOR)
        self.length = 1
        self.positions = [CENTER]
        self.direction = DIRECTIONS[pygame.K_RIGHT]
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """
        Получение позиции головы змейки.
        :return: Кортеж (x, y) с координатами головы.
        """
        return self.positions[0]

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змейки на одну ячейку в текущем направлении."""
        current_head = self.get_head_position()
        dx, dy = self.direction
        new_head = ((current_head[0] + dx) % SCREEN_WIDTH,
                    (current_head[1] + dy) % SCREEN_HEIGHT)

        # Проверка на столкновение с собой
        if new_head in self.positions[:-1]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()

    def draw(self, surface):
        """
        Отрисовка змейки на игровом поле.
        :param surface: Поверхность для отрисовки.
        """
        for position in self.positions:
            pygame.draw.rect(surface, self.body_color,
                             (position[0], position[1], GRID_SIZE, GRID_SIZE))
        if self.last:
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR,
                             (self.last[0], self.last[1], GRID_SIZE, GRID_SIZE))

    def reset(self):
        """Сброс змейки в начальное состояние."""
        self.length = 1
        self.positions = [CENTER]
        self.direction = DIRECTIONS[pygame.K_RIGHT]
        self.next_direction = None

# Функция для обработки нажатий клавиш
def handle_keys(snake):
    """
    Обработка нажатий клавиш для управления змейкой.
    :param snake: Экземпляр класса Snake.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key in DIRECTIONS:
                new_direction = DIRECTIONS[event.key]
                if (new_direction[0], new_direction[1]) != (-snake.direction[0], -snake.direction[1]):
                    snake.next_direction = new_direction

# Основной игровой цикл
def main():
    """Основная функция игры."""
    clock = pygame.time.Clock()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка на съедение яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple = Apple(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()

        clock.tick(10)

if __name__ == "__main__":
    main()
