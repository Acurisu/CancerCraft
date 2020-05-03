import math
import time
import threading

from minecraft.networking.packets import serverbound

class Client:
    x = 0
    y = 0
    z = 0
    yaw = 0
    pitch = 0

class Bobber:
    def __init__(self, id, x, y, z):
        self.id = id
        self.x = x
        self.y = y
        self.z = z

def calc_distance(a, b):
        return math.sqrt(math.pow(b.x - a.x, 2) + math.pow(b.y - a.y, 2) + math.pow(b.z - a.z, 2))

class Bot:
    _range_bobber_detection = 5
    _range_bobber_sound = 3
    _sleep = 1

    _active = False

    def __init__(self, terminal, connection):
        self._terminal = terminal
        self._connection = connection
        self._client = Client()

        self.keys = { 
            'f': self._fish
        }

    # Senders
    def _use_item(self):
        packet = serverbound.play.UseItemPacket()
        packet.hand = 0
        self._connection.write_packet(packet)

    # Listeners
    def player_position_and_lock(self, packet):
        packet.apply(self._client)

    def spawn_object(self, packet):
        if packet.type_id == 102 and not self._active and calc_distance(self._client, packet) < self._range_bobber_detection:
            self._terminal.log(f'[FISH] Found fishing bobber ({hex(packet.entity_id):s})')
            self._bobber = Bobber(packet.entity_id, packet.x, packet.y, packet.z)
            self._active = True

    def destroy_entities(self, packet):
        if self._active:
            for entity_id in packet.entity_ids:
                if entity_id == self._bobber.id:
                    self._terminal.log(f'[FISH] Bobber got destroyed')
                    self._active = False
                    threading.Timer(self._sleep, self._use_item).start()

    def sound_effect(self, packet):
        if self._active and packet.sound_id == 73 and calc_distance(self._bobber, packet.effect_position) < self._range_bobber_sound:
            self._terminal.log(f'[FISH] Caught something')
            self._active = False
            self._use_item()
            threading.Timer(self._sleep, self._use_item).start()

    # Custom methods
    def _fish(self):
        if not self._active:
            self._terminal.log(f'[FISH] Started fishing')
            self._use_item()
        else:
            self._terminal.log(f'[FISH] Stopped fishing')
            self._active = False
            self._use_item()



    