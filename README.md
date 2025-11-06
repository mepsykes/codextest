# codextest

## Flappy Face

A light-hearted Flappy Bird style game that replaces the bird with a cartoon rendition of the provided face. Built with [pygame](https://www.pygame.org/).

### How to play

1. Install dependencies (pygame):
   ```bash
   pip install pygame
   ```
2. Run the game:
   ```bash
   python flappy_face.py
   ```
3. Press <kbd>Space</kbd>, <kbd>Up</kbd>, or click to flap. Avoid the pipes and keep flying!

### Controls

- **Space / Up Arrow / Left Click**: flap upward
- **When game over**: press Space or click to restart

### Notes

- The face sprite is generated procedurally at runtime, inspired by the supplied image.
- Designed for quick experimentation; tweak constants at the top of `flappy_face.py` to adjust difficulty.
