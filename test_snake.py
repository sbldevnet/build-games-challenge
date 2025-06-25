import pytest
import pygame
from main import Snake, Direction, GRID_COUNT, Game, PowerUpEffect


def test_snake_initialization():
    snake = Snake()
    assert len(snake.positions) == 1
    assert snake.direction == Direction.RIGHT
    assert snake.next_direction == Direction.RIGHT
    assert not snake.grow
    assert not snake.confused
    assert not snake.double_growth
    assert snake.speed_mult == 1.0


def test_snake_movement():
    snake = Snake()
    initial_pos = snake.positions[0]
    snake.update()
    new_pos = snake.positions[0]

    # Snake should move right by default
    assert new_pos[0] == (initial_pos[0] + 1) % GRID_COUNT
    assert new_pos[1] == initial_pos[1]


def test_snake_growth():
    snake = Snake()
    initial_length = len(snake.positions)
    snake.grow = True
    snake.update()
    assert len(snake.positions) == initial_length + 1


def test_snake_collision():
    snake = Snake()
    # Create a collision by making the snake turn back on itself
    snake.positions = [(5, 5), (6, 5), (5, 5)]
    assert snake.check_collision() == True


def test_double_growth():
    snake = Snake()
    initial_length = len(snake.positions)
    snake.double_growth = True
    snake.grow = True
    snake.update()
    snake.grow = True  # Simulating second growth from double growth
    snake.update()
    assert len(snake.positions) == initial_length + 2


def test_speed_calculation():
    game = Game()
    game.difficulty = "Beginner"
    assert game.get_current_speed() == 5  # Base speed for beginner

    game.difficulty = "Expert"
    game.level = 1
    assert game.get_current_speed() == 12.5  # Base speed (12) + level_speed (0.5)

    game.level = 10
    # Expert speed should be base (12) + min(level * 0.5, 8) = 12 + 5 = 17
    assert game.get_current_speed() == 17


def test_half_speed_power_up():
    game = Game()
    game.difficulty = "Recommended"
    game.snake.positions = [(5, 5)]
    game.power_up_pos = (5, 5)
    game.power_up = PowerUpEffect.HALF_SPEED
    game.update()
    assert game.snake.speed_mult == 0.5


def test_double_speed_power_up():
    game = Game()
    game.difficulty = "Recommended"
    game.snake.positions = [(5, 5)]
    game.power_up_pos = (5, 5)
    game.power_up = PowerUpEffect.DOUBLE_SPEED
    game.update()
    assert game.snake.speed_mult == 2.0


def test_confusion_power_up():
    game = Game()
    game.difficulty = "Recommended"
    game.snake.positions = [(5, 5)]
    game.power_up_pos = (5, 5)
    game.power_up = PowerUpEffect.CONFUSION
    game.update()
    assert game.snake.confused == True


def test_double_growth_power_up():
    game = Game()
    game.difficulty = "Recommended"
    game.snake.positions = [(5, 5)]
    game.power_up_pos = (5, 5)
    game.power_up = PowerUpEffect.DOUBLE_GROWTH
    game.update()
    assert game.snake.double_growth == True


def test_game_reset():
    game = Game()
    game.difficulty = "Expert"
    game.score = 10
    game.level = 3
    game.snake.positions = [(5, 5), (6, 5), (7, 5)]
    game.active_power_up = PowerUpEffect.CONFUSION
    game.snake.confused = True

    game.reset()

    assert game.score == 0
    assert game.level == 1
    assert len(game.snake.positions) == 1
    assert game.difficulty == "Expert"  # Difficulty should be preserved
    assert game.active_power_up is None
    assert not game.snake.confused


def test_game_over_collision():
    game = Game()
    game.difficulty = "Beginner"
    # Create a collision scenario
    game.snake.positions = [(5, 5), (6, 5), (5, 5)]

    game.update()

    assert game.game_over == True


def test_food_collision():
    game = Game()
    game.difficulty = "Recommended"
    game.food_pos = (5, 5)
    game.snake.positions = [(5, 5)]
    initial_score = game.score

    game.update()

    assert game.score == initial_score + 1
    assert game.snake.grow == True
    assert game.food_pos != (5, 5)  # Food should have moved


def test_spawn_power_up():
    game = Game()
    game.difficulty = "Expert"

    # Force spawn a power-up
    game.spawn_power_up()

    assert game.power_up is not None
    assert game.power_up_pos is not None
    assert game.power_up in [
        PowerUpEffect.DOUBLE_SPEED,
        PowerUpEffect.CONFUSION,
        PowerUpEffect.HALF_SPEED,
        PowerUpEffect.DOUBLE_GROWTH,
    ]


def test_handle_input():
    game = Game()
    game.difficulty = "Recommended"
    game.snake.direction = Direction.RIGHT

    # Create a proper mock for pygame.key.get_pressed
    original_get_pressed = pygame.key.get_pressed

    # Mock that returns True only for UP key
    def mock_get_pressed():
        keys = [
            False
        ] * 1073742000  # Create a list with enough elements for all key constants
        keys[pygame.K_UP] = True
        return keys

    pygame.key.get_pressed = mock_get_pressed

    try:
        game.handle_input()
        assert game.snake.next_direction == Direction.UP
    finally:
        # Restore the original function
        pygame.key.get_pressed = original_get_pressed


def test_confused_input():
    game = Game()
    game.difficulty = "Expert"
    game.snake.direction = Direction.RIGHT
    game.snake.confused = True

    # Create a proper mock for pygame.key.get_pressed
    original_get_pressed = pygame.key.get_pressed

    # Mock that returns True only for UP key
    def mock_get_pressed():
        keys = [
            False
        ] * 1073742000  # Create a list with enough elements for all key constants
        keys[pygame.K_UP] = True
        return keys

    pygame.key.get_pressed = mock_get_pressed

    try:
        game.handle_input()
        assert game.snake.next_direction == Direction.DOWN
    finally:
        # Restore the original function
        pygame.key.get_pressed = original_get_pressed


def test_power_up_duration():
    game = Game()
    game.difficulty = "Recommended"
    game.active_power_up = PowerUpEffect.HALF_SPEED
    game.snake.speed_mult = 0.5
    game.score = 5
    game.last_score = 4  # Simulate score increase

    game.update()

    assert game.active_power_up is None
    assert game.snake.speed_mult == 1.0


def test_level_calculation():
    game = Game()
    game.difficulty = "Expert"

    # Simulate eating food to update level
    game.snake.positions = [(5, 5)]
    game.food_pos = (5, 5)
    game.score = 4  # Starting at 4, will become 5 after eating food
    game.update()
    assert game.level == 2  # Level should be (5 // 5) + 1 = 2

    # Test another level increase
    game.snake.positions = [(6, 6)]
    game.food_pos = (6, 6)
    game.score = 9  # Will become 10 after eating food
    game.update()
    assert game.level == 3  # Level should be (10 // 5) + 1 = 3
