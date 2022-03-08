#!/usr/bin/python3

from p5 import size, background, run
import numpy as np
from boid import Boid


width = 800
height = 800
nbBoids = 25

flock = [Boid(*np.random.rand(2) * 1000, width, height) for _ in range(nbBoids)]


def setup():
    size(width, height)


def draw():
    global flock

    background(30, 30, 47)

    for boid in flock:
        boid.edges()
        boid.apply_behaviour(flock)
        boid.update()
        boid.show()


#run(frame_rate=100)
#run(frame_rate=200)
run()
