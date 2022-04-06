# -*- coding: utf-8 -*-

# Generic/Built-in
import math
import threading

# ammaraskar/pyCraft
from minecraft.networking.packets import serverbound

class Bobber:
    def __init__(self, id, x, y, z):
        self.id = id
        self.x = x
        self.y = y
        self.z = z

def calc_distance(a, b):
        return math.sqrt(math.pow(b.x - a.x, 2) + math.pow(b.y - a.y, 2) + math.pow(b.z - a.z, 2))

class Bot:
    _auto_reconnect = True
    _range_bobber_detection = 2
    _range_bobber_sound = 8
    _sleep = 1
    _sleep_reconnect = 60

    _anti_anti_fish = True
    _yaw_movement = 23
    _looking_away = False

    _active = False

    def __init__(self, terminal, connection, client):
        self._terminal = terminal
        self._connection = connection
        self._client = client

        self.keys = { 
            'f': self._fish
        }

    # Senders
    def _use_item(self):
        packet = serverbound.play.UseItemPacket()
        packet.hand = 0
        self._connection.write_packet(packet)

    def _look_over(self):
        packet = serverbound.play.PositionAndLookPacket()
        packet.x = self._client.x
        packet.feet_y = self._client.y
        packet.z = self._client.z
        self._client.yaw += (-self._yaw_movement if self._looking_away else self._yaw_movement)
        self._client.yaw = self._client.yaw % 360.0
        packet.yaw = self._client.yaw
        packet.pitch = self._client.pitch
        packet.on_ground = True
        self._connection.write_packet(packet)
        self._terminal.position.update_facing(self._client.yaw, self._client.pitch)
        self._looking_away = not self._looking_away

    # Listeners
    def join_game(self, packet):
        threading.Timer(self._sleep, self._fish).start()
            
    def disconnect(self, packet):
        if self._auto_reconnect:
            self._active = False
            threading.Timer(self._sleep_reconnect, self._connection.connect).start()

    def spawn_object(self, packet):
        if packet.type_id == 112 and not self._active and calc_distance(self._client, packet) < self._range_bobber_detection:
            self._terminal.console.log(f'[FISH] Found fishing bobber ({hex(packet.entity_id):s})')
            self._bobber = Bobber(packet.entity_id, packet.x, packet.y, packet.z)
            self._active = True

    def entity_position_delta(self, packet):
        if self._active and packet.entity_id == self._bobber.id:
            self._bobber.x += packet.delta_x_float
            self._bobber.y += packet.delta_y_float
            self._bobber.z += packet.delta_z_float

    def entity_teleport(self, packet):
        if self._active and packet.entity_id == self._bobber.id:
            self._bobber.x = packet.x
            self._bobber.y = packet.y
            self._bobber.z = packet.z

    def destroy_entities(self, packet):
        if self._active:
            for entity_id in packet.entity_ids:
                if entity_id == self._bobber.id:
                    self._terminal.console.log('[FISH] Bobber got destroyed')
                    self._active = False
                    threading.Timer(self._sleep, self._use_item).start()

    def sound_effect(self, packet):
        if self._active and packet.sound_id == 372 and calc_distance(self._bobber, packet.effect_position) < self._range_bobber_sound:
            self._terminal.console.log('[FISH] Caught something')
            self._active = False
            self._use_item()
            if self._anti_anti_fish:
                self._look_over()
            threading.Timer(self._sleep, self._use_item).start()

    # Custom methods
    def _fish(self):
        if not self._active:
            self._terminal.console.log('[FISH] Started fishing')
            self._use_item()
        else:
            self._terminal.console.log('[FISH] Stopped fishing')
            self._active = False
            self._use_item()



    