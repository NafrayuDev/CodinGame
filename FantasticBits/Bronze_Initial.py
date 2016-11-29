import sys
import math


def log(data):
    print(data, file=sys.stderr)


def logger(data):
    print(*data, file=sys.stderr)


# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.

round_counter = 0
my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left


###
# Classes
class Team:
    id = 0
    goal_own = 0
    goal_enemy = 0
    magic = 0

    def __init__(self, paramId):
        self.id = paramId
        if self.id == 1:
            self.goal_enemy = (0, 3750)
            self.goal_own = (16000, 3750)
        else:
            self.goal_enemy = (16000, 3750)
            self.goal_own = (0, 3750)


class Vector:
    x, y = 0, 0

    def __init__(self, paramX, paramY):
        self.x, self.y = paramX, paramY

    def get(self):
        return self.x, self.y

    def get_length(self):
        return math.sqrt((self.x ** 2) + (self.y ** 2))

    def get_normalized(self, paramMagnitude):
        fx = self.x * (paramMagnitude / self.get_length())
        fy = self.y * (paramMagnitude / self.get_length())
        return fx, fy


class Entity:
    e_id = 0
    e_type = 0
    x, y = 0, 0
    vx, vy = 0, 0
    state = 0

    def __init__(self, paramEntityId, paramEntityType, paramX, paramY, paramVX, paramVY, paramState):
        self.e_id = paramEntityId
        self.e_type = paramEntityType
        self.x = paramX
        self.y = paramY
        self.vx = paramVX
        self.vy = paramVY
        self.state = paramState

    def get_coordinates(self):
        return self.x, self.y

    def get_speed_vector(self):
        return self.vx, self.vy

    def get_speed_vector_length(self):
        return math.sqrt((self.vx ** 2) + (self.vy ** 2))


class Wizard(Entity):
    entity = 0

    def __init__(self, paramEntity):
        self.entity = paramEntity

    def get_distance_to(self, paramTarget):
        return int(math.hypot(paramTarget.x - self.entity.x, paramTarget.y - self.entity.y))

    def get_next_snaffle(self):
        snaffle_distances = {}
        for snaffle in snaffles:
            snaffle_distances[self.get_distance_to(Vector(snaffle.x, snaffle.y))] = snaffle
        nearest = min(snaffle_distances.keys())
        return snaffle_distances[nearest]


class Output:
    command = ""
    x, y = 0, 0
    power = 0
    profile = ""

    def __init__(self, paramCommand, paramX, paramY, paramPower):
        self.command = paramCommand
        self.x = paramX
        self.y = paramY
        self.power = paramPower

    def print_action(self):
        print(*(self.command, self.x, self.y, self.power, self.profile))

    @staticmethod
    def spell_obliviate(paramId):
        print(*("OBLIVIATE", paramId))

    @staticmethod
    def spell_petrificus(paramId):
        print(*("PETRIFICUS", paramId))

    @staticmethod
    def spell_accio(paramId):
        print(*("ACCIO", paramId))

    @staticmethod
    def spell_flipendo(paramId):
        print(*("FLIPENDO", paramId))


class ProfileBasic:
    wizard = 0

    def __init__(self, paramWizard):
        self.wizard = paramWizard

    def action(self):
        out = Output("MOVE", 0, 0, 0)
        nxt_snaffle = wizard.get_next_snaffle()
        out.x = nxt_snaffle.x
        out.y = nxt_snaffle.y
        out.power = 150

        if wizard.entity.state == 1:
            out.command = "THROW"
            out.x = myTeam.goal_enemy[0]
            out.y = myTeam.goal_enemy[1]
            out.power = 500

        out.print_action()


class ProfileDefend:
    wizard = 0
    score = 100

    def __init__(self, paramWizard):
        self.wizard = paramWizard

    def action_rating(self):
        for snaffle in snaffles:
            if snaffle.x < 8000:
                self.score += 5
        return self.score

    def action(self):
        snaffle_distances = {}
        for snaffle in snaffles:
            snaffle_distances[snaffle.x] = snaffle
        nearest = min(snaffle_distances.keys())
        out = Output("MOVE", 0, 0, 0)
        nxt_snaffle = snaffle_distances[nearest]
        out.x = nxt_snaffle.x
        out.y = nxt_snaffle.y
        out.power = 150
        out.profile = "-DEFENDER-"

        if wizard.entity.state == 1:
            out.command = "THROW"
            out.x = myTeam.goal_enemy[0]
            out.y = myTeam.goal_enemy[1]
            out.power = 500

        out.print_action()


class ProfileAttack:
    wizard = 0
    score = 100

    def __init__(self, paramWizard):
        self.wizard = paramWizard

    def action_rating(self):
        for snaffle in snaffles:
            if snaffle.x > 8000:
                self.score += 2
        return self.score

    def action(self):
        out = Output("MOVE", 0, 0, 0)
        nxt_snaffle = wizard.get_next_snaffle()
        out.x = nxt_snaffle.x
        out.y = nxt_snaffle.y
        out.power = 150
        out.profile = "-ATTACKER-"

        if wizard.entity.state == 1:
            out.command = "THROW"
            out.x = myTeam.goal_enemy[0]
            out.y = myTeam.goal_enemy[1]
            out.power = 500

        out.print_action()
###
# Global Area
myTeam = Team(my_team_id)

# game loop
while True:
    round_counter += 2
    entities_count = int(input())  # number of entities still in game
    entities = []
    wizards, enemies, snaffles, bludgers = [], [], [], []
    for i in range(entities_count):
        # entity_id: entity identifier
        # entity_type: "WIZARD", "OPPONENT_WIZARD" or "SNAFFLE" (or "BLUDGER" after first league)
        # x: position
        # y: position
        # vx: velocity
        # vy: velocity
        # state: 1 if the wizard is holding a Snaffle, 0 otherwise
        entity_id, entity_type, x, y, vx, vy, state = input().split()
        entities.append(Entity(int(entity_id), entity_type, int(x), int(y), int(vx), int(vy), int(state)))
    for e in entities:
        if e.e_type == "WIZARD":
            wizards.append(Wizard(e))
        elif e.e_type == "OPPONENT_WIZARD":
            enemies.append(Wizard(e))
        elif e.e_type == "SNAFFLE":
            snaffles.append(e)
        elif e.e_type == "BLUDGER":
            bludgers.append(e)

    for wizard in wizards:
        selected_profile = 0
        selected_profile_score = 0
        profiler_list = [ProfileDefend(wizard), ProfileAttack(wizard)]
        for profile in profiler_list:
            if profile.action_rating() > selected_profile_score:
                selected_profile = profile

        selected_profile.action()

        # Profile_Basic(wizard).action()

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)

        # Edit this line to indicate the action for each wizard (0 ≤ thrust ≤ 150, 0 ≤ power ≤ 500)
        # i.e.: "MOVE x y thrust" or "THROW x y power"
        # print("MOVE 8000 3750 100")
