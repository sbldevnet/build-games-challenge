# Application Requirements

## Overview
Implement the classic Snake retro game.

## Requirements
- The application must use a supported python version.
- The application must use `pygame` python library.
- The game must be controled using keyboard keys.
  - Arrows or `wasd` will control the snake direction.
- Keep the code as simple as possible.
- The code must have a `README.md` file with an overview and explanations about the game and some code logic.

## Features
- Implements the core snake game functionality.
- Before starting the game display a screen with the following information:
  - Difficulty level selector: ["Expert", "Recommended", "Beginner"].
  - Start button: this will start the game.
- Pause the game when using `Esc` key.

## Details

### Basic flow
- Each time you eat, you score a point.
- Every 5 points, you level up.

### Difficulty level selector
The level of difficulty will change the complexity of the game depending on the level:
- Beginner: Normal speed. No incremental speed. No bad Power Ups.
- Recommended: Normal speed. Incremental speed. Bad and good.
- Expert: High speed. Incremental speed. Bad and good power ups.

### Power Ups
- Each 5 levels, a random unused cell will spawn a Power Up.
- There are two Power Up categories: `Good` and `Bad`.
- Power Ups can belong to only one category.
- Available Power Ups:
  - Half speed.
    - Category: `Good`.
    - Description: this will reduce the speed to the half during the current turn.
  - 2x1.
    - Category: `Good`.
    - Description: this will obtain 2 parts instead of 1 when obtaining the next part.
  - Double speed.
    - Category: `Bad`.
    - Description: this will increment the speed to the double during the current turn.
  - Confusion.
    - Category: `Bad`.
    - Description: This will invert the up/down right/left controls during the current turn.
