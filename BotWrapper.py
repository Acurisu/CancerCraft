# -*- coding: utf-8 -*-

# Generic/Built-in
import sys
import importlib
import inspect

# ammaraskar/pyCraft
from minecraft import authentication
from minecraft.exceptions import YggdrasilError
from minecraft.networking.connection import Connection
from minecraft.networking.packets import Packet, clientbound, serverbound

# Owned
import util
from classes.Client import Client

class BotWrapper:
    def __init__(self, terminal, options):
        self._terminal = terminal

        auth_token = authentication.AuthenticationToken()
        if options.auth_type == 'Mojang':
            try:
                auth_token.authenticate(options.username, options.password)
            except YggdrasilError as e:
                print(e)
                sys.exit() # TODO Use correct status and not default to 0 as it's a failure

        self._client = Client(auth_token.profile.name, auth_token.profile.id_)
        
        self._terminal.update_info(self._client.name, util.format_uuid(self._client.uuid))
        self._terminal.log('Successfully authenticated')

        self._address = options.address
        self._port = options.port

        self._connection = Connection(self._address, self._port, auth_token=auth_token)

        if hasattr(options, 'Bot'):
            self._bot = options.Bot(self._terminal, self._connection)
        else:
            self._bot = None

        self._register_listeners()

        self._connection.connect()

        while (True):
            key = self._terminal.stdscr.getkey()
            if (key == 'q'):
                sys.exit(0)
            
            if (key == 'KEY_UP'):
                self._terminal.scroll_up()
            elif (key == 'KEY_DOWN'):
                self._terminal.scroll_down()
            else:
                if hasattr(self._bot, 'keys') and key in self._bot.keys and inspect.ismethod(self._bot.keys[key]):
                    self._bot.keys[key]()

    def _register_listeners(self):
        # Login
        self._connection.register_packet_listener(self._login_success, clientbound.login.LoginSuccessPacket)
        # Play
        self._connection.register_packet_listener(self._join_game, clientbound.play.JoinGamePacket)
        self._connection.register_packet_listener(self._player_position_and_lock, clientbound.play.PlayerPositionAndLookPacket)
        self._connection.register_packet_listener(self._respawn, clientbound.play.RespawnPacket)
        self._connection.register_packet_listener(self._set_experience, clientbound.play.SetExperiencePacket)
        self._connection.register_packet_listener(self._update_health, clientbound.play.UpdateHealthPacket)

        # Dynamically registered        # TODO detect which ones to register        
        if hasattr(self._bot, 'spawn_object') and inspect.ismethod(self._bot.spawn_object):
            self._connection.register_packet_listener(self._bot.spawn_object, clientbound.play.SpawnObjectPacket)

        if hasattr(self._bot, 'destroy_entities') and inspect.ismethod(self._bot.destroy_entities):
            self._connection.register_packet_listener(self._bot.destroy_entities, clientbound.play.DestroyEntitiesPacket)

        if hasattr(self._bot, 'sound_effect') and inspect.ismethod(self._bot.sound_effect):
            self._connection.register_packet_listener(self._bot.sound_effect, clientbound.play.SoundEffectPacket)
        
    # Login
    def _login_success(self, packet):
        self._terminal.log(f'Successfully logged into {self._address:s}:{self._port:d}')

        if hasattr(self._bot, 'login_success') and inspect.ismethod(self._bot.login_success):
            self._bot.login_success(packet)

    # Play
    def _join_game(self, packet):
        self._client.entity_id = packet.entity_id
        self._client.dimension = packet.dimension
        self._terminal.update_dimension(self._client.dimension)
        self._terminal.log(f'Successfully joined the game ({hex(self._client.entity_id):s})')

        if hasattr(self._bot, 'join_game') and inspect.ismethod(self._bot.join_game):
            self._bot.join_game(packet)

    def _player_position_and_lock(self, packet):
        packet.apply(self._client)
        self._terminal.update_xyz(self._client.x, self._client.y, self._client.z)
        self._terminal.update_facing(self._client.yaw, self._client.pitch)

        if hasattr(self._bot, 'player_position_and_lock') and inspect.ismethod(self._bot.player_position_and_lock):
            self._bot.player_position_and_lock(packet)

    def _respawn(self, packet):
        if (self.dimension == packet.dimension): # useless ?
            return

        self._client.dimension = packet.dimension

        if hasattr(self._bot, 'respawn') and inspect.ismethod(self._bot.respawn):
            self._bot.respawn(packet)

    def _set_experience(self, packet):
        if (self._client.xp_bar == packet.experience_bar and self._client.lvl == packet.lvl): # useless ?
            return

        self._client.xp_bar = packet.experience_bar
        self._client.lvl = packet.level
        self._terminal.update_xp(self._client.xp_bar, self._client.lvl)

        if hasattr(self._bot, 'set_experience') and inspect.ismethod(self._bot.set_experience):
            self._bot.set_experience(packet)
    
    def _update_health(self, packet):
        health = int(packet.health)
        if (not self._client.health == health or not self._client.food == packet.food):
            self._client.health = health
            self._client.food = packet.food
            self._terminal.update_bar(self._client.health, self._client.food)

        if hasattr(self._bot, 'update_health') and inspect.ismethod(self._bot.update_health):
            self._bot.update_health(packet)
