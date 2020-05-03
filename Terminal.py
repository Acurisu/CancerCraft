import curses

# TODO move to helper
from datetime import datetime

def get_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

dimensions = { -1: 'Nether', 0: 'Overworld', 1: 'End'}
############

# TODO fix output when being piped
class Terminal:
    _spacing = 2

    _padding = 2

    # TODO just use a class already
    _console_height = 12

    _console_max_lines = 1000
    _console_min_line = -_console_height + 2 + 1
    _console_current_line =  _console_min_line
    _console_max_line = _console_max_lines - _console_height + 2 - 1
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(False)

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        self._color_pair_black_green = curses.color_pair(1)

        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self._color_pair_green_black = curses.color_pair(2)

        self._cols_div_2 = curses.COLS >> 1
        self._cols_div_4 = self._cols_div_2 >> 1

        self._init_info()
        self._init_bar()
        self._init_xp()
        self._init_pos()

        self.stdscr.refresh()

        self.update_info('N/A', '00000000-0000-0000-0000-000000000000')
        self.update_xp(0, 0)

        self.frame = curses.newwin(self._console_height, curses.COLS, curses.LINES - self._console_height, 0)
        self.frame.box()
        self.frame.refresh()

        self._console = curses.newpad(self._console_max_lines, curses.COLS - 2)
        self._console.scrollok(True)

    def _init_info(self):
        info_y = 0 * self._spacing

        name = 'Name: '
        self._name_length_max = 16 # min is 3 (https://help.minecraft.net/hc/en-us/articles/360034636712-Minecraft-Usernames)
        name_x = self._cols_div_4 - (len(name) + self._name_length_max >> 1)
        self.stdscr.addstr(info_y, name_x, name)
        self._name = curses.newwin(1, self._name_length_max + 1, info_y, name_x + len(name))

        uuid = 'UUID: '
        uuid_length = 36 # 8-4-4-4-12 (https://tools.ietf.org/html/rfc4122#section-3)
        uuid_x = self._cols_div_2 + self._cols_div_4 - (len(uuid) + uuid_length >> 1)
        self.stdscr.addstr(info_y, uuid_x, uuid)
        self._uuid = curses.newwin(1, uuid_length + 1, info_y, uuid_x + len(uuid))

    def _init_bar(self):
        bar_y = 1 * self._spacing
        bar_width = 2

        health = 'Health: '
        health_x = self._cols_div_4 - (len(health) + bar_width >> 1)
        self.stdscr.addstr(bar_y, health_x, health)
        self._health = curses.newwin(1, bar_width + 1, bar_y, health_x + len(health))

        food = 'Food: '
        food_x = self._cols_div_2 + self._cols_div_4 - (len(food) + bar_width >> 1)
        self.stdscr.addstr(bar_y, food_x, food)
        self._food = curses.newwin(1, bar_width + 1, bar_y, food_x + len(food))

    def _init_xp(self):
        xp_y = 2 * self._spacing
        self._xp_width = curses.COLS - (self._padding << 1)
        self._xp_length = self._xp_width - 4
        self._xp = curses.newwin(3, self._xp_width, xp_y, self._padding)

        self._xp_gauge = curses.newwin(1, self._xp_width - 2, xp_y + 1, self._padding + 1)

        self._xp_level = -1
        self._xp_bar = 0

    def _init_pos(self):
        pos_y = 4 * self._spacing
        
        dimension = 'Dimension: '
        dimension_width = len(dimensions[0])
        self.stdscr.addstr(pos_y, self._padding, dimension)
        self._dimension = curses.newwin(1, dimension_width + 1, pos_y, len(dimension) + self._padding)

        pos_y = pos_y + 1

        xyz = 'XYZ: '
        xyz_width = curses.COLS - len(xyz) - (self._padding << 1)
        self.stdscr.addstr(pos_y, self._padding, xyz)
        self._xyz = curses.newwin(1, xyz_width + 1, pos_y, len(xyz) + self._padding)

        pos_y = pos_y + 1

        facing = 'Facing: '
        facing_width = curses.COLS - len(facing) - (self._padding << 1)
        self.stdscr.addstr(pos_y, self._padding, facing)
        self._facing = curses.newwin(1, facing_width + 1, pos_y, len(facing) + self._padding)
        
    def update_info(self, name, uuid):
        self._name.addstr(0, self._name_length_max - len(name) >> 1, name)
        self._uuid.addstr(0, 0, uuid)

        self._name.refresh()
        self._uuid.refresh()

    def update_bar(self, health, food):
        self._health.addstr(0, 0, f'{health:02d}')
        self._food.addstr(0, 0, f'{food:02d}')

        self._health.refresh()
        self._food.refresh()

    def update_xp(self, xp_bar, lvl):
        if not lvl == self._xp_level or xp_bar < self._xp_bar:
            self._xp.box()

            if not lvl == 0:
                level = f' Lvl {lvl:02d} '
                level_y = self._xp_width - len(level) >> 1
                self._xp.addstr(0, level_y, level)

            self._xp.refresh()
            self._xp_level = lvl

        progress = round(self._xp_length * xp_bar)
        self._xp_gauge.addstr(0, 1, '▉' * progress, self._color_pair_green_black)
        # self._xp_gauge.addstr(0, 1, ' ' * progress, self._color_pair_black_green)
        self._xp_gauge.refresh()
        self._xp_bar = xp_bar

    def update_dimension(self, dimension):
        self._dimension.addstr(0, 0, dimensions[dimension])

        self._dimension.refresh()

    def update_xyz(self, x, y, z):
        self._xyz.addstr(0, 0, f'{x:f} / {y:f} / {z:f}')

        self._xyz.refresh()

    def update_facing(self, yaw, pitch):
        self._facing.addstr(0, 0, f'{yaw:f} / {pitch:f}')

        self._facing.refresh()

    def scroll_up(self):
        if self._console_current_line == self._console_min_line:
            return

        self._console_current_line = self._console_current_line - 1
        self._console.refresh(0 if self._console_current_line < 0 else self._console_current_line, 0, curses.LINES - self._console_height + 1, 1, curses.LINES - 2, curses.COLS - 1)

    def scroll_down(self):
        if self._console_current_line == self._console_max_line:
            return

        self._console_current_line = self._console_current_line + 1
        self._console.refresh(0 if self._console_current_line < 0 else self._console_current_line, 0, curses.LINES - self._console_height + 1, 1, curses.LINES - 2, curses.COLS - 1)


    def log(self, string):
        # TODO add colors
        self._console.addstr(f'[{get_time():s}] [LOG] {string:s}\n')
        self._console.refresh(0 if self._console_current_line < 0 else self._console_current_line, 0, curses.LINES - self._console_height + 1, 1, curses.LINES - 2, curses.COLS - 1)
        if (self._console_current_line < self._console_max_line):
            self._console_current_line = self._console_current_line + 1