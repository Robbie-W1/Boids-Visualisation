import pygame.gfxdraw
from math import sin, cos, pi, sqrt, atan2

from vectors import Vector


class Boid:
    def __init__(self, window, position=Vector(0, 0), velocity=Vector(0, 0)):
        self.position = position
        self.velocity = velocity
        self.acceleration = Vector(0, 0)
        self.heading = self.calculate_heading()
        self.window = window
        self.length = 15
        self.width = 10

        self.max_speed = 10
        self.max_force = 1
        self.perception_distance = 100
        self.alignment_weighting = 5
        self.cohension_weighting = 5
        self.separation_weighting = 1

    def calculate_heading(self, returning=False):
         
        if returning:
            return self.heading

    def flock(self, flock):
        """ 
        Runs all three flocking methods
        """
        self.acceleration += self.alignment(flock) * self.alignment_weighting
        self.acceleration += self.cohesion(flock) * self.cohension_weighting
        self.acceleration += self.separation(flock) * self.separation_weighting


    def update(self):
        """ 
        Adjusts the boid's position, using its velocity, handles edge collision, and calculates its vertices
        """

        self.velocity += self.acceleration

        speed = sqrt(self.velocity.x ** 2 + self.velocity.y ** 2)
        if speed > self.max_speed:
            speed * (self.max_speed / speed)

        self.position += self.velocity

        self.handle_edge_collisions()
        self.calculate_heading()
        self.calculate_points()

        self.acceleration *= 0

    def calculate_points(self):
        """ 
        Calculates the coordinates of the three vertices of the triangle which makes up the boid
        """
        self.front_x = int(
            self.position.x + ((self.length) * sin(self.heading)))
        self.front_y = int(
            self.position.y + ((self.length) * cos(self.heading)))

        self.back_left_x = int(
            self.position.x + ((self.width/2) * sin(self.heading+(pi/2))))
        self.back_left_y = int(
            self.position.y + ((self.width/2) * cos(self.heading+(pi/2))))

        self.back_right_x = int(
            self.position.x - ((self.width/2) * sin(self.heading+(pi/2))))
        self.back_right_y = int(
            self.position.y - ((self.width/2) * cos(self.heading+(pi/2))))

    def handle_edge_collisions(self):
        """ 
        Adjusts the position of the boid so that it wraps around when it hits an edge 
        """
        if self.position.x < 0:
            self.position.x = self.window.width
        elif self.position.x >= self.window.width:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = self.window.height
        elif self.position.y >= self.window.height:
            self.position.y = 0

    def draw(self):
        """ 
        Draws the boid, as a triangle, on the screen
        """
        pygame.gfxdraw.filled_trigon(self.window.screen,
                                     self.front_x, self.front_y,
                                     self.back_left_x, self.back_left_y,
                                     self.back_right_x, self.back_right_y,
                                     (255, 255, 255))

    def __str__(self):
        return f"Boid at ({self.x :.2f}, {self.y :.2f}),\tspeed: {self.speed :.2f},\theading: {self.heading :.2f}"

    def alignment(self, others):  # sourcery skip: extract-method
        """
        Aligns the boid to the velocity of its neighbors
        """
        target_velocity = Vector(0, 0)
        total = 0

        for other in others:
            if other is not self:
                distance = sqrt((self.position.x - other.position.x)**2 +
                                (self.position.y - other.position.y)**2)

                if distance <= self.perception_distance:
                    target_velocity += other.velocity
                    total += 1

        if total > 0:
            target_velocity /= total
            force = target_velocity - self.velocity
            force = force.set_magnitude(self.max_speed)
            force -= self.velocity
            if force.magnitude > 0:
                force = force.set_magnitude(self.max_force)

            return force

    def cohesion(self, others):  # sourcery skip: extract-method
        """ 
        Steer toward the average position of its neighboring boids
        """

        target_position = Vector(0, 0)
        total = 0

        for other in others:
            if other is not self:
                distance = sqrt((self.position.x - other.position.x)**2 +
                                (self.position.y - other.position.y)**2)

                if distance <= self.perception_distance:
                    target_position += other.position
                    total += 1

        if total > 0:
            target_position /= total
            force = target_position - self.position
            force = force.set_magnitude(self.max_speed)
            force -= self.velocity
            if force.magnitude > 0:
                force = force.set_magnitude(self.max_force)

            return force

    def separation(self, others):

        force = Vector(0, 0)
        total = 0

        for other in others:
            if other is not self:
                distance = sqrt((self.position.x - other.position.x)**2 +
                                (self.position.y - other.position.y)**2)

                if distance <= self.perception_distance:
                    difference = self.position - other.position
                    difference /= distance
                    force += difference
                    total += 1

        if total > 0:
            force /= total
            # force -= self.position
            force = force.set_magnitude(self.max_speed)
            force -= self.velocity
            if force.magnitude > 0:
                force = force.set_magnitude(self.max_force)

            return force
