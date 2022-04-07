# -*- coding: utf-8 -*-

# Generic/Built-in
import sys
import inspect
import json
import re
from time import sleep

# ammaraskar/pyCraft
from minecraft.networking.connection import Connection
from minecraft.networking.packets import clientbound

# Owned
import util
from classes import Client
from view import Terminal
from helper import get_auth_code, authenticate

class BotWrapper:
    """
    Wrapper handling listener registration and updating displayed informations

    Attributes
    ----------
    _terminal : Terminal
        class representing a Terminal which displays informations and output
    _client : Client
        class representing a Client containing basic informations about the player
    _address : str
        Minecraft server to be conencted to
    _port : ushort
        port of the server
    _connection : Connection
        class representing a connection to a Minecraft server
    _bot : Bot
        class representing a Minecraft bot

    Methods
    -------
    _register_listeners(self)
        Registers all packet listeners
    _login_success(self, packet)
        To be executed on 'login success' packet
    _join_game(self, packet)
        To be executed on 'join game' packet
    _player_position_and_lock(self, packet)
        To be executed on 'player position and lock' packet
    _respawn(self, packet)
        To be executed on 'respawn' packet
    _set_experience(self, packet)
        To be executed on 'set experience' packet
    _update_health(self, packet)
        To be executed on 'update health' packet
    """

    def __init__(self, terminal: Terminal, options: object):
        """
        Parameters
        ----------
        terminal : Terminal
            class representing and managing the terminal and it's subwindows
        options : object
            options parsed by the argument parser
        """
        self._terminal = terminal

        auth_code = options.auth_code
        if not options.auth_code:
            self._terminal.console.log("Please head to your browser for authentication.")
            auth_code = get_auth_code(options.client_id, options.redirect_port)
            if options.auth_code == "":
                self._terminal.console.log(f'Auth Code: {auth_code}')
                sleep(10)
                sys.exit(0)

        auth_token = authenticate(options.client_id, options.client_secret, options.redirect_port, auth_code)

        self._client = Client(auth_token.profile.name, auth_token.profile.id_)
        
        self._terminal.info.update(self._client.name, util.format_uuid(self._client.uuid))
        self._terminal.console.log('Successfully authenticated')

        self._address = options.address
        self._port = options.port

        self._connection = Connection(self._address, self._port, auth_token=auth_token)

        if hasattr(options, 'Bot'):
            self._bot = options.Bot(self._terminal, self._connection, self._client)
        else:
            self._bot = None

        self._register_listeners()

        self._connection.connect()

        while (True):
            key = self._terminal.stdscr.getkey()
            if (key == 'q'):
                sys.exit(0)
            
            if (key == 'KEY_UP'):
                self._terminal.console.scroll_up()
            elif (key == 'KEY_DOWN'):
                self._terminal.console.scroll_down()
            else:
                if hasattr(self._bot, 'keys') and key in self._bot.keys and inspect.ismethod(self._bot.keys[key]):
                    self._bot.keys[key]()

    def _register_listeners(self):
        # Login
        self._connection.register_packet_listener(self._login_success, clientbound.login.LoginSuccessPacket)
        # Play
        self._connection.register_packet_listener(self._disconnect, clientbound.play.DisconnectPacket)
        self._connection.register_packet_listener(self._join_game, clientbound.play.JoinGamePacket)
        self._connection.register_packet_listener(self._player_position_and_lock, clientbound.play.PlayerPositionAndLookPacket)
        self._connection.register_packet_listener(self._respawn, clientbound.play.RespawnPacket)
        self._connection.register_packet_listener(self._chat_message, clientbound.play.ChatMessagePacket)
        self._connection.register_packet_listener(self._set_experience, clientbound.play.SetExperiencePacket)
        self._connection.register_packet_listener(self._update_health, clientbound.play.UpdateHealthPacket)

        # Dynamically registered        # TODO detect which ones to register        
        if hasattr(self._bot, 'spawn_object') and inspect.ismethod(self._bot.spawn_object):
            self._connection.register_packet_listener(self._bot.spawn_object, clientbound.play.SpawnObjectPacket)

        if hasattr(self._bot, 'entity_position_delta') and inspect.ismethod(self._bot.entity_position_delta):
            self._connection.register_packet_listener(self._bot.entity_position_delta, clientbound.play.EntityPositionDeltaPacket)

        if hasattr(self._bot, 'destroy_entities') and inspect.ismethod(self._bot.destroy_entities):
            self._connection.register_packet_listener(self._bot.destroy_entities, clientbound.play.DestroyEntitiesPacket)

        if hasattr(self._bot, 'sound_effect') and inspect.ismethod(self._bot.sound_effect):
            self._connection.register_packet_listener(self._bot.sound_effect, clientbound.play.SoundEffectPacket)

        if hasattr(self._bot, 'entity_teleport') and inspect.ismethod(self._bot.entity_teleport):
            self._connection.register_packet_listener(self._bot.entity_teleport, clientbound.play.EntityTeleportPacket)
        
    # Login
    def _login_success(self, packet):
        self._terminal.console.log(f'Successfully logged into {self._address:s}:{self._port:d}')

        if hasattr(self._bot, 'login_success') and inspect.ismethod(self._bot.login_success):
            self._bot.login_success(packet)

    # Play
    def _join_game(self, packet):
        self._client.entity_id = packet.entity_id
        self._client.dimension = packet.dimension_codec['minecraft:dimension_type']['value'][0]['name'].value
        self._terminal.position.update_dimension(self._client.dimension)
        self._terminal.console.log(f'Successfully joined the game ({hex(self._client.entity_id):s})')

        if hasattr(self._bot, 'join_game') and inspect.ismethod(self._bot.join_game):
            self._bot.join_game(packet)

    def _disconnect(self, packet):
        self._terminal.console.log(f'Disconnected: {packet.json_data}')

        if hasattr(self._bot, 'disconnect') and inspect.ismethod(self._bot.disconnect):
            self._bot.disconnect(packet)

    def _player_position_and_lock(self, packet):
        packet.apply(self._client)
        self._terminal.position.update_xyz(self._client.x, self._client.y, self._client.z)
        self._terminal.position.update_facing(self._client.yaw, self._client.pitch)

        if hasattr(self._bot, 'player_position_and_lock') and inspect.ismethod(self._bot.player_position_and_lock):
            self._bot.player_position_and_lock(packet)

    def _respawn(self, packet):
        if (self._client.dimension == packet.dimension_codec['minecraft:dimension_type']['value'][0]['name'].value): # useless ?
            return

        self._client.dimension = packet.dimension_codec['minecraft:dimension_type']['value'][0]['name'].value
        self._terminal.position.udpate_dimenstion(self._client.dimension)

        if hasattr(self._bot, 'respawn') and inspect.ismethod(self._bot.respawn):
            self._bot.respawn(packet)

    def _chat_message(self, packet):
        msg = ''
        data = json.loads(packet.json_data)
        # TODO handle other kind of messages
        for kind in data.values():
            for value in kind:
                if 'text' in value:
                    msg += value['text']

        msg = re.sub(r'\\u[0-9a-fA-F]{4}', '', msg)
        # TODO adjust for multiline messages (i.e. message longer than console width)
        if msg:
            self._terminal.console.log(f'[CHAT] {msg}')

        if hasattr(self._bot, 'chat_message') and inspect.ismethod(self._bot.chat_message):
            self._bot.chat_message(packet)

    def _set_experience(self, packet):
        if (self._client.xp_bar == packet.experience_bar and self._client.lvl == packet.level): # useless ?
            return

        self._client.xp_bar = packet.experience_bar
        self._client.lvl = packet.level
        self._terminal.xp.update(self._client.xp_bar, self._client.lvl)

        if hasattr(self._bot, 'set_experience') and inspect.ismethod(self._bot.set_experience):
            self._bot.set_experience(packet)
    
    def _update_health(self, packet):
        health = int(packet.health)
        if (not self._client.health == health or not self._client.food == packet.food):
            self._client.health = health
            self._client.food = packet.food
            self._terminal.bar.update(self._client.health, self._client.food)

        if hasattr(self._bot, 'update_health') and inspect.ismethod(self._bot.update_health):
            self._bot.update_health(packet)