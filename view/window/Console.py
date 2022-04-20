# -*- coding: utf-8 -*-

# Generic/Built-in
import curses

# Owned
import util

class Console:
    """
    Class representing a console pad on the screen

    Attributes
    ----------
    _height : int
        height of the console (including frame)
    _max_lines : int
        max lines of the buffer
    _min_line : int
        min scrollback line (used for scroll fix)
    _current_line : int
        current line to be displayed
    _max_line : int
        max scrollback line (used for scroll fix)
    _pad : object
        pad object representing the console

    Methods
    -------
    scroll_up(self)
        scrolls the displaye area of the pad up
    scroll_down(self)
        scrolls the displaye area of the pad down
    log(self, string)
        writes log output to the buffer
    """

    _height = 12

    _max_lines = 1000
    _min_line = -_height + 2 + 1
    _current_line =  _min_line
    _max_line = _max_lines - _height + 2 - 1

    def __init__(self):
        frame = curses.newwin(self._height, curses.COLS, curses.LINES - self._height, 0)
        frame.box()
        frame.refresh()

        self._pad = curses.newpad(self._max_lines, curses.COLS - 2)
        self._pad.scrollok(True)

    def scroll_up(self):
        if self._current_line == self._min_line:
            return

        self._current_line = self._current_line - 1
        self._pad.refresh(0 if self._current_line < 0 else self._current_line, 0, curses.LINES - self._height + 1, 1, curses.LINES - 2, curses.COLS - 1)

    def scroll_down(self):
        if self._current_line == self._max_line:
            return

        self._current_line = self._current_line + 1
        self._pad.refresh(0 if self._current_line < 0 else self._current_line, 0, curses.LINES - self._height + 1, 1, curses.LINES - 2, curses.COLS - 1)

    def log(self, string: str):
        self.print(f'[LOG] {string:s}')

    def print(self, string: str):
        # TODO add colors
        self._pad.addstr(f'[{util.get_time():s}] {string:s}\n')
        self._pad.refresh(0 if self._current_line < 0 else self._current_line, 0, curses.LINES - self._height + 1, 1, curses.LINES - 2, curses.COLS - 1)
        if (self._current_line < self._max_line):
            self._current_line = self._current_line + 1
