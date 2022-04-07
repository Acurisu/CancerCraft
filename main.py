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
__version__ = "0.2.0"
__maintainer__ = "Acurisu"
__email__ = "acurisu@gmail.com"
__status__ = "Dev"

def get_options():
    """
    Parses all required arguments either from command-line input
    or terminal prompts
    """
    parser = ArgumentParser(prog="CancerCraft")

    parser.add_argument('-cid', '--client-id', dest='client_id', type=str, help='Azure App Client ID', default=None)
    parser.add_argument('-cs', '--client-secret', dest='client_secret', type=str, help='Azure App Client Secret', default=None)
    parser.add_argument('-r', '--redirect-port', dest='redirect_port', type=int, help='Redirect URL for the authentication process', default=6969)
    parser.add_argument('-a', '--auth-code', dest='auth_code', type=str, help='Sets the auth code needed to authenticate without a browser, enter an empty string to get it', default=None)

    parser.add_argument('-s', '--server', dest='server', type=str, help='server host or host:port (enclose IPv6 addresses in square brackets)', default=None)

    parser.add_argument('-b', '--bot', dest='bot_path', type=str, help='relative/absoulte path of the bot file (relative path from: ./bots)', default=None)

    parser.add_argument('-i', '--ignore', dest='ignore', action='store_true', help='will assume that non-required variables such as \'name\' were left blank on purpose and thus ignore them', default=False)

    options = parser.parse_args()

    if not options.client_id:
        options.client_id = input('Enter an Azure App Client ID: ') # TODO check uuid format

    if not options.auth_code == "":
        if not options.client_secret:
            options.client_secret = getpass('Enter an Azure App Client Secret: ')

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