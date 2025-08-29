import random

from minesweeper import Minesweeper


def test_mine_count():
    rand = random.Random(0)
    game = Minesweeper(5, 5, 3, rand=rand)
    mines = sum(1 for row in game.board for cell in row if cell)
    assert mines == 3


def test_reveal_cascade():
    rand = random.Random(0)
    game = Minesweeper(3, 3, 1, rand=rand)
    game.reveal(0, 0)
    revealed = sum(1 for row in game.revealed for cell in row if cell)
    assert revealed > 1


def test_is_won_after_clearing_safe_cells():
    rand = random.Random(0)
    game = Minesweeper(2, 1, 1, rand=rand)
    game.reveal(0, 0)
    assert game.is_won()
