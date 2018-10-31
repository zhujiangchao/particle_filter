import turtle
turtle.tracer(False)
turtle.speed(0)
turtle.register_shape("tri", ((-3, -2), (0, 3), (3, -2), (0, 0)))

landmarks = [[20.0, 20.0],
             [80.0, 80.0],
             [20.0, 80.0],
             [80.0, 20.0]]
world_size = 100.0

#
# def draw_landmarks(landmarks):
#     turtle.color("black")
#     for landmark in landmarks:
#         x, y = landmark[0], landmark[1]
#         print x, y
#         turtle.up()
#         turtle.setposition(x, y)
#         turtle.down()
#         turtle.begin_fill()
#         turtle.circle(10)
#         turtle.end_fill()
#         turtle.up()
#     turtle.update()
#
# while True:
#     draw_landmarks(landmarks)

class painter(object):
    def __init__(self, world_size, landmarks, robot, particles):
        turtle.setworldcoordinates(0, 0, world_size, world_size)
        self.world_size = world_size
        self.landmarks = landmarks
        self.robot = robot
        self.particles = particles
        turtle.up()

    def draw_landmarks(self):
        turtle.color("black")
        self.landmarks = landmarks
        for landmark in self.landmarks:
            x, y = landmark[0], landmark[1]
            turtle.up()
            turtle.setposition(x, y)
            turtle.down()
            turtle.begin_fill()
            turtle.circle(1)
            turtle.end_fill()
            turtle.up()
        turtle.update()


    def draw_particles(self, particles):
        turtle.clearstamps()
        turtle.shape('tri')
        turtle.color("blue")
        self.particles = particles
        for particle in self.particles:
            x, y, o = particle.x, particle.y, particle.orientation
            turtle.setposition(x, y)
            turtle.setheading(90 - o)
            turtle.stamp()
        turtle.update()

    def draw_robot(self, robot):
        self.robot = robot
        x, y = self.robot.x, self.robot.y
        turtle.color("green")
        turtle.setposition(x, y)
        turtle.shape("turtle")
        turtle.setheading(90 - robot.orientation)
        turtle.stamp()
        turtle.update()

    def draw_mean(self, x, y, accept = False):
        print "draw_mean", x, y, accept
        if accept == 1:
            turtle.color("blue")
        else:
            turtle.color("red")
        turtle.setposition(x, y)
        turtle.shape("circle")
        turtle.stamp()
        turtle.update()


