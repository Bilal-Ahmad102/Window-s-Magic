import pyglet as pg
from window import Window
from balls import *
import subprocess
import numpy as np
from pyglet.gl import gl
import platform
import ctypes

class Main():
    def __init__(self) -> None:
        self.windows = np.array([])
        self.size_x = 300
        self.size_y = 300
        self.nums_of_windows = 2
        # self.colors = ((255, 131, 67),(23, 155, 174),(65, 88, 166))
        # self.colors =((41, 95, 152),(205, 194, 165),(225, 215, 198))
        # self.colors =((30, 32, 30),(60, 61, 55),(105, 117, 101))
        self.colors =((55, 149, 189),(166, 227, 233),(203, 241, 245))
        self.os_name = platform.system()
        self.setup()
        
        self.wins_pos = [win.window.get_location() for win in self.windows]
        self.window_hierarchy = [len(self.windows)-i for i in range(len(self.windows))]
        pg.clock.schedule_interval(self.update, 1/30)
        pg.clock.schedule_interval(self.balls_coming, 1/2)

        self.background_window = pg.window.Window(1380,720)
        self.background_window.push_handlers(on_draw=self.draw)
        self.background_window.set_location(20,0) 
        self.change = True
        self.balls_start = False

    def balls_coming(self,dt):
        if self.balls_start:
            self.windows[0].setup()
            
    def setup(self):
        # x,y = 100,150
        x_loc = 0
        for num in range(1,self.nums_of_windows+1):
            self.windows = np.append(self.windows,Window(self.size_x,self.size_y,500,200,num,(self.colors[0],self.colors[1])))
        self.windows[0].target_x,self.windows[0].target_y = 500,200
    def move_location(self):

        y = self.windows[0].target_y+60
        for win in self.windows:
            y -= 60
            win.target_y = y


    def get_last_active_window_linux(self):
        # Get the window ID of the last active window
        window_id = subprocess.check_output(["xdotool", "getactivewindow"]).decode('utf-8').strip()

        # Get the window name using the window ID
        window_name = subprocess.check_output(["xdotool", "getwindowname", window_id]).decode('utf-8').strip()

        return window_name

    def get_last_active_window_windows(self):
        # Get the handle of the foreground window
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        
        # Get the length of the window title
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        
        # Create a buffer for the window title
        buf = ctypes.create_unicode_buffer(length + 1)
        
        # Get the window title
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)
        
        return buf.value

    def get_last_active_window(self):
        if self.os_name == "Linux":
            window_name = self.get_last_active_window_linux()
        elif self.os_name == "Windows":
            window_name = self.get_last_active_window_windows()
        else:
            print(f"Unsupported operating system: {self.os_name}")
            return

        # Find the window with the matching name and update its hierarchy
        for win in self.windows:
            if win.window.caption == window_name:
                for rest_of_window in self.windows:
                    if win.last_active > rest_of_window.last_active:
                        rest_of_window.last_active += 1
                win.last_active = 1
                break

    def validate_overlaping(self, win_1_loc, win_2):
        def validate_x():
            return win_1_loc[0] < win_2[0] and win_1_loc[0] + self.size_x > win_2[0]

        def validate_y():
            return win_1_loc[1] < win_2[1] + self.size_y and win_1_loc[1] + self.size_y > win_2[1]

        return validate_x() and validate_y()

    def window_overlaping_check(self, win_1):
        win_1_loc = win_1.window.get_location()
        points = []

        for win_2 in self.windows:
            win_2_loc = win_2.window.get_location()

            # Don't calculate Overlapping if both windows are the same or neither has balls
            if (win_1 == win_2) or not (len(win_1.balls) > 0 or len(win_2.balls) > 0):
                continue            

            if self.validate_overlaping(win_1_loc, win_2_loc):
                win_1_loc_x = abs(win_1_loc[0] - win_2_loc[0])

                if win_1_loc[1] > win_2_loc[1]:                
                    win_1_loc_y = abs(win_1_loc[1] - win_2_loc[1])
                else:
                    win_1_loc_y = self.size_y - abs(win_1_loc[1] - win_2_loc[1])

                if win_2_loc[1] > win_1_loc[1]:                
                    win_2_loc_y = abs(win_2_loc[1] - win_1_loc[1])
                else:
                    win_2_loc_y = self.size_y - abs(win_2_loc[1] - win_1_loc[1])

                win_2_loc_x = self.size_x - abs(win_2_loc[0] - win_1_loc[0])

                points.extend([(win_1_loc_x, win_2_loc_y), (win_2_loc_x, win_1_loc_y)])
                points.extend([win_1, win_2])
                

        return points 
    def is_top_right(self,win_1_loc, win_2_loc):
            return win_1_loc[0] < win_2_loc[0] and win_1_loc[1] > win_2_loc[1]

    def is_bottom_right(self,win_1_loc, win_2_loc):
            return win_1_loc[0] < win_2_loc[0] and win_1_loc[1] < win_2_loc[1]

    def win_1(self,win_1,win_2,win_1_point,win_2_point):
        jump = False
        win_1_loc = win_1.window.get_location()
        win_2_loc = win_2.window.get_location()
        balls_to_process = list(enumerate(win_1.balls_positions))
        a = 0
        balls_to_transfer = []

        for i, ball_position in balls_to_process: 
            if i >= len(win_1.balls):
                continue  # Skip this iteration if the ball no longer exists

            if ball_position[0] + win_1.balls[i].velocity[0] >= win_1_point[0]:
                x, y = None, None
                if self.is_top_right(win_1_loc,win_2_loc):
                    # Case 1: win_2 is at top right corner and balls enter from top or right of win_1 into win_2                        
                    
                    if win_1.last_active > win_2.last_active:
                        if self.size_y - ball_position[1] > win_1_point[1]   and \
                        (ball_position[1]) + win_1.balls[i].velocity[1] > (self.size_y - win_1_point[1]) - win_1.balls[i].size:
                            a = 1 
                            y = win_1.balls[i].size
                            x = ball_position[0] - win_1_point[0]
                            

                        elif self.size_y - ball_position[1] < win_1_point[1]:
                            a = 2
                            y = self.size_y - ((self.size_y - ball_position[1]) + (self.size_y - win_1_point[1]))
                            x = win_1.balls[i].size
                            
                                       
                    else:

                        if win_1_loc[1] + (self.size_y- ball_position[1]) < win_2_loc[1] + self.size_y and \
                        (ball_position[1]) + win_1.balls[i].velocity[1]  >= self.size_y - win_1.balls[i].size - 1:
                            a = 3
                            y = self.size_y - win_2_point[1]
                            x = ball_position[0] - win_1_point[0]
                            
                        
                        elif(ball_position[0]) + win_1.balls[i].velocity[0]  >= self.size_x - win_1.balls[i].size  \
                            and win_1_loc[1] + (self.size_y - ball_position[1]) < win_2_loc[1] +self.size_y:
                            a = 4
                            y = win_1_point[1] - (self.size_y - ball_position[1])
                            x = win_2_point[0] + win_1.balls[i].size
                        
                if self.is_bottom_right(win_1_loc,win_2_loc):
                    # Case 2: win_1 is at top left corner and balls enter from bottom or right of win_1 to win_2
                    
                    if win_1.last_active > win_2.last_active:
                        
                        if self.size_y - ball_position[1] < win_1_point[1] and \
                        (self.size_y - ball_position[1]) + -(win_1.balls[i].velocity[1]) >  win_1_point[1] - win_1.balls[i].size:
                            a = 5
                            y = self.size_y - win_1.balls[i].size
                            x = ball_position[0] - win_1_point[0]
                            

                        elif self.size_y - ball_position[1] > win_1_point[1]:
                            a = 6
                            y = ball_position[1] +  win_1_point[1]
                            x = win_1.balls[i].size
                            

                    else:
                        
                        if win_1_loc[1] + (self.size_y- ball_position[1]) > win_2_loc[1]and \
                        (ball_position[1]) + (win_1.balls[i].velocity[1])  <=  win_1.balls[i].size:
                            a = 7
                            y = self.size_y - win_2_point[1]
                            x = ball_position[0] - win_1_point[0]
                            
                            

                        elif (ball_position[0]) + win_1.balls[i].velocity[0]  >= self.size_x - win_1.balls[i].size \
                            and win_1_loc[1] + (self.size_y - ball_position[1]) > win_2_loc[1]:
                            a = 8
                            y = (self.size_y - win_2_point[1]) + (ball_position[1])
                            x = win_2_point[0]
                if x is not None and y is not None:
                    balls_to_transfer.append((i, x, y, win_1.balls[i].velocity,win_1.balls[i].color))
                            
                            
        for i, x, y, velocity,color in balls_to_transfer:
            new_ball = Ball(self.size_x, self.size_y, [x, y], velocity,color)
            win_2.balls = np.append(win_2.balls, new_ball)

        # Remove transferred balls
        win_1.balls = np.delete(win_1.balls, [i for i, _, _, _,_ in balls_to_transfer])            


    def win_2(self,win_1,win_2,win_1_point,win_2_point):
        jump = False
        a = 0
        win_1_loc = win_1.window.get_location()
        win_2_loc = win_2.window.get_location()
        balls_to_process = list(enumerate(win_2.balls_positions))
        balls_to_transfer = []
        for i, ball_position in balls_to_process: 
            if i >= len(win_2.balls):
                continue  # Skip this iteration if the ball no longer exists
            if ball_position[0] + win_2.balls[i].velocity[0] <= win_2_point[0]:
                x,y = None,None
                if self.is_top_right(win_1_loc,win_2_loc):
                        # Case 1: win_1 is at bottom left corner of win_2 and balls enter from top or right
                        # win_2 is last active and win_1 is not
                        
                        if win_1.last_active < win_2.last_active:                             
                            # enters from top
                            if self.size_y - ball_position[1] < win_2_point[1] and \
                            (self.size_y - ball_position[1]) + -win_2.balls[i].velocity[1] > win_2_point[1]:
                                a = 1        
                                y = self.size_y - win_2.balls[i].size - 1
                                x = ball_position[0] + win_1_point[0]
                                
                            
                            # enters from right
                            elif self.size_y - ball_position[1] > win_2_point[1]:
                                a = 2
                                y = ball_position[1] + win_2_point[1]
                                x = self.size_x - win_2.balls[i].size - 1 
                                
                        else:
                            # win_1 is last active window and win_2 is not 
                            # Ball is passing the bottom boundary of window 2 into window 1 
                            if (ball_position[1] + win_2.balls[i].velocity[1]) <= win_2.balls[i].size:
                                a = 3
                                x = ball_position[0] + win_1_point[0]
                                y = self.size_y - win_1_point[1]
                                
                                
                            # Ball is passing the left boundary of window 2 into window 1 from the right side 
                            # and ball is below the window 1 points in window 2                                 
                            elif ball_position[0] + win_2.balls[i].velocity[0] <= win_2.balls[i].size and \
                                win_2_loc[1] + (self.size_y - ball_position[1]) >= win_1_loc[1]: 
                                a = 4
                                y = (ball_position[1]) + (self.size_y - win_1_point[1]) 
                                x = win_1_point[0]
                                
                            
                elif self.is_bottom_right(win_1_loc,win_2_loc):
                        # Case 2: win_1 is at bottom right corner and balls enter win_2  from bottom or right
                        
                        if win_1.last_active < win_2.last_active:
                            if self.size_y - ball_position[1]  > win_2_point[1] - win_2.balls[i].size and \
                            self.size_y - (ball_position[1] + win_2.balls[i].velocity[1]) <=  win_2_point[1]:
                                a = 5
                                y = win_2.balls[i].size
                                x = ball_position[0] + win_1_point[0]
                                
                            elif self.size_y - ball_position[1] < win_2_point[1]:
                                a = 6
                                y = self.size_y - (self.size_y - ball_position[1] +  win_1_point[1])
                                x = self.size_x - win_2.balls[i].size 
                                
                        else:

                            # Ball is passing the top boundary of window 2 into window 1 from the Down side
                            if ball_position[1] + win_2.balls[i].velocity[1] >= self.size_y - win_2.balls[i].size:
                                a = 7
                                x = ball_position[0] + win_1_point[0]
                                y = self.size_y - win_1_point[1]
                                
                            # Ball is passing the left boundary of window 2 into window 1 from the right side and ball is above the window 1 points in window 2                                 
                            elif ball_position[0] + win_2.balls[i].velocity[0] <= win_2.balls[i].size and  \
                                win_2_loc[1] + (self.size_y - ball_position[1]) < win_1_loc[1] + self.size_y: 
                                a = 8
                                y =   ball_position[1] - (self.size_y - win_2_point[1]) 
                                x = win_1_point[0]
                if x is not None and y is not None:
                    balls_to_transfer.append((i, x, y, win_2.balls[i].velocity,win_2.balls[i].color))

                                
                
        for i, x, y, velocity,color in balls_to_transfer:

            new_ball = Ball(self.size_x, self.size_y, [x, y], velocity,color)
            win_1.balls = np.append(win_1.balls, new_ball)
        
        # Remove transferred balls
        win_2.balls = np.delete(win_2.balls, [i for i, _, _, _,_ in balls_to_transfer])            
            
    def balls_passing_windows(self, win_1_point, win_2_point, win_1, win_2):
        if len(win_1.balls) > 0:
            self.win_1(win_1, win_2, win_1_point, win_2_point)

        if len(win_2.balls) > 0:
            self.win_2(win_1, win_2, win_1_point, win_2_point)
            
    def update(self, dt: float) -> None:
        """
        Updates all windows and checks for ball passing between them.

        Parameters:
            dt (float): The time elapsed since the last update.
        """
        # if not self.windows[-1].moving and self.windows[-1].move_times >= 1 and self.change:
        #     self.move_location() 
        #     self.change = False
        for wins in self.windows:
            # if wins.flag_move:
            #     for win in self.windows:
            #         win.moving = True
            #         win.move_times += 1
            #     win.flag_move = False                         
                
            wins.update(dt)
            if wins.initialize_balls:
                # self.balls_start = not self.balls_start 
                self.windows[0].setup()
                wins.initialize_balls = False
            points = self.window_overlaping_check(wins)            
            if len(points) > 4: self.balls_passing_windows(points[4], points[5], points[6], points[7]) 
            if len(points) > 0:
                self.balls_passing_windows(points[0], points[1], points[2], points[3])

        self.get_last_active_window()
    def draw(self):
        self.background_window.clear()
        # gl.glClearColor(0.0, 0.7, 0.8, 1.0)  # A bright and lively aqua blue color
        r,g,b = self.colors[2]
        gl.glClearColor(r/255, g/255, b/255, 1.0)  # A modern and sleek cool gray

    def run(self):
        
        for window in self.windows:
            window.run()

        pg.app.run()



main = Main()
main.run()
