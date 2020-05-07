# -*- coding: utf-8 -*-

# Generic/Built-in
import curses

class XP:
    """
    Class representing and managing the bar

    Attributes
    ----------
    _health : object
        window object displaying health
    _food : object
        window object displaying food
    _color_pair_green_black : int
        attribute value of fg: green and bg: black
    _width : int
        width of the xp window
    _length : int
        length inside xp gauge
    _xp : object
        window object displaying the gauge frame
    _gauge : object
        window object displaying the gauge
    _lvl : int
        xp level
    _bar : float
        percentage of the xp bar being full

    Methods
    -------
    update(self, xp_bar, lvl)
        updates xp display
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
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self._color_pair_green_black = curses.color_pair(2)

        # curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        # self._color_pair_black_green = curses.color_pair(1)

        xp_y = idx * spacing
        self._width = curses.COLS - (padding << 1)
        self._length = self._width - 4
        self._xp = curses.newwin(3, self._width, xp_y, padding)

        self._gauge = curses.newwin(1, self._width - 2, xp_y + 1, padding + 1)

        self._lvl = -1
        self._bar = 0

    def update(self, xp_bar: float, lvl: int):
        if not lvl == self._lvl or xp_bar < self._bar:
            self._xp.box()

            if not lvl == 0:
                level = f' Lvl {lvl:02d} '
                level_y = self._width - len(level) >> 1
                self._xp.addstr(0, level_y, level)

            self._xp.refresh()
            self._lvl = lvl

        progress = round(self._length * xp_bar)
        self._gauge.addstr(0, 1, '▉' * progress, self._color_pair_green_black)
        # self._gauge.addstr(0, 1, ' ' * progress, self._color_pair_black_green)
        self._gauge.refresh()
        self._bar = xp_bar