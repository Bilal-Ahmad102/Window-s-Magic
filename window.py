import pyglet as pg
from balls import Ball
import numpy as np
import math
from pyglet import gl
from pyglet.window import key


class Window:
    def __init__(self, width, height, loc_x, loc_y, num, color) -> None:
        """
        Initialize the Window class.

        This class represents a window in the game. A window is where the balls are drawn and updated.

        Parameters
        ----------
        width : int
            The width of the window.
        height : int
            The height of the window.
        loc_x : int
            The x location of the window.
        loc_y : int
            The y location of the window.
        num : int
            The number of the window.
        color : tuple
            The color of the window and balls.
        """

        # Load the circular image into pyglet
        logo = pg.image.load(f"logos//logo_2.png")

        self.window = pg.window.Window(
            width=width, height=height, caption="win " + str(num)
        )
        self.window.set_location(loc_x, loc_y)
        self.window.set_icon(logo)

        self.width = self.window.width
        self.height = self.window.height
        self.batch = pg.graphics.Batch()
        self.window.push_handlers(on_draw=self.draw, on_key_press=self.on_key_press)
        self.last_active = num
        self.balls = np.array([])
        self.balls_positions = None
        self.num_of_balls = 1
        self.fps = pg.window.FPSDisplay(self.window)
        self.color = color
        self.initialize_balls = False

        self.flag_move = False

        # New attributes for window movement
        self.target_x = None
        self.target_y = None
        self.current_x = loc_x
        self.current_y = loc_y
        self.velocity = 50  # pixels per second
        self.moving = False
        self.move_times = 0

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.initialize_balls = not self.initialize_balls
        elif symbol == key.M:  # Press 'M' to move the window
            self.flag_move = True

    def setup(self):
        """
        Setup method for the Window class.
        This method creates and appends a Ball object to the balls list.
        """
        for _ in range(self.num_of_balls):
            ball = Ball(self.width, self.height, color=self.color[0])
            self.balls = np.append(self.balls, ball)

    def move(self, dt):
        # Move the window if it's not at the target location
        if self.moving:
            dx = self.target_x - self.current_x
            dy = self.target_y - self.current_y
            distance = math.sqrt(dx**2 + dy**2)

            if distance > 10:
                move_distance = min(self.velocity * dt, distance)
                angle = math.atan2(dy, dx)
                self.current_x += move_distance * math.cos(angle)
                self.current_y += move_distance * math.sin(angle)
                self.window.set_location(int(self.current_x), int(self.current_y))
            else:
                self.current_x = self.target_x
                self.current_y = self.target_y
                self.window.set_location(self.target_x, self.target_y)
                self.moving = False

    def update(self, dt):
        """
        Update method for the window class.

        This method updates the positions of the balls in the window and moves the window if necessary.

        Parameters:
            dt (float): The time elapsed since the last update.
        """
        self.move(dt)
        # Update balls
        self.balls_positions = np.array([])

        if len(self.balls) > 0:
            for ball in self.balls:
                ball.show(self.batch)
                ball.update()

            self.balls_positions = np.array([ball.pos for ball in self.balls])

    def draw(self):
        """
        Draw method for the Window class.

        This method clears the window and then draws the batch of shapes.
        """
        self.window.clear()
        r, g, b = self.color[1]
        gl.glClearColor(r / 255, g / 255, b / 255, 1.0)
        self.batch.draw()

    def run(self):
        """
        Run method for the Window class.
        """
        pg.app.run()
