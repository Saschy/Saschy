"""Simple command-line Minesweeper game.
"""

from __future__ import annotations

import random
from typing import Iterable, List, Tuple, Optional


class Minesweeper:
    """Represents a Minesweeper game board."""

    def __init__(self, width: int, height: int, mines: int, rand: Optional[random.Random] = None):
        if mines >= width * height:
            raise ValueError("Number of mines must be less than total cells")
        self.width = width
        self.height = height
        self.mines = mines
        self.rand = rand or random.Random()

        self.board: List[List[bool]] = [[False for _ in range(width)] for _ in range(height)]
        self.revealed: List[List[bool]] = [[False for _ in range(width)] for _ in range(height)]
        self.flags: List[List[bool]] = [[False for _ in range(width)] for _ in range(height)]

        positions = [(x, y) for x in range(width) for y in range(height)]
        for mx, my in self.rand.sample(positions, mines):
            self.board[my][mx] = True

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbors(self, x: int, y: int) -> Iterable[Tuple[int, int]]:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny):
                    yield nx, ny

    def adjacent_mines(self, x: int, y: int) -> int:
        return sum(1 for nx, ny in self.neighbors(x, y) if self.board[ny][nx])

    def reveal(self, x: int, y: int) -> int:
        """Reveal a cell. Returns -1 if a mine was revealed, otherwise the count of adjacent mines."""
        if not self.in_bounds(x, y) or self.revealed[y][x] or self.flags[y][x]:
            return 0
        self.revealed[y][x] = True
        if self.board[y][x]:
            return -1
        count = self.adjacent_mines(x, y)
        if count == 0:
            for nx, ny in self.neighbors(x, y):
                if not self.revealed[ny][nx]:
                    self.reveal(nx, ny)
        return count

    def flag(self, x: int, y: int) -> None:
        if self.in_bounds(x, y) and not self.revealed[y][x]:
            self.flags[y][x] = not self.flags[y][x]

    def is_won(self) -> bool:
        for y in range(self.height):
            for x in range(self.width):
                if not self.board[y][x] and not self.revealed[y][x]:
                    return False
        return True

    def display(self, reveal_mines: bool = False) -> str:
        lines: List[str] = []
        for y in range(self.height):
            row: List[str] = []
            for x in range(self.width):
                if self.flags[y][x]:
                    row.append('F')
                elif not self.revealed[y][x]:
                    if reveal_mines and self.board[y][x]:
                        row.append('*')
                    else:
                        row.append('.')
                elif self.board[y][x]:
                    row.append('*')
                else:
                    count = self.adjacent_mines(x, y)
                    row.append(str(count) if count > 0 else ' ')
            lines.append(' '.join(row))
        return '\n'.join(lines)


def play() -> None:
    """Start an interactive Minesweeper session."""
    import argparse

    parser = argparse.ArgumentParser(description="Play Minesweeper")
    parser.add_argument("--width", type=int, default=9, help="Board width")
    parser.add_argument("--height", type=int, default=9, help="Board height")
    parser.add_argument("--mines", type=int, default=10, help="Number of mines")
    args = parser.parse_args()

    game = Minesweeper(args.width, args.height, args.mines)

    while True:
        print(game.display())
        cmd = input("Command (r x y to reveal, f x y to flag, q to quit): ").strip().split()
        if not cmd:
            continue
        action = cmd[0].lower()
        if action == 'q':
            print("Goodbye!")
            break
        if len(cmd) != 3 or action not in {'r', 'f'}:
            print("Invalid command")
            continue
        try:
            x, y = int(cmd[1]), int(cmd[2])
        except ValueError:
            print("Invalid coordinates")
            continue
        if action == 'r':
            result = game.reveal(x, y)
            if result == -1:
                print("Boom! You hit a mine.")
                print(game.display(reveal_mines=True))
                break
        else:
            game.flag(x, y)
        if game.is_won():
            print("Congratulations! You cleared the field.")
            print(game.display(reveal_mines=True))
            break


if __name__ == "__main__":
    play()
