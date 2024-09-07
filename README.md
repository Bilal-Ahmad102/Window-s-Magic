# Window's Magic: A Multi-Window Bouncing Balls Simulation

This project is an interactive simulation of bouncing balls across multiple windows using Pyglet. It demonstrates advanced concepts in graphics programming, window management, and physics simulations.

## Features

- Multiple interactive windows
- Bouncing balls with realistic physics
- Inter-window ball movement
- Sound effects on ball collisions
- Window hierarchy management
- Customizable colors and settings
- FPS display
- Keyboard controls for interaction

## Requirements

- Python 3.x
- Pyglet
- NumPy
- xdotool (for Linux window management)
- ctypes (for Windows window management)
- There is not any window management system for linux right now in project, feel free to implement your own

## Installation

1. Clone this repository or download the source code.
2. Install the required dependencies:

```
pip install pyglet numpy
```

3. If you're on Linux, ensure you have xdotool installed:

```
sudo apt-get install xdotool
```
or For windows install ctypes

```
pip install ctypes
```

## Usage

Run the `main.py` file to start the simulation:

```
python main.py
```

### Controls:
- Press 'SPACE' to initialize or reset balls
- Press 'M' to trigger window movement (if implemented)

## Files

- `main.py`: Sets up the main simulation environment and manages multiple windows
- `window.py`: Implements the `Window` class for individual simulation windows
- `balls.py`: Contains the `Ball` class for ball physics and rendering
- `colors.py`: (Not provided, but referenced) Likely contains color definitions

## How It Works

1. The simulation creates multiple windows using Pyglet.
2. Each window contains its own set of bouncing balls.
3. Balls can move between windows when they overlap.
4. The program tracks window hierarchy based on user interaction.
5. Physics calculations ensure realistic ball movement and collisions.
6. Sound effects play when balls collide with window boundaries.

## Customization

You can customize the simulation by modifying the following:

- In `main.py`:
  - Adjust `self.size_x` and `self.size_y` to change window sizes
  - Modify `self.colors` to change the color scheme
  - Adjust `self.nums_of_windows` to change the number of simulation windows

- In `balls.py`:
  - Modify ball physics parameters like `self.max_velocity` and `self.min_velocity`
  - Change `self.size` to adjust ball size

- In `window.py`:
  - Adjust `self.velocity` to change window movement speed
  - Modify `self.num_of_balls` to change the initial number of balls per window

## Contributing

Contributions to improve the simulation or add new features are welcome. Please feel free to submit pull requests or open issues for any bugs or enhancements.

## License

This project is open-source and available under the MIT License.

## Acknowledgements

This project uses the Pyglet library for graphics rendering and window management.