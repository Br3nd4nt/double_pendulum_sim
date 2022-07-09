import pygame as pg
import math
import random

# global variables
BG_COLOR = pg.Color('#000000')
PD_COLOR = pg.Color('#FFFFFF')
G = 1
size = width, height = 2560, 1440
start_coords = width // 2, height // 2
first_mass = 20
second_mass = 20
first_angle = math.pi / 2
second_angle = 2 * math.pi / 4
first_length = 300
second_length = 300
path = []

first_velocity = 0
second_velocity = 0
first_acceleration = 0
second_acceleration = 0

def main():
    global first_velocity, second_velocity, first_acceleration, second_acceleration, first_angle, second_angle, path, first_mass, second_mass, first_length, second_length
    pg.display.set_caption('Double pendulum')
    screen = pg.display.set_mode(size, pg.FULLSCREEN)
    clock = pg.time.Clock()
    running = True
    counter = 0
    showing_pendulum = True
    while running:
        first_coords = (first_length * math.sin(first_angle) + start_coords[0], first_length * math.cos(first_angle) + start_coords[1])
        second_coords = (second_length * math.sin(second_angle) + first_coords[0], second_length * math.cos(second_angle) + first_coords[1])
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                showing_pendulum = not showing_pendulum
        # updating trail
        screen.fill(color=BG_COLOR)
        path += [second_coords]
        for dot in range(1, len(path)):
            color = pg.Color(0, 0, 0)
            color.hsva = (len(path) - dot) % 360, 100, 20
            # pg.draw.ellipse(screen, PD_COLOR, pg.Rect(dot[0] - 1, dot[1] - 1, 1, 1))
            pg.draw.line(screen, color, path[dot - 1], path[dot])
        path = path[len(path)-360 * 5:]
        # doing the math
        
        first_acceleration = (-G * (2 * first_mass + second_mass) * math.sin(first_angle) - second_mass * G * math.sin(first_angle - 2 * second_angle) - 2 * math.sin(first_angle - second_angle) * second_mass * (second_velocity ** 2 * second_length + first_velocity ** 2 * first_length * math.cos(first_angle - second_angle))) / (first_length * (2 * first_mass + second_mass - second_mass * math.cos(2 * first_angle - 2 * second_angle)))

        second_acceleration = (2 * math.sin(first_angle - second_angle) * (first_velocity ** 2 * first_length * (first_mass + second_mass) + G * (first_mass + second_mass) * math.cos(first_angle) + second_velocity ** 2 * second_length * second_mass * math.cos(first_angle - second_angle))) / (second_length * (2 * first_mass + second_mass - second_mass * math.cos(2 * first_angle - 2 * second_angle)))


        first_velocity += first_acceleration
        second_velocity += second_acceleration
        first_angle += first_velocity
        second_angle += second_velocity
        # drawing pendulum
        if showing_pendulum:
            # first

            pg.draw.line(screen, PD_COLOR, start_coords, first_coords)
            pg.draw.ellipse(screen, PD_COLOR, pg.Rect(first_coords[0] - first_mass // 2, first_coords[1] - first_mass // 2, first_mass, first_mass))
            
            # second
            
            pg.draw.line(screen, PD_COLOR, first_coords, second_coords)
            pg.draw.ellipse(screen, PD_COLOR, pg.Rect(second_coords[0] - second_mass // 2, second_coords[1] - second_mass // 2, second_mass, second_mass))

        counter += 1
        print(counter)
        if counter > 8000:
            counter = 0
            first_mass = random.randint(5, 100)
            second_mass = random.randint(5, 100)
            first_angle = math.pi * random.random()
            second_angle = math.pi * random.random()
            first_length = random.randint(50, 600)
            second_length = random.randint(50, 600)
            path = []
            first_velocity = 0
            second_velocity = 0
            first_acceleration = 0
            second_acceleration = 0

        pg.display.flip()
        clock.tick(60)
    pg.quit()


if __name__ == '__main__':
    main()