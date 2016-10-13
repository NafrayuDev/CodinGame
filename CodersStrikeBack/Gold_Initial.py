import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

laps = int(input())
checkpoint_count = int(input())
gen_checkpoints = []
checkpoints = []
p_counter = 0
for i in range(checkpoint_count):
    gen_checkpoints.append(int(j) for j in input().split())


########################
# Init Functions

def log(data):
    print(data, file=sys.stderr)


def logger(data):
    print(*data, file=sys.stderr)


#####
# Classes ###
#####

class Point:
    x, y = 0, 0

    def __init__(self, paramX, paramY):
        self.x = paramX
        self.y = paramY


class Pod:
    x, y = 0, 0
    vx, vy = 0, 0
    angle = 0
    nextCheckpointId = 0

    def __init__(self, paramX, paramY, paramVX, paramVY, paramAngle, paramNextCheckpointId):
        self.x = paramX
        self.y = paramY
        self.vx = paramVX
        self.vy = paramVY
        self.angle = paramAngle
        self.nextCheckpointId = paramNextCheckpointId

    def get_location(self):
        return Point(self.x, self.y)

    def get_speed_vector(self):
        return Vector(self.vx, self.vy)

    def get_distance_to(self, p):
        return int(math.hypot(p.x - self.x, p.y - self.y))

    def get_vector_to(self, p):
        return Vector(p.x - self.x, p.y - self.y)

    def get_facing_vector(self):
        cx = math.cos(math.radians(self.angle)) * 100
        cy = math.sin(math.radians(self.angle)) * 100
        return Vector(int(cx), int(cy))

    def get_angle_to_point(self, p):
        return calc_angle(self.get_speed_vector(), Vector(p.x - self.x, p.y - self.y))

    def get_facing_angle_to_point(self, p):
        return calc_angle(self.get_facing_vector(), Vector(p.x - self.x, p.y - self.y))

    def get_future(self, paramTarget, paramThrust):
        # Rotation
        future_angle = 0
        calc_angle = -18
        current_angle = self.get_facing_angle_to_point(paramTarget)
        if current_angle > 180:
            calc_angle = 18
        theta = math.radians(angle)
        cs = math.cos(theta)
        sn = math.sin(theta)
        px = x * cs - y * sn
        py = x * sn + y * cs
        # Acceleration
        future_speed_vect = self.get_facing_vector().get_in_magnitude(paramThrust/100).add_vect(self.get_speed_vector())
        # Movement
        future_location = Point(self.x + future_speed_vect.x, self.y + future_speed_vect.y)
        # Friction
        future_speed_vect = future_speed_vect.get_in_magnitude(0.85)
        # Post Calculus
        future_checkpoint = 0
        return Pod(future_location.x, future_location.y, future_speed_vect.x, future_speed_vect.y, future_angle, future_checkpoint)


class Vector:
    x, y = 0, 0

    def __init__(self, paramX, paramY):
        self.x = paramX
        self.y = paramY

    def get(self):
        return self

    def add_vect(self, v):
        rx = self.x + v.x
        ry = self.y + v.y
        return Vector(rx, ry)

    def get_length(self):
        return math.sqrt((self.x ** 2) + (self.y ** 2))

    def get_normalized(self, paramMagnitude):
        fx = self.x * (paramMagnitude/self.get_length())
        fy = self.y * (paramMagnitude/self.get_length())
        return Vector(fx, fy)

    def get_in_magnitude(self, paramMagnitude):
        fx = self.x * paramMagnitude
        fy = self.y * paramMagnitude
        return Vector(fx, fy)

    def get_perpendicular(self):
        return Vector(self.y * (-1), self.x)

    def apply_to(self, p):
        return Vector(p.x + self.x, p.y + self.y)


class Output:
    target = Point(0, 0)
    thrust = ""
    comment = ""

    def __init__(self, target, thrust, comment):
        self.target = target
        self.thrust = thrust
        self.comment = comment

########################
# Global Functions


def calc_angle(v1, v2):
    from math import atan2, degrees, pi
    rads = atan2(v2.y, v2.x) - atan2(v1.y, v1.x)
    rads %= 2 * pi
    return degrees(rads)


def populate_checkpoints():
    try:
        while True:
            for abc in gen_checkpoints:
                checkpoints.append(Point(int(next(abc)), int(next(abc))))
    except StopIteration:
        pass


populate_checkpoints()

########################
# game loop
while True:
    racer = []
    for i in range(2):
        # x: x position of your pod
        # y: y position of your pod
        # vx: x speed of your pod
        # vy: y speed of your pod
        # angle: angle of your pod
        # next_check_point_id: next check point id of your pod
        x, y, vx, vy, angle, next_check_point_id = [int(j) for j in input().split()]
        racer.append(Pod(x, y, vx, vy, angle, next_check_point_id))

    enemy = []
    for i in range(2):
        # x_2: x position of the opponent's pod
        # y_2: y position of the opponent's pod
        # vx_2: x speed of the opponent's pod
        # vy_2: y speed of the opponent's pod
        # angle_2: angle of the opponent's pod
        # next_check_point_id_2: next check point id of the opponent's pod
        x_2, y_2, vx_2, vy_2, angle_2, next_check_point_id_2 = [int(j) for j in input().split()]
        enemy.append(Pod(x_2, y_2, vx_2, vy_2, angle_2, next_check_point_id_2))
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    p0_f1 = racer[0].get_future(checkpoints[racer[0].nextCheckpointId], 100)
    logger((racer[0].get_location().x, racer[0].get_location().y))
    logger((p0_f1.x, p0_f1.y))

    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
    ### POD 0
    output_0 = Output(checkpoints[racer[0].nextCheckpointId], "100", "--POD_0--")
    out_0 = (output_0.target.x, output_0.target.y, output_0.thrust, output_0.comment)
    ### POD 1
    output_1 = Output(checkpoints[racer[1].nextCheckpointId], "100", "--POD_1--")
    out_1 = (output_1.target.x, output_1.target.y, output_1.thrust, output_1.comment)
    out = (out_0, out_1)
    # Ouput Area
    for o in out:
        print(*o)
