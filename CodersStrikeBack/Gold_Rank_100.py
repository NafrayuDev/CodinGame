import sys
import math
import datetime

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def log(data):
    print(data, file=sys.stderr)


def logger(data):
    print(*data, file=sys.stderr)


laps = int(input())
checkpoint_count = int(input())
gen_checkpoints = []
checkpoints = []
p_counter = 0
for i in range(checkpoint_count):
    gen_checkpoints.append(int(j) for j in input().split())


def populate_checkpoints():
    try:
        while True:
            for abc in gen_checkpoints:
                checkpoints.append((int(next(abc)), int(next(abc))))
    except StopIteration:
        pass


populate_checkpoints()


########################

#####
# Classes ###
#####
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

    def get_coords(self):
        return (self.x, self.y)

    def get_speed_vector(self):
        return (self.vx, self.vy)

    def get_speed_vector_length(self):
        return get_vector_length((self.vx, self.vy))

    def get_distance_to_checkpoint(self):
        return int(math.hypot(checkpoints[self.nextCheckpointId][0] - self.x, checkpoints[self.nextCheckpointId][1] - self.y))

    def get_vector_to_checkpoint(self):
        return checkpoints[self.nextCheckpointId][0] - self.x, checkpoints[self.nextCheckpointId][1] - self.y

    def get_next_checkpoint_coords(self):
        return checkpoints[self.nextCheckpointId]

    def get_distance_to(self, p):
        return int(math.hypot(p[0] - self.x, p[1] - self.y))

    def get_cp_distance_progress(self):
        cpDistance = int(math.hypot(checkpoints[self.nextCheckpointId][0] - checkpoints[self.nextCheckpointId-1][0], checkpoints[self.nextCheckpointId][1] - checkpoints[self.nextCheckpointId-1][1]))
        return (100 - int((self.get_distance_to_checkpoint() / cpDistance) * 100))

    def get_angle_to_checkpoint(self):
        return calc_angle(self.get_speed_vector(), (
            checkpoints[self.nextCheckpointId][0] - self.x, checkpoints[self.nextCheckpointId][1] - self.y))

    def get_angle_to_point(self, paramPoint):
        return calc_angle(self.get_speed_vector(), (paramPoint[0] - self.x, paramPoint[1] - self.y))

    def get_facing_vector(self):
        cx = math.cos(math.radians(self.angle)) * 100
        cy = math.sin(math.radians(self.angle)) * 100
        return (int(cx), int(cy))

    def get_fangle_to_checkpoint(self):
        return calc_angle(self.get_facing_vector(), (
            checkpoints[self.nextCheckpointId][0] - self.x, checkpoints[self.nextCheckpointId][1] - self.y))

    def get_fangle_to_point(self, paramPoint):
        return calc_angle(self.get_facing_vector(), (paramPoint[0] - self.x, paramPoint[1] - self.y))

class Vector:
    x, y = 0, 0

    def get(self):
        return (self.x, self.y)

    def get(self):
        return (self.x, self.y)

    def get_normalized(self, paramMagnitude):
        fx = self.x * (paramMagnitude/vlen)
        fy = data[1] * (paramMagnitude/vlen)
        return (fx, fy)
#####
# Functions ###
#####

def normalize_vector(data, paramMagnitude):
    vlen = get_vector_length(data)
    fx = data[0] * (paramMagnitude/vlen)
    fy = data[1] * (paramMagnitude/vlen)
    return (fx, fy)

def calc_angle2(v1, v2):
    nen = vector_dot_product(v1, v2)
    zae = get_vector_length(v1) + get_vector_length(v2)
    return math.acos((nen / zae))


def calc_angle(v1, v2):
    from math import atan2, degrees, pi
    rads = atan2(v2[1], v2[0]) - atan2(v1[1], v1[0])
    rads %= 2 * pi
    return degrees(rads)


def action_rating(paramPod, paramX, paramY):
    mod = [1, 1, 1]
    angle_perC = (1 - (180 - abs(paramPod.get_fangle_to_point((paramX, paramY)) - 180)) / 180) * 100
    res = angle_perC
    distance = paramPod.get_distance_to_checkpoint()
    if angle_perC < 50: mod[0] = 0.75
    if angle_perC < 35: mod[0] = 0.5
    if angle_perC < 15: mod[0] = 0.2
    if distance < 1000: mod[1] = 0.75
    if distance < 750: mod[1] = 0.5
    for m in mod:
        res *= m
    return int(res)


#####

def get_checkpoint(data):
    return checkpoints[data % checkpoint_count]


def get_distance(p_1, p_2):
    return int(math.hypot(p_2[0] - p_1[0], p_2[1] - p_1[1]))


def get_vector_length(data):
    tmp = 0
    for d in data:
        tmp += d ** 2
    return math.sqrt(tmp)


def vector_dot_product(v1, v2):
    res = []
    for tmp_cnt in range(len(v1)):
        tmp = v2[tmp_cnt] * v1[tmp_cnt]
        res.append(tmp)
    return sum(res)


def add_vector(v1, v2):
    return tuple(map(sum, zip(v1, v2)))


def vect_a_to_b(paramA, paramB):
    res = []
    for tmp_cnt in range(len(paramA)):
        tmp = paramB[tmp_cnt] - paramA[tmp_cnt]
        res.append(tmp)
    return tuple(res)


def collision_detecter(paramPod, paramSpeedVectorMultiplier, paramCollisionRange):
    res = False
    nextRoundRacerPosition = (paramPod.x + paramPod.vx * paramSpeedVectorMultiplier, paramPod.y + paramPod.vy * paramSpeedVectorMultiplier)
    nextRoundEnemyPosition = []
    for e in enemy:
        nextRoundEnemyPosition.append((e.x + e.vx * paramSpeedVectorMultiplier, e.y + e.vy * paramSpeedVectorMultiplier))
    for ep in nextRoundEnemyPosition:
        if get_distance(ep, nextRoundRacerPosition) < paramCollisionRange:
            res = True
            log("Prepare for impact!")
    return res


def get_perpendicular_vector(paramV):
    return (paramV[1] * (-1), paramV[0])


def calculate_checkpoint_edges():
    res = []
    prev_cpt = checkpoints[0]
    for tmp_cnt in range(1, len(checkpoints) + 1):
        v_con = vect_a_to_b(prev_cpt, get_checkpoint(tmp_cnt))
        v_con_len = get_vector_length(v_con)
        multiplier = 300 / v_con_len
        pt_tmp = []
        for c in v_con:
            pt_tmp.append(int(multiplier * c))
        res.append(add_vector(prev_cpt, pt_tmp))
        prev_cpt = get_checkpoint(tmp_cnt)
    return res


def curve2(data):
    return (-(math.log1p(x/100) *x*x*x*x))/200000


def curve(data):
    return (-0.7 * (data)) + 20
    #return -((0.05)*(data-50)*(data-50)) + 20


def get_angle_perC(paramAngle):
    return  (1 - (180 - abs(paramAngle - 180)) / 180) * 100


# paramsMV = [cnt:2] deltaCoods Multiplier (int 0-5, float 0.0-1.0)
# paramsSHIELD = [cnt:2] CollisionDetecter Parameters (SpeedVectorMultiplier 0-5, CollisionRange 800 - 1500)
#   CheckpointDistance (0-4000) SpeedVectorLength (0-500)
# paramsBOOST = [cnt:4] CollisionDetecter Parameters (SpeedVectorMultiplier 0-5, CollisionRange 800 - 2500)
#   CheckpointDistance (0-4000) CheckpointFaceAnglePerCent (0-100)
# paramsOFFSET = [cnt:3] Checkpoint Offset, checkpoint+1 before reaching checkpoint
# Distance to Checkpoint (0-1500), MVAngle to Checkpoint 0-100, SpeedVectorLength 50-350
def profiler_racing(paramPod, paramsMV, paramsSHIELD, paramsBOOST, paramsOFFSET):
    (p1_x, p1_y) = get_checkpoint((paramPod.nextCheckpointId))
    dx = p1_x - paramPod.x - paramPod.vx * paramsMV[0]
    dy = p1_y - paramPod.y - paramPod.vy * paramsMV[0]
    p1_x = (paramPod.x + (dx * paramsMV[1]))
    p1_y = (paramPod.y + (dy * paramsMV[1]))
    p1_thrust = action_rating(paramPod, p1_x, p1_y)
    if (collision_detecter(paramPod, paramsSHIELD[0], paramsSHIELD[1]) and paramPod.get_distance_to_checkpoint() < paramsSHIELD[2] and get_vector_length(
            paramPod.get_speed_vector()) > paramsSHIELD[3]):
        p1_thrust = "SHIELD"
    if (not collision_detecter(paramPod, paramsBOOST[0], paramsBOOST[1]) and paramPod.get_distance_to_checkpoint() > paramsBOOST[2] and (
                1 - (180 - abs(paramPod.get_fangle_to_checkpoint() - 180)) / 180) * 100 > paramsBOOST[3]):
        p1_thrust = "BOOST"
    if (paramPod.get_distance_to_checkpoint() < paramsOFFSET[0] and get_angle_perC(paramPod.get_angle_to_checkpoint()) > paramsOFFSET[1] and paramPod.get_speed_vector_length() > paramsOFFSET[2]):
        (p1_x, p1_y) = get_checkpoint(paramPod.nextCheckpointId + 1)
        p1_thrust = action_rating(paramPod, p1_x, p1_y)
    return (p1_x, p1_y, p1_thrust, "--RACER--")

def speed_rating(paramPod, paramX, paramY):
    mod = [1, 1, 1]
    angle_perC = get_angle_perC(paramPod.get_angle_to_point((paramX, paramY)))
    distanceProgress = paramPod.get_cp_distance_progress()
    distance = paramPod.get_distance_to_checkpoint()
    res = 100
    if angle_perC < 80: mod[0] = 0.8
    if angle_perC < 50: mod[0] = 0.5
    if angle_perC < 20: mod[0] = 0.2
    if distance < 1000: mod[1] = 0.75
    if distance < 750: mod[1] = 0.5
    if distanceProgress > 75: mod[2] = 0.75
    if distanceProgress > 85: mod[2] = 0.5
    for m in mod:
        res *= m
    return int(res)

def profiler_hunting(paramPod):
    #(fx, fy) = paramPod.get_next_checkpoint_coords()
    (fx, fy) = paramPod.get_vector_to_checkpoint()
    f_coords = (fx, fy)
    (fx, fy) = normalize_vector((fx, fy), 500)
    ppd_vect = get_perpendicular_vector((fx, fy))
    n_ppd_vect_x = (ppd_vect[0] * -1)
    n_ppd_vect_y = (ppd_vect[1] * -1)
    ppdDistance = int(math.hypot(get_checkpoint(paramPod.nextCheckpointId +1)[0] - (fx + ppd_vect[0]),
      get_checkpoint(paramPod.nextCheckpointId +1)[1] - (fy + ppd_vect[1])))
    nppdDistance = int(math.hypot(get_checkpoint(paramPod.nextCheckpointId +1)[0] - (fx + n_ppd_vect_x),
      get_checkpoint(paramPod.nextCheckpointId +1)[1] - (fy + n_ppd_vect_y)))
    if ppdDistance > nppdDistance:
        ppd_vect = (n_ppd_vect_x, n_ppd_vect_y)
    fx += paramPod.x
    fy += paramPod.y
    f_thrust = 100

    cpDistance = int(math.hypot(checkpoints[paramPod.nextCheckpointId][0] - checkpoints[paramPod.nextCheckpointId-1][0], checkpoints[paramPod.nextCheckpointId][1] - checkpoints[paramPod.nextCheckpointId-1][1]))
    distanceProgress = 100 - int((paramPod.get_distance_to_checkpoint() / cpDistance) * 100)
    mod = 0
    if distanceProgress < 0:
        mod = curve(0)
    if distanceProgress > 40:
        mod = curve(83)
    else:
        mod = curve(distanceProgress)
    if mod < 1:
        mod = 0
    fx += (ppd_vect[0] * (mod/100))
    fy += (ppd_vect[1] * (mod/100))
    f_thrust = speed_rating(paramPod, fx, fy)
    logger((int(fx), int(fy), f_thrust, "--HUNTER--", int(distanceProgress), mod))
    return (int(fx), int(fy), f_thrust, "--HUNTER--")


def tmpNIU(paramPod):
    res = [0, 0, 100, "--HUNTER--"]
    vect_PC = list(paramPod.get_vector_to_checkpoint())
    vect_PC[0] = int(vect_PC[0] * 1)
    vect_PC[1] = int(vect_PC[1] * 1)
    ppd_vect = get_perpendicular_vector(vect_PC)
    ppd_vect_len = get_vector_length(ppd_vect)
    for c in ppd_vect:
        c *= 10/ppd_vect_len
    res[0] = paramPod.get_next_checkpoint_coords()[0] + ppd_vect[0]
    res[1] = paramPod.get_next_checkpoint_coords()[1] + ppd_vect[1]
    logger(res)
    tmp = normalize_vector((res[0], res[1]), 500)
    res[0] = paramPod.get_next_checkpoint_coords()[0] + tmp[0]
    res[1] = paramPod.get_next_checkpoint_coords()[1] + tmp[1]
    logger(res)
    return tuple(res)


def profiler_defending(paramPod):
    victim_id = 0
    tmp_val = 0

    tarId = 0
    tarVal = 999999
    for e_cnt in range(0, len(enemy)):
        if (paramPod.get_distance_to(enemy[e_cnt].get_coords()) < tarVal):
            tarId = e_cnt
            tarVal = paramPod.get_distance_to(enemy[e_cnt].get_coords())
    for e_cnt in range(0, len(enemy)):
        if e_tracer[e_cnt][1] == tmp_val:
            victim_id = tarId
        if e_tracer[e_cnt][1] > tmp_val:
            victim_id = e_cnt
            tmp_val = e_tracer[e_cnt][1]
    victim = enemy[victim_id]
    fob = vect_a_to_b(victim.get_coords(), get_checkpoint(defenderStation[0]))
    def_x = victim.x + (fob[0] * 0.8)
    def_y = victim.y + (fob[1] * 0.8)
    if (defenderStation[0] >= victim.nextCheckpointId) and victim.nextCheckpointId != 0:
        def_thrust = action_rating(paramPod, def_x, def_y)
        distance_modificator = 1
        if paramPod.get_distance_to((def_x, def_y)) < 4500:
            distance_modificator = 0.75
        if paramPod.get_distance_to((def_x, def_y)) < 3000:
            distance_modificator = 0.5
        def_thrust = int(def_thrust * distance_modificator)
        if (paramPod.get_distance_to((def_x, def_y)) < 2000):
            def_x = victim.x + (3 * victim.vx)
            def_y = victim.y + (3 * victim.vy)
            def_thrust = 0
            v_ang_perC = (1 - (180 - abs(victim.get_fangle_to_checkpoint() - 180)) / 180) * 100
            p_ang_perC = (1 - (180 - abs(paramPod.get_fangle_to_point((def_x, def_y)) - 180)) / 180) * 100
            if (victim.get_distance_to(get_checkpoint(defenderStation[0])) < 4500) and p_ang_perC > 70 and v_ang_perC > 80:
                ang = (1 - (180 - abs(paramPod.get_fangle_to_point((victim.x + (2 * victim.vx), victim.y + (2 * victim.vy))) - 180)) / 180) * 100
                mvAng = (1 - (180 - abs(paramPod.get_angle_to_point((victim.x + (4 * victim.vx), victim.y + (4 * victim.vy))) - 180)) / 180) * 100
                def_thrust = 60
                if (ang > 70):
                    def_thrust = int(ang)
                if (mvAng > 95):
                    def_thrust = "BOOST"
            if (collision_detecter(paramPod, 2, 1250)):
                def_thrust = "SHIELD"
    else:
        defenderStation[0] = (victim.nextCheckpointId + 1) % (checkpoint_count)
        log("victim nxt cp id")
        log(victim.nextCheckpointId)
        log((victim.nextCheckpointId + 1) % (checkpoint_count))
        log("-end--")
        def_thrust = action_rating(paramPod, def_x, def_y)

    return (int(def_x), int(def_y), def_thrust, "--DEFENDER--")


def enemy_tracker(paramEnemy):
    for e_cnt in range(0, len(paramEnemy)):
        if paramEnemy[e_cnt].nextCheckpointId != e_tracer[e_cnt][0]:
            if min(p_tracer, key=lambda t: t[1]) < max(e_tracer, key=lambda t: t[1]):
                global p_counter
                p_counter += 1
            e_tracer[e_cnt] = (paramEnemy[e_cnt].nextCheckpointId, e_tracer[e_cnt][1] + 1)


def pod_tracker(paramRacer):
    for p_cnt in range(0, len(paramRacer)):
        if paramRacer[p_cnt].nextCheckpointId != p_tracer[p_cnt][0]:
            p_tracer[p_cnt] = (paramRacer[p_cnt].nextCheckpointId, p_tracer[p_cnt][1] + 1)


#########################
# After AREA

checkpoints = calculate_checkpoint_edges()
#####
# Global Variables ###
#####

g_cnt = 0
t_en = 1
# (CurrentTargetCheckpoint, Checkpoints Collected)
e_tracer = [(1, 1), (1, 1)]

p_tracer = [(1, 1), (1, 1)]

defenderStation = [2]
#####
# Game loop ###
#####
while True:
    now = datetime.datetime.time(datetime.datetime.now())
    log(now)
    g_cnt += 2
    # Input Area
    racer = []
    for i in range(2):
        # x: x position of your pod
        # y: y position of your pod
        # vx: x speed of your pod
        # vy: y speed of your pod
        # angle: angle of your pod
        # next_check_point_id: next check point id of your pod
        x, y, vx, vy, angle, next_check_point_id = [int(j) for j in input().split()]
        tmp = Pod(x, y, vx, vy, angle, next_check_point_id)
        racer.append(tmp)
    enemy = []
    for i in range(2):
        # x_2: x position of the opponent's pod
        # y_2: y position of the opponent's pod
        # vx_2: x speed of the opponent's pod
        # vy_2: y speed of the opponent's pod
        # angle_2: angle of the opponent's pod
        # next_check_point_id_2: next check point id of the opponent's pod
        x_2, y_2, vx_2, vy_2, angle_2, next_check_point_id_2 = [int(j) for j in input().split()]
        tmp = Pod(x_2, y_2, vx_2, vy_2, angle_2, next_check_point_id_2)
        enemy.append(tmp)
    # Computation Area
    enemy_tracker(enemy)
    pod_tracker(racer)
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    racerParamsMV = (3, 0.8)
    racerParamsSHIELD = (3, 1100, 1250, 250)
    racerParamsBOOST = (5, 1000, 2750, 95)
    racerParamsOFFSET = (650, 75, 200)
    # Assign Racing Profile
    racerPod = profiler_racing(racer[0], racerParamsMV, racerParamsSHIELD, racerParamsBOOST, racerParamsOFFSET)
    defenderPod = profiler_racing(racer[1], racerParamsMV, racerParamsSHIELD, racerParamsBOOST, racerParamsOFFSET)
    if p_counter > 5:
        if p_tracer[0][1] < p_tracer[1][1]:
            racerPod = profiler_defending(racer[0])
        else:
            defenderPod = profiler_defending(racer[1])
    # You have to output the target position
    #racerPod = profiler_hunting(racer[0])
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
    ### POD 1
    out1_x = str(int(racerPod[0]))
    out1_y = str(int(racerPod[1]))
    out1_thrust = str(racerPod[2])
    out1 = (out1_x, out1_y, out1_thrust, racerPod[3])
    ### POD 2
    out2_x = str(int(defenderPod[0]))
    out2_y = str(int(defenderPod[1]))
    out2_thrust = str(defenderPod[2])
    out2 = (out2_x, out2_y, out2_thrust, defenderPod[3])
    out = (out1, out2)
    # Ouput Area
    for o in out:
        print(*o)
