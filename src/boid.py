from p5 import Vector, stroke, circle
import numpy as np

class Boid():

    def __init__(self, x, y, width, height):
        self.position = Vector(x, y)
        vec = (np.random.rand(2) - 0.5) * 10
        self.velocity = Vector(*vec)

        vec = (np.random.rand(2) - 0.5) / 2
        self.acceleration = Vector(*vec)
        self.max_speed = 5
        self.perception = 100

        self.width = width
        self.height = height


    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration

        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed

        self.acceleration = Vector(*np.zeros(2))


    def show(self):
        stroke(255)
        circle((self.position.x, self.position.y), 5)


    def apply_behaviour(self, boids):
        self.acceleration += self.allTogether(boids)


    def edges(self):
        if self.position.x > self.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.width

        if self.position.y > self.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.height


    def align(self, total, avg_vector):
        steering = Vector(*np.zeros(2))

        avg_vector /= total
        avg_vector = Vector(*avg_vector)
        avg_vector = (avg_vector / np.linalg.norm(avg_vector)) * self.max_speed
        steering = avg_vector - self.velocity

        return steering


    def cohesion(self, total, center_of_mass):
        steering = Vector(*np.zeros(2))
        # max_force = 0.3
        max_force = 0.7

        center_of_mass /= total
        center_of_mass = Vector(*center_of_mass)
        vec_to_com = center_of_mass - self.position
        if np.linalg.norm(vec_to_com) > 0:
            vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * self.max_speed
        steering = vec_to_com - self.velocity
        if np.linalg.norm(steering) > max_force:
            steering = (steering / np.linalg.norm(steering)) * max_force

        return steering


    def separation(self, total, avg_vector):
        steering = Vector(*np.zeros(2))
        max_force = 1

        avg_vector /= total
        avg_vector = Vector(*avg_vector)
        if np.linalg.norm(steering) > 0:
            avg_vector = (avg_vector / np.linalg.norm(steering)) * self.max_speed
        steering = avg_vector - self.velocity
        if np.linalg.norm(steering) > max_force:
            steering = (steering / np.linalg.norm(steering)) * max_force

        return steering


    def allTogether(self, boids):
        steering = Vector(*np.zeros(2))

        align_total = 0
        align_avg_vector = Vector(*np.zeros(2))

        cohesion_total = 0
        cohesion_center_of_mass = Vector(*np.zeros(2))

        separation_total = 0
        separation_avg_vector = Vector(*np.zeros(2))

        for boid in boids:
            if self.position == boid.position: continue
            distance = np.linalg.norm(boid.position - self.position)

            if distance < self.perception / 2:
                diff = self.position - boid.position
                diff /= distance
                separation_avg_vector += diff
                separation_total += 1

            elif distance < self.perception and distance > self.perception / 5:
                cohesion_center_of_mass += boid.position
                cohesion_total += 1

            if distance < self.perception:
                align_avg_vector += boid.velocity
                align_total += 1

        if align_total > 0:
            steering += self.align(align_total, align_avg_vector)
        if cohesion_total > 0:
            steering += self.cohesion(cohesion_total, cohesion_center_of_mass)
        if separation_total > 0:
            steering += self.separation(separation_total, separation_avg_vector)

        return steering
