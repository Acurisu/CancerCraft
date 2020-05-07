# -*- coding: utf-8 -*-

# Generic/Built-in
import curses

class Bar:
    """
    Class representing and managing the bar

    Attributes
    ----------
    _health : object
        window object displaying health
    _food : object
        window object displaying food

    Methods
    -------
    update(self, health, food)
        updates health and food display
    """

    def __init__(self, stdscr: object, idx: int, spacing: int, padding: int):
        """
        Parameters
        ----------
        stdscr : object
            class representing and managing the terminal and it's subwindows
        idx : int
            y level index on the screen
        spacing : int
            style spacing
        padding : int
            style padding
        """
        bar_y = idx * spacing

        cols_div_2 = curses.COLS >> 1
        cols_div_4 = curses.COLS >> 2

        bar_width = 2

        health = 'Health: '
        health_x = cols_div_4 - (len(health) + bar_width >> 1)
        stdscr.addstr(bar_y, health_x, health)
        self._health = curses.newwin(1, bar_width + 1, bar_y, health_x + len(health))

        food = 'Food: '
        food_x = cols_div_2 + cols_div_4 - (len(food) + bar_width >> 1)
        stdscr.addstr(bar_y, food_x, food)
        self._food = curses.newwin(1, bar_width + 1, bar_y, food_x + len(food))

    def update(self, health: int, food: int):
        self._health.addstr(0, 0, f'{health:02d}')
        self._food.addstr(0, 0, f'{food:02d}')

        self._health.refresh()
        self._food.refresh()