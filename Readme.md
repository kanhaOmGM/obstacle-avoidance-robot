# Robot Obstacle Avoidance Simulator

A Python simulation of a differential drive robot with ultrasonic sensor-based obstacle avoidance.

## Requirements

- Python 3.6+
- pygame
- numpy

## Installation

```bash
pip install pygame numpy
```

## Project Structure

```
.
├── main.py          # Main simulation loop
├── classes.py       # Robot, sensor, and graphics classes
├── robot.png        # Robot sprite image
└── ROOM.png         # Map/environment image
```

## Usage

Run the simulation:

```bash
python main.py
```

## Features

- **Differential drive kinematics** - Two-wheeled robot with independent wheel control
- **Ultrasonic sensor simulation** - 250-pixel range with 40-degree field of view
- **Obstacle avoidance** - Automatic backward curved motion when obstacles detected within 100 pixels
- **Real-time visualization** - pygame-based rendering with sensor ray visualization

## Configuration

Main parameters can be adjusted in `main.py`:

```python
MAP_DIMENSIONS = (600, 1200)  # Window size
start = (100, 200)             # Starting position
sensor = 250, math.radians(40) # Range and FOV
```

Robot parameters in `classes.py`:

```python
self.maxspeed = 0.03 * self.m2p  # Maximum speed
self.min_obs_dis = 100           # Obstacle detection threshold
self.count_down = 5              # Avoidance duration (seconds)
```

## How It Works

The robot continuously:
1. Scans for obstacles using simulated ultrasonic sensor
2. Moves forward when path is clear
3. Executes backward curved motion for 5 seconds when obstacle detected within threshold
4. Returns to forward motion after avoidance maneuver

## Controls

- Close window or press X to exit

## Future Improvements

### PID Control Implementation

The current obstacle avoidance uses a simple timer-based approach. A more sophisticated method would be implementing a **PID (Proportional-Integral-Derivative) controller** for smooth and precise robot navigation.

**What is PID?**
- **Proportional (P)**: Corrects based on current error (distance to obstacle or target)
- **Integral (I)**: Corrects based on accumulated past errors
- **Derivative (D)**: Predicts future errors based on rate of change

**Benefits for this project:**
- Smoother obstacle avoidance trajectories
- Better distance maintenance from walls
- More efficient path planning
- Reduced oscillations and overshooting
- Adaptive speed control based on proximity to obstacles

The PID controller would calculate appropriate wheel speeds dynamically, replacing the fixed backward motion with responsive, proportional adjustments.

## License

MIT