# -*- coding: utf-8 -*-

# Generic/Built-in
import curses

# TODO move to helper
dimensions = { -1: 'Nether', 0: 'Overworld', 1: 'End'}
############

class Position:
    """
    Class representing and managing the bar

    Attributes
    ----------
    _dimension : object
        window object displaying health
    _xyz : object
        window object displaying xyz
    _facing : object
        window object displaying facing (yaw / pitch)

    Methods
    -------
    update_dimension(self, dimension)
        updates dimension display
    update_xyz(self, x, y, z)
        updates xyz display
    update_facing(self, yaw, pitch)
        updates facing (yaw / pitch) display
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
        pos_y = idx * spacing
        
        dimension = 'Dimension: '
        dimension_width = len(dimensions[0])
        stdscr.addstr(pos_y, padding, dimension)
        self._dimension = curses.newwin(1, dimension_width + 1, pos_y, len(dimension) + padding)

        pos_y += 1

        xyz = 'XYZ: '
        xyz_width = curses.COLS - len(xyz) - (padding << 1)
        stdscr.addstr(pos_y, padding, xyz)
        self._xyz = curses.newwin(1, xyz_width + 1, pos_y, len(xyz) + padding)

        pos_y += 1

        facing = 'Facing: '
        facing_width = curses.COLS - len(facing) - (padding << 1)
        stdscr.addstr(pos_y, padding, facing)
        self._facing = curses.newwin(1, facing_width + 1, pos_y, len(facing) + padding)

    def update_dimension(self, dimension: int):
        self._dimension.addstr(0, 0, dimensions[dimension])

        self._dimension.refresh()

    def update_xyz(self, x: float, y: float, z: float):
        self._xyz.addstr(0, 0, f'{x:f} / {y:f} / {z:f}')

        self._xyz.refresh()

    def update_facing(self, yaw: float, pitch: float):
        self._facing.addstr(0, 0, f'{yaw:f} / {pitch:f}')

        self._facing.refresh()