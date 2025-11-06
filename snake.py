import curses
import random
import time

SNAKE_CHAR = '#'
FOOD_CHAR = '*'
INITIAL_DELAY = 0.15
MIN_DELAY = 0.05
DELAY_DECREASE = 0.005

DIRECTIONS = {
    curses.KEY_UP: (-1, 0),
    curses.KEY_DOWN: (1, 0),
    curses.KEY_LEFT: (0, -1),
    curses.KEY_RIGHT: (0, 1),
}


def create_food(height: int, width: int, snake):
    """Return a random location for food that's not on the snake."""
    while True:
        position = (random.randint(1, height - 2), random.randint(1, width - 2))
        if position not in snake:
            return position


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    stdscr.clear()

    height, width = stdscr.getmaxyx()
    center_y, center_x = height // 2, width // 2
    snake = [(center_y, center_x + i) for i in range(3)][::-1]
    direction = DIRECTIONS[curses.KEY_RIGHT]
    food = create_food(height, width, snake)
    score = 0
    delay = INITIAL_DELAY

    while True:
        stdscr.clear()
        stdscr.border()
        stdscr.addstr(0, 2, f" Score: {score} ")
        stdscr.addstr(0, width - 17, " q to quit ")

        for y, x in snake:
            stdscr.addch(y, x, SNAKE_CHAR)

        fy, fx = food
        stdscr.addch(fy, fx, FOOD_CHAR)
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key in DIRECTIONS:
            new_direction = DIRECTIONS[key]
            if (new_direction[0] != -direction[0]) or (new_direction[1] != -direction[1]):
                direction = new_direction

        head_y, head_x = snake[0]
        dy, dx = direction
        new_head = (head_y + dy, head_x + dx)

        if (
            new_head[0] in (0, height - 1)
            or new_head[1] in (0, width - 1)
            or new_head in snake
        ):
            stdscr.nodelay(False)
            stdscr.addstr(height // 2, width // 2 - 5, "Game Over!")
            stdscr.addstr(height // 2 + 1, width // 2 - 9, f"Final Score: {score}")
            stdscr.addstr(height // 2 + 2, width // 2 - 12, "Press any key to exit")
            stdscr.refresh()
            stdscr.getch()
            break

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            delay = max(MIN_DELAY, delay - DELAY_DECREASE)
            food = create_food(height, width, snake)
        else:
            snake.pop()

        time.sleep(delay)


if __name__ == "__main__":
    curses.wrapper(main)
