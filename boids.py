from animation import Animation
from boid import Boid
from p5 import noise
from random import randint
from vectors import Vector


def main():  # sourcery skip: extract-method

    window = Animation(1000, 800, fps=60, caption="Boids", color=(50, 50, 50))

    boids = [
        Boid(
            window,
            position=Vector(randint(0, window.width),
                            randint(0, window.height)),
            velocity=Vector(randint(0, 2), randint(0, 2))
        )
        for _ in range(75)
    ]

    while True:
        window.check_quit()
        window.clear()

        for boid in boids:
            boid.flock(boids)
            boid.update()
            boid.draw()

        # print(boids[1].velocity.magnitude)
        window.draw()

        window.set_caption(f"Boids @ {window.clock.get_fps() :.2f} fps")


if __name__ == "__main__":
    main()
