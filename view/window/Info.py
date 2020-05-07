# -*- coding: utf-8 -*-

# Generic/Built-in
import curses

class Info:
    """
    Class representing and managing the info

    Attributes
    ----------
    _name_length_max : int
        Minecraft username max length
    _name : object
        window object displaying name
    _uuid : object
        window object displaying uuid

    Methods
    -------
    update(self, name, uuid)
        updates name and uuid display
    """

    _name_length_max = 16 # min is 3 (https://help.minecraft.net/hc/en-us/articles/360034636712-Minecraft-Usernames)

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
        info_y = idx * spacing

        cols_div_2 = curses.COLS >> 1
        cols_div_4 = curses.COLS >> 2

        name = 'Name: '
        name_x = cols_div_4 - (len(name) + self._name_length_max >> 1)
        stdscr.addstr(info_y, name_x, name)
        self._name = curses.newwin(1, self._name_length_max + 1, info_y, name_x + len(name))

        uuid = 'UUID: '
        uuid_length = 36 # 8-4-4-4-12 (https://tools.ietf.org/html/rfc4122#section-3)
        uuid_x = cols_div_2 + cols_div_4 - (len(uuid) + uuid_length >> 1)
        stdscr.addstr(info_y, uuid_x, uuid)
        self._uuid = curses.newwin(1, uuid_length + 1, info_y, uuid_x + len(uuid))

    def update(self, name: str, uuid: str):
        self._name.addstr(0, self._name_length_max - len(name) >> 1, name)
        self._uuid.addstr(0, 0, uuid)

        self._name.refresh()
        self._uuid.refresh()