from math import *
import random
from draw import painter

landmarks = [[20.0, 20.0],
             [80.0, 80.0],
             [20.0, 80.0],
             [80.0, 20.0]]
world_size = 100.0
RATE = 0.95
PARTICLE_NUM = 1000

class robot(object):
    """docstring for robot"""
    def __init__(self):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0
        self.turn_noise = 0.0
        self.sense_noise = 0.0

    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise ValueError, 'X coordinate out of bound'
        if new_y < 0 or new_y >= world_size:
            raise ValueError, 'Y coordinate out of bound'
        if new_orientation < 0 or new_orientation >= 2.0 * pi:
            raise ValueError, 'Orientation out of bound'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        self.forward_noise = float(new_f_noise)
        self.turn_noise = float(new_t_noise)
        self.sense_noise = float(new_s_noise)

    def sense(self):
        Z = []
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z

    def move(self, turn, forward):
        if forward < 0:
            raise ValueError, 'Robot cant move backwards'
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi

        #move and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= world_size
        y %= world_size

        #set particle
        res = robot()
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res

    def random_move(self):
        turn = 0
        forward = 5
        return self.move(turn, forward)

    def Gaussian(self, mu, sigma, x):
        #calculate the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0 ) / sqrt(2.0 * pi * (sigma ** 2))

    def measurement_prob(self, measurement):
        # calculates how likely a measurement should be
        prob = 1.0
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob

    def __repr__(self):
        return '[x = %.6s y = %.6s orient = %.6s]' % (str(self.x), str(self.y), str(self.orientation))


def eval(r, p):
    sum = 0.0
    for i in range(len(p)): # calculate mean error
        dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
        dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))

def calculate_mean(particles, w):
    sum_x = 0
    sum_y = 0
    sum_w = 0

    for i in range(PARTICLE_NUM):
        particle = particles[i]
        sum_x += particle.x * w[i]
        sum_y += particle.y * w[i]
        sum_w += w[i]

    x = sum_x / sum_w
    y = sum_y / sum_w
    cnt = 0
    for particle in particles:
        dist = sqrt((particle.x - x) ** 2 + (particle.y - y) ** 2)
        if (dist < 5):
            cnt += 1
    return x, y, cnt > PARTICLE_NUM * RATE

myrobot = robot()
myrobot = myrobot.move(0.1, 5.0)
Z = myrobot.sense()

p = []
for i in range(PARTICLE_NUM):
    r = robot()
    r.set_noise(0.05, 0.05, 5.0)
    p.append(r)
print eval(myrobot,p)

painter = painter(world_size, landmarks, robot, p)
# while True:
#     painter.draw_landmarks(landmarks)
while True:
    #move robot
    myrobot = myrobot.move(0.1, 5.0)
    Z = myrobot.sense()

    #move particles
    p2 = []
    for i in range(PARTICLE_NUM):
        p2.append(p[i].move(0.1, 5.0))
    p = p2
    #evaluate
    w = []
    for i in range(PARTICLE_NUM):
        w.append(p[i].measurement_prob(Z))

    x, y, accept = calculate_mean(p, w)


    painter.draw_robot(myrobot)
    painter.draw_mean(x, y, accept)
    painter.draw_particles(p)
    painter.draw_landmarks()
    #resampling
    p3 = []
    index = int(random.random() * PARTICLE_NUM)
    beta = 0.0
    mw = max(w)
    for i in range(PARTICLE_NUM):
        beta += random.random() * 2.0 * mw
        while beta > w[index]:
            beta -= w[index]
            index = (index + 1) % PARTICLE_NUM
        p3.append(p[index])
    p = p3
    print eval(myrobot,p)