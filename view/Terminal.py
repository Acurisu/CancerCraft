# -*- coding: utf-8 -*-

# Generic/Built-in
import curses

# Owned
import util
from .window import Bar, Console, Info, Position, XP

# TODO fix output when being piped
class Terminal:
    """
    Class representing and managing the terminal and it's subwindows

    Attributes
    ----------
    stdscr : object
        window object representing the whole screen
    info : Info
        window object managing the info (name, UUID)
    bar : Bar
        window object managing the bar (health, food)
    xp : XP
        window object managing the xp (lvl, gauge)
    position : Position
        window object managing the position (dimension, xyz, yaw/pitch)
    console : Console
        window (pad) object managing the console
    _spacing : int
        style spacing
    _padding : int
        style padding
    """

    _spacing = 2

    _padding = 2
    
    def __init__(self, stdscr):
        """
        Parameters
        ----------
        stdscr : object
            class representing and managing the terminal and it's subwindows
        """
        self.stdscr = stdscr
        self.stdscr.clear()
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(False)

        self.info = Info(self.stdscr, 0, self._spacing, self._padding)
        self.bar = Bar(self.stdscr, 1, self._spacing, self._padding)
        self.xp = XP(self.stdscr, 2, self._spacing, self._padding)
        self.position = Position(self.stdscr, 4, self._spacing, self._padding)

        self.stdscr.refresh()

        self.info.update('N/A', '00000000-0000-0000-0000-000000000000')
        self.xp.update(0, 0)

        self.console = Console()