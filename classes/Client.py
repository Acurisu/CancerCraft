# -*- coding: utf-8 -*-

from util import format_uuid


class Client:
    """
    Class representing the player

    Attributes
    ----------
    entity_id : int
        entity ID on the server
    health : int
        healh value (0-20)
    food : int
        food value (0-20)
    xp_bar : float
        percentage of the xp bar being full
    lvl : int
        xp level
    dimension : int
        dimension (-1: Nether, 0: Overworld, 1: End)
    x : float
        x coordinate
    y : float
        y coordinate
    z : float
        z coordinate
    yaw : float
        yaw
    pitch : float
        pitch
    name : str
        player username (!= login username)
    uuid : str
        UUID
    """

    entity_id = 0

    health = 0
    food = 0
    # saturation = 0

    xp_bar = 0
    lvl = 0
    # xp_total = 0

    dimension = 0 # -1: Nether, 0: Overworld, 1: End

    x = 0
    y = 0
    z = 0

    yaw = 0
    pitch = 0

    def __init__(self, name: str, uuid: int):
        """
        Parameters
        ----------
        name : str
            player username (!= login username)
        uuid : int
            UUID as number (not formatted)
        """
        self.name = name
        self.uuid = format_uuid(uuid)