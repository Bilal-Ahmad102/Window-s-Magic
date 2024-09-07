from pyglet.shapes import Circle
import numpy as np
import pyglet as pg
from random import randint, uniform, choice

# At the module level, create a pool of players
PLAYER_POOL = [pg.media.Player() for _ in range(10)]  # Adjust the number as needed

class Ball:
    def __init__(self, width, height, position=None, velocity=None, color=None) -> None:
        self.width = width
        self.height = height

        minus_velocity_left  = -20
        minus_velocity_right = -10
        plus_velocity_left  = 10
        plus_velocity_right = 20

        self.max_velocity = randint(plus_velocity_left, plus_velocity_right)
        self.min_velocity =  randint(minus_velocity_left, minus_velocity_right)
        
        if position is None:
            self.pos = np.array([float(width // 2), float(height // 2)])
        else:
            self.pos = np.array(position, dtype=float)

        if velocity is not None:
            self.velocity = np.array(velocity, dtype=float)
        else:
            self.velocity = np.array([uniform(-self.max_velocity, self.max_velocity), 
                                      uniform(-self.max_velocity, self.max_velocity)])
            # self.velocity = np.array([0.7*5,-0.7*5],dtype=float)
        self.shape = None
        self.size = 5
        self.segments = 100
        if color is None:
            self.color = (255,255,255)
        else:
            self.color = color
        self.sounds = []
        self.setup()

    def setup(self):
        for i in range(2, 6):
            self.sounds.append(pg.media.load(f'sounds/{i}.wav', streaming=False))

    def show(self, batch):
        if self.shape is None:
            self.shape = Circle(self.pos[0], self.pos[1], self.size,
                                self.segments, self.color, batch=batch)    
        else:
            self.shape.x = self.pos[0]
            self.shape.y = self.pos[1]

    def update(self):
        new_position = self.pos + self.velocity
        bounce = False

        if new_position[0] >= self.width or new_position[0]  <= 0:
            self.velocity[0] = -self.velocity[0]
            bounce = True
        if new_position[1]  >= self.height or new_position[1]  <= 0:
            self.velocity[1] = -self.velocity[1]
            bounce = True

        if bounce:
            sound = choice(self.sounds)
            # Find an available player from the pool
            for player in PLAYER_POOL:
                if not player.playing:
                    player.queue(sound)

                    player.play()
                    break
            else:
                # If all players are busy, create a new one-time player
                pg.media.Player().queue(sound).play()
                print("All players are busy. Creating a new one-time player.")
        self.pos = new_position
