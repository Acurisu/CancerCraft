# CancerCraft

CancerCraft is a wrapper based on [pyCraft](https://github.com/ammaraskar/pyCraft) that should make coding [Minecraft](https://www.minecraft.net) [bots](https://en.wikipedia.org/wiki/Software_agent) with [Python](https://www.python.org) easier and more organised.

## Installation

You have to have at least Python 3.5 and Pip installed.

Python module requirements (install using `pip`):

```bash
cryptography>=1.5
requests
future
```

#### Note
As this uses default [Python curses](https://docs.python.org/3/howto/curses.html), it is not (yet) compatible with Windows. Either remove all curses related code or use the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

### Set-Up
As this is based on pyCraft you need to clone (or download) it. Only the `minecraft` folder is required. Since pyCraft does not have all packets implemented, you have to add additional ones yourself. Helpful resources are [Current Protocol Specification](https://wiki.vg/Protocol) and [MC Dev Data](https://joodicator.github.io/mc-dev-data/). It would be nice to contribute created packet implementations to [pyCraft](https://github.com/ammaraskar/pyCraft).

This wrapper requires one additional packet:
```python
class SetExperiencePacket(Packet):
    @staticmethod
    def get_id(context):
        return 0x48 if context.protocol_version >= 550 else \
               0x47 if context.protocol_version >= 471 else \
               0x43 if context.protocol_version >= 461 else \
               0x44 if context.protocol_version >= 451 else \
               0x43 if context.protocol_version >= 389 else \
               0x42 if context.protocol_version >= 352 else \
               0x41 if context.protocol_version >= 345 else \
               0x40 if context.protocol_version >= 336 else \
               0x3F if context.protocol_version >= 318 else \
               0x3D if context.protocol_version >= 70 else \
               0x1f

    packet_name = 'set experience'
    get_definition = staticmethod(lambda context: [
        {'experience_bar': Float},
        {'level': VarInt},
        {'total_experience': VarInt}
    ])
```
Add it to [`minecraft/networking/packets/clientbound/play/__init__.py`](https://github.com/ammaraskar/pyCraft/blob/master/minecraft/networking/packets/clientbound/play/__init__.py). Don't forget to extend `packets` at the top of the file.
```python
def get_packets(context):
    packets = {
        ...,
        SetExperiencePacket
    }
```

## Usage

Execute `python3 main.py -h` for help or just run `python3 main.py` for it to guide you through the process. Keep in mind that the auth type arguments ([Mojang](https://www.mojang.com) / [MCLeaks](https://mcleaks.net)) are positional. Thus they and their related arguments have to be at the end.

I would advise against providing your password directly as an argument as it will be logged in your [shell](https://en.wikipedia.org/wiki/Command-line_interface)'s [command history](https://en.wikipedia.org/wiki/Command_history).

Press `q` to quit and use the arrow keys (up and down) or the scroll wheel to [scroll](https://en.wikipedia.org/wiki/Scrolling) the output [pad](https://docs.python.org/3/howto/curses.html#windows-and-pads) up and down.

## Screenshot(s)
![](./img/screenshot_0.png)

## Bot
To create a bot, simply make a new python file and create a [class](https://docs.python.org/3/tutorial/classes.html#class-objects) called `Bot`.

Keybinds can be set by creating a [class / instance variable](https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables) called `keys` which is a [dict](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) that maps a key returned by [getkey](https://docs.python.org/3/library/curses.html#curses.window.getkey) to a function.

To listen to a certain packet, add the corresponding method to your class.
Currently available methods:
```python
login_success
join_game
player_position_and_lock
respawn
set_experience
update_health
spawn_object
destroy_entities
sound_effect
```

#### Example
```python
class Bot:
    def __init__(self):
        ...

    def login_success(self, packet):
        ...
```
### Problems
Currently, only predefined methods that are linked to packets can be used in the `Bot` definition. Feel free to open an issue or make a pull request if you need one that is missing.

### Ready-to-use Bot(s)
#### [Fisher](./bots/Fisher.py)
The fisher requires two additional packets:
```python
class EntityPositionPacket(Packet): # was named EntityRelativeMove in the past
    @staticmethod
    def get_id(context):
        return 0x29 if context.protocol_version >= 550 else \
               0x28 if context.protocol_version >= 389 else \
               0x27 if context.protocol_version >= 345 else \
               0x26 if context.protocol_version >= 318 else \
               0x25 if context.protocol_version >= 94 else \
               0x26 if context.protocol_version >= 70 else \
               0x15

    packet_name = 'entity position'

    fields = 'entity_id', 'delta_x', 'delta_y', 'delta_z', 'on_ground'

    def read(self, file_object):
        self.entity_id = VarInt.read(file_object)
        self.delta_x = Short.read(file_object) / (32 * 128)
        self.delta_y = Short.read(file_object) / (32 * 128)
        self.delta_z = Short.read(file_object) / (32 * 128)

        # TODO context.protocol_version < 106 ->
        # self.delta_x = Byte.read(file_object)
        # self.delta_y = Byte.read(file_object)
        # self.delta_z = Byte.read(file_object)

        self.on_ground = Boolean.read(file_object)

class DestroyEntitiesPacket(Packet):
    @staticmethod
    def get_id(context):
        return 0x38 if context.protocol_version >= 550 else \
               0x37 if context.protocol_version >= 471 else \
               0x35 if context.protocol_version >= 461 else \
               0x36 if context.protocol_version >= 451 else \
               0x35 if context.protocol_version >= 389 else \
               0x34 if context.protocol_version >= 352 else \
               0x33 if context.protocol_version >= 345 else \
               0x32 if context.protocol_version >= 336 else \
               0x31 if context.protocol_version >= 332 else \
               0x32 if context.protocol_version >= 318 else \
               0x30 if context.protocol_version >= 70 else \
               0x13

    packet_name = 'destroy entities'

    fields = 'count', 'entity_ids'
    
    def read(self, file_object):
        self.count = VarInt.read(file_object)
        self.entity_ids = []
        for i in range(self.count):
            self.entity_ids.append(VarInt.read(file_object))
```
They can be added with the same procedure as mentioned above.

To start/stop [fishing](https://minecraft.gamepedia.com/Fishing) press `f`.

## Thanks
- Huge thanks to [Ammar Askar](https://github.com/ammaraskar) for [pyCraft](https://github.com/ammaraskar/pyCraft)