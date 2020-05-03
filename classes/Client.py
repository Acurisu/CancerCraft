class Client:
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

    def __init__(self, name, uuid):
        self.name = name
        self.uuid = uuid