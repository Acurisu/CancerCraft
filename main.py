# -*- coding: utf-8 -*-

# Generic/Built-in
import curses
import re
from os import path
from argparse import ArgumentParser
from getpass import getpass

# Owned
import util
from view import Terminal
from BotWrapper import BotWrapper

__author__ = "Acurisu"
__copyright__ = "Copyright 2020, Acurisu"
__credits__ = ["Acurisu"]

__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Acurisu"
__email__ = "acurisu@gmail.com"
__status__ = "Dev"

def get_options():
    """
    Parses all required arguments either from command-line input
    or terminal prompts
    """
    parser = ArgumentParser(prog="CancerCraft")
    auth_type = parser.add_subparsers(dest='auth_type', help='choose either Mojang or MCLeaks as authentication type')

    auth_type_Mojang = auth_type.add_parser('Mojang', help='Mojang authentication')
    auth_type_Mojang.add_argument('-u', '--user', dest='username', type=str, help='Mojang username', default=None)
    auth_type_Mojang.add_argument('-p', '--pass', dest='password', type=str, help='Mojang password', default=None)

    auth_type_MCLeaks = auth_type.add_parser('MCLeaks', help='MCLeaks authentication')
    auth_type_MCLeaks.add_argument('-n', '--name', dest='name', type=str, help='name of the cached MCLeaks account (leave blank to use a new one)', default=None)

    parser.add_argument('-s', '--server', dest='server', type=str, help='server host or host:port (enclose IPv6 addresses in square brackets)', default=None)

    parser.add_argument('-b', '--bot', dest='bot_path', type=str, help='relative/absoulte path of the bot file (relative path from: ./bots)', default=None)

    parser.add_argument('-i', '--ignore', dest='ignore', action='store_true', help='will assume that non-required variables such as \'name\' were left blank on purpose and thus ignore them', default=False)

    options = parser.parse_args()

    if not options.auth_type:
        options.auth_type = input('Enter the desired authentication type (Mojang | MCLeaks): ')
        
    # TODO maybe don't be case-sensitive
    if options.auth_type == 'Mojang':
        if not hasattr(options, 'username') or not options.username: # TODO maybe use 'easier to ask for forgiveness than permission' (EAFP) over 'look before you leap' (LBYL)
            options.username = input('Enter your username: ')

        if not hasattr(options, 'password') or not options.password:
            options.password = getpass('Enter your password: ') # TODO add 'leave blank for offline mode' (combined with -b)
    elif options.auth_type == 'MCLeaks':
        if not hasattr(options, 'name') or not options.name:
            if options.ignore:
                options.name = None
            else:
                options.name = input('Enter the name of a cached MCLeaks account (leave blank to use a new one): ')
    else:
        raise ValueError(f'Invalid authentication type: \'{options.auth_type:s}\'')

    if not options.server:
        options.server = input('Enter server host or host:port (enclose IPv6 addresses in square brackets): ')

    match = re.match(r'((?P<host>[^\[\]:]+)|\[(?P<addr>[^\[\]]+)\])'
                     r'(:(?P<port>\d+))?$', options.server)

    if match is None:
        raise ValueError('Invalid server address: \'{options.server:s}\'')

    options.address = match.group('host') or match.group('addr')
    options.port = int(match.group('port') or 25565)

    if not options.ignore:
        if not options.bot_path:
            options.bot_path = input('Enter the relative/absoulte path of the bot file (relative path from: ./bots): ')

    if options.bot_path:
        directory = path.dirname(path.realpath(__file__))
        if not options.bot_path.endswith('.py'):
            options.bot_path += '.py'

        if path.isfile(f'{directory:s}/bots/{options.bot_path:s}'):
            options.bot_path = f'{directory:s}/bots/{options.bot_path:s}'
        elif not path.isfile(options.bot_path):
            raise ValueError(f'Invalid bot file path: \'{options.bot_path:s}\'')

        options.Bot = util.import_file('Bot', options.bot_path).Bot
        

    # TODO implement
    if options.auth_type == 'MCLeaks':
        raise NotImplementedError
    ############

    return options

def curse(stdscr: object, options: object):
    """
    Initialize terminal and bot_wrapper

    Parameters
    ----------
    stdscr : object
        window object representing the whole screen
    options : object
        options parsed by the argument parser
    """
    terminal = Terminal(stdscr)
    bot_wrapper = BotWrapper(terminal, options)

if __name__ == '__main__':
    options = get_options()
    curses.wrapper(curse, options)