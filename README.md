# Snake Game

> [!NOTE]
> This project is part of the Amazon Build Games Challenge. Learn more at [samuelburgos.dev](https://samuelburgos.dev/blog/202506_games_challenge/)

A classic Snake game implementation in Python using Pygame.

## Overview

This is a modern take on the classic Snake game, featuring multiple difficulty levels and power-ups. The game is built using Python and the Pygame library.

## How to Use

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the game:
   ```bash
   python main.py
   ```

## Features

- Three difficulty levels: Beginner, Recommended, and Expert
- Power-up system with both beneficial and challenging effects
- Pause functionality
- Keyboard controls (Arrow keys or WASD)

## Controls

- Arrow keys or WASD: Control snake direction
- ESC: Pause game
- R: Restart the game

## Difficulty Levels

1. **Beginner**
   - Normal speed
   - No speed increase over time
   - No bad power-ups

2. **Recommended**
   - Normal starting speed
   - Speed increases over time
   - Both good and bad power-ups (50% probability)

3. **Expert**
   - High starting speed
   - Speed increases over time
   - Both good and bad power-ups (65% probability)

## Power-ups

Power-ups spawn every 5 levels in random locations. There are two categories:

### Good Power-ups
- Half Speed: Reduces speed by 50% for the current turn
- 2x1: Gain 2 snake segments instead of 1 on next food collection

### Bad Power-ups
- Double Speed: Doubles speed for the current turn
- Confusion: Inverts directional controls for the current turn

## Code Structure

The game is organized into several Python modules:
- `main.py`: Entry point and game initialization
- `game.py`: Core game logic and main game loop
- `snake.py`: Snake class and movement logic
- `powerup.py`: Power-up system implementation
