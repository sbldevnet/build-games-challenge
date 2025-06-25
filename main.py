import pygame
import sys

# from enum import Enum
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)


class Direction:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class PowerUpEffect:
    HALF_SPEED = "Half Speed"
    DOUBLE_SPEED = "Double Speed"
    DOUBLE_GROWTH = "x2"
    CONFUSION = "Confusion"


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.positions = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.grow = False
        self.double_growth = False
        self.confused = False
        self.speed_mult = 1.0

    def update(self):
        self.direction = self.next_direction
        current_head = self.positions[0]
        new_head = (
            (current_head[0] + self.direction[0]) % GRID_COUNT,
            (current_head[1] + self.direction[1]) % GRID_COUNT,
        )

        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        self.grow = False

    def check_collision(self):
        return self.positions[0] in self.positions[1:]


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.power_up_pos = None  # Initialize power_up_pos
        self.last_move_time = 0  # Track last movement time
        self.active_power_up = None  # Track the currently active power-up
        self.reset()

    def reset(self):
        # Store current difficulty before resetting
        current_difficulty = getattr(self, "difficulty", None)

        self.snake = Snake()
        self.food_pos = self.get_random_position()
        self.power_up = None
        self.power_up_pos = None
        self.score = 0
        self.level = 1
        self.paused = False
        self.game_over = False
        self.difficulty = current_difficulty  # Preserve difficulty when resetting
        self.active_power_up = None
        self.last_move_time = pygame.time.get_ticks()  # Reset movement timer
        self.last_score = 0  # Track last score to detect when score changes

    def get_random_position(self):
        while True:
            pos = (random.randint(0, GRID_COUNT - 1), random.randint(0, GRID_COUNT - 1))
            if pos not in self.snake.positions:
                if self.power_up_pos != pos:
                    return pos

    def spawn_power_up(self):
        # Force spawn a power-up regardless of level
        power_ups = []
        if self.difficulty == "Beginner":
            power_ups = [PowerUpEffect.HALF_SPEED, PowerUpEffect.DOUBLE_GROWTH]
        else:
            power_ups = [
                PowerUpEffect.DOUBLE_SPEED,
                PowerUpEffect.CONFUSION,
                PowerUpEffect.HALF_SPEED,
                PowerUpEffect.DOUBLE_GROWTH,
            ]

        # Always spawn a power-up
        self.power_up = random.choice(power_ups)
        self.power_up_pos = self.get_random_position()

    def handle_input(self):
        keys = pygame.key.get_pressed()

        direction_map = {
            (pygame.K_UP, pygame.K_w): Direction.UP,
            (pygame.K_DOWN, pygame.K_s): Direction.DOWN,
            (pygame.K_LEFT, pygame.K_a): Direction.LEFT,
            (pygame.K_RIGHT, pygame.K_d): Direction.RIGHT,
        }

        for (key1, key2), direction in direction_map.items():
            if keys[key1] or keys[key2]:
                if self.snake.confused:
                    # Invert directions when confused
                    if direction == Direction.UP:
                        new_dir = Direction.DOWN
                    elif direction == Direction.DOWN:
                        new_dir = Direction.UP
                    elif direction == Direction.LEFT:
                        new_dir = Direction.RIGHT
                    else:
                        new_dir = Direction.LEFT
                else:
                    new_dir = direction

                # Prevent 180-degree turns
                if (
                    self.snake.direction[0] * -1,
                    self.snake.direction[1] * -1,
                ) != new_dir:
                    self.snake.next_direction = new_dir

    def update(self):
        # Generate a new power-up every 5 rounds (5th, 10th, etc.)
        if (
            self.score % 5 == 0
            and self.score > 0
            and not self.power_up
            and self.score != self.last_score
        ):
            self.spawn_power_up()

        # Check if score has increased for powerup duration
        if self.score > self.last_score and self.active_power_up:
            # Reset all temporary effects after 1 score
            self.snake.confused = False
            self.snake.speed_mult = 1.0
            self.active_power_up = None  # Clear the active power-up display
            self.snake.double_growth = False

        # Update last_score
        self.last_score = self.score

        # Time-based movement for fluid motion
        current_time = pygame.time.get_ticks()
        move_delay = 1000 / self.get_current_speed()  # Convert speed to milliseconds

        if current_time - self.last_move_time >= move_delay:
            self.snake.update()
            self.last_move_time = current_time

        # Check collisions
        if self.snake.check_collision():
            self.game_over = True
            return

        # Check food collision
        if self.snake.positions[0] == self.food_pos:
            # Apply double score if double_growth is active
            score_increase = 2 if self.snake.double_growth else 1
            self.score += score_increase
            self.level = (self.score // 5) + 1
            self.snake.grow = True
            if self.snake.double_growth:
                self.snake.grow = True  # Will grow again next update
                self.snake.double_growth = False
            self.food_pos = self.get_random_position()

        # Check power-up collision
        if self.power_up and self.snake.positions[0] == self.power_up_pos:
            # Store the active power-up type to display it
            self.active_power_up = self.power_up

            if self.power_up == PowerUpEffect.HALF_SPEED:
                self.snake.speed_mult = 0.5
            elif self.power_up == PowerUpEffect.DOUBLE_SPEED:
                self.snake.speed_mult = 2.0
            elif self.power_up == PowerUpEffect.DOUBLE_GROWTH:
                self.snake.double_growth = True
            elif self.power_up == PowerUpEffect.CONFUSION:
                self.snake.confused = True

            self.power_up = None
            self.power_up_pos = None

    def draw(self):
        self.screen.fill(BLACK)

        # Draw snake
        for i, pos in enumerate(self.snake.positions):
            color = DARK_GREEN if i == 0 else GREEN
            pygame.draw.rect(
                self.screen,
                color,
                (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1),
            )

        # Draw food
        pygame.draw.rect(
            self.screen,
            RED,
            (
                self.food_pos[0] * GRID_SIZE,
                self.food_pos[1] * GRID_SIZE,
                GRID_SIZE - 1,
                GRID_SIZE - 1,
            ),
        )

        # Draw power-up
        if self.power_up:
            color = BLUE  # Always use blue for powerups
            pygame.draw.rect(
                self.screen,
                color,
                (
                    self.power_up_pos[0] * GRID_SIZE,
                    self.power_up_pos[1] * GRID_SIZE,
                    GRID_SIZE - 1,
                    GRID_SIZE - 1,
                ),
            )
            # Add "?" symbol to power-up (smaller size)
            small_font = pygame.font.Font(None, 24)  # Smaller font size
            question_mark = small_font.render("?", True, WHITE)
            question_rect = question_mark.get_rect(
                center=(
                    self.power_up_pos[0] * GRID_SIZE + GRID_SIZE // 2,
                    self.power_up_pos[1] * GRID_SIZE + GRID_SIZE // 2,
                )
            )
            self.screen.blit(question_mark, question_rect)

        # Draw score, level, difficulty and speed
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        diff_text = self.font.render(f"Difficulty: {self.difficulty}", True, WHITE)
        speed_text = self.font.render(
            f"Speed: {self.get_current_speed():.1f}", True, WHITE
        )

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))
        self.screen.blit(diff_text, (10, 90))
        self.screen.blit(speed_text, (10, 130))

        # Display active power-up only after it's collected
        if self.active_power_up:
            power_up_text = self.font.render(
                f"Power-up: {self.active_power_up}", True, BLUE
            )
            self.screen.blit(power_up_text, (10, 170))

        if self.paused:
            pause_text = self.font.render("PAUSED", True, WHITE)
            restart_text = self.font.render("Press R to restart", True, WHITE)

            pause_rect = pause_text.get_rect(
                center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2)
            )
            restart_rect = restart_text.get_rect(
                center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 50)
            )

            self.screen.blit(pause_text, pause_rect)
            self.screen.blit(restart_text, restart_rect)

        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, WHITE)
            restart_text = self.font.render("Press R to restart", True, WHITE)

            game_over_rect = game_over_text.get_rect(
                center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2)
            )
            restart_rect = restart_text.get_rect(
                center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 50)
            )

            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def show_menu(self):
        self.screen.fill(BLACK)

        title = self.font.render("Snake Game", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_SIZE // 2, 100))
        self.screen.blit(title, title_rect)

        difficulties = ["Beginner", "Recommended", "Expert"]
        button_height = 50
        button_width = 200
        spacing = 20

        start_y = (
            WINDOW_SIZE // 2 - (len(difficulties) * (button_height + spacing)) // 2
        )

        mouse_pos = pygame.mouse.get_pos()

        for i, diff in enumerate(difficulties):
            button_rect = pygame.Rect(
                (WINDOW_SIZE - button_width) // 2,
                start_y + i * (button_height + spacing),
                button_width,
                button_height,
            )

            color = GRAY if button_rect.collidepoint(mouse_pos) else WHITE
            pygame.draw.rect(self.screen, color, button_rect, 2)

            text = self.font.render(diff, True, color)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

        pygame.display.flip()
        return difficulties, start_y, button_height, spacing, button_width

    def run(self):
        while True:
            if self.difficulty is None:
                difficulties, start_y, btn_height, spacing, btn_width = self.show_menu()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        for i, diff in enumerate(difficulties):
                            button_rect = pygame.Rect(
                                (WINDOW_SIZE - btn_width) // 2,
                                start_y + i * (btn_height + spacing),
                                btn_width,
                                btn_height,
                            )
                            if button_rect.collidepoint(mouse_pos):
                                self.difficulty = diff
                                break
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r and (self.game_over or self.paused):
                        self.reset()

            if not self.paused and not self.game_over:
                self.handle_input()
                self.update()

            self.draw()
            self.clock.tick(FPS)

    def get_current_speed(self):
        # Calculate speed based on difficulty and level
        base_speed = {"Beginner": 5, "Recommended": 8, "Expert": 12}[self.difficulty]

        # Add level-based speed increase for non-beginner modes
        level_speed = 0 if self.difficulty == "Beginner" else min(self.level * 0.5, 8)
        return max(1, (base_speed + level_speed) * self.snake.speed_mult)


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
