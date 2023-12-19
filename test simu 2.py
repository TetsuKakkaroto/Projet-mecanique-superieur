import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define the constant (tous est * 10**11)
m1 = 1
m2 = 100
lz = 70
# Variable
mu = (m1*m2)/(m1+m2)
M = m1+m2
G = 6.673

# Define the curve function
def curve_function(x):
    y = (lz**2)/(2*mu*(x**2)) - ((G*m1*m2)/(x))  # Change this function according to your curve
    return y

# First derivative of the curve function to determine slope
def curve_slope(x):
    h = 1e-5
    return (curve_function(x + h) - curve_function(x)) / h

# On calcule le minimum de x
x_min = None  # Initialize x_min to None
for i in np.arange(0.1, 500, 0.05):
    if curve_slope(i) >= -0.1 and curve_slope(i) <= 0.1:
        if x_min is None or curve_function(i) < curve_function(x_min):
            x_min = i  # Update x_min only if it's None or the function value at i is smaller
print(x_min)

# Set up the plot for the first simulation (sliding particle)
fig1, ax1 = plt.subplots()
particle1, = ax1.plot([], [], 'bo', markersize=8)
trajectory1, = ax1.plot([], [], 'r-')

# Particle parameters for the first simulation
initial_x1 = float(input("Initial x for sliding particle = "))
initial_y1 = curve_function(initial_x1)
gravity = 9.8

# Set the axis limits for the first plot
ax1.set_xlim(0, initial_x1 +50)
ax1.set_ylim(initial_y1 - 20, initial_y1 + 80)

# Simulation parameters
dt = 0.02  # Time step
velocity_gain_factor = 1  # Adjust this factor to control the rate of velocity gain

# Initialization function for the first animation
def init1():
    particle1.set_data([], [])
    trajectory1.set_data([], [])
    return particle1, trajectory1

# Animation function for the first simulation
def update1(frame):
    global initial_x1, velocity1, prev_velocity1, prev_x1, t0, check, d0, initial_y1

    # Update particle position
    t1 = frame * dt

    # Update velocity based on sliding down the curve
    if curve_slope(prev_x1) > 0:
        velocity1 -= gravity * dt * velocity_gain_factor * abs(curve_slope(prev_x1))  # Lose velocity zhen going up

    # Lose velocity when going uphill on the concave part
    if curve_slope(prev_x1) < 0:
        velocity1 += gravity * dt * velocity_gain_factor * abs(curve_slope(prev_x1))  # Gain velocity when going down

    # No change in velocity when going on a straight line
    if curve_slope(prev_x1) == 0:
        pass

    # Update particle position
    x1 = prev_x1 + velocity1 * np.cos(np.arctan(curve_slope(4)))
    y1 = curve_function(x1)

    # Store previous velocity and x position
    prev_velocity1 = velocity1
    prev_x1 = x1
    prev_y1 = y1

    particle1.set_data(x1, y1)

    # Update trajectory for the first simulation
    x_values1 = np.linspace(0, 100, 100000)
    y_values1 = curve_function(x_values1)
    trajectory1.set_data(x_values1, y_values1)

   # Check if the particle has reached its original position
    if frame > 0 and y1 >= (curve_function(initial_x1) - 0.005) and y1 <= (curve_function(initial_x1) + 0.005) and check == 0:
        t0 = t1
        check += 1
    
    if check ==0 :
        d0 += abs(velocity1)*dt

    return particle1, trajectory1


    return particle1, trajectory1

# Initial velocity is zero
velocity1 = 0
prev_velocity1 = 0
prev_x1 = initial_x1
t0 = 1
check = 0
d0=1
prev_y1 = initial_y1

# Create the first animation
animation1 = FuncAnimation(fig1, update1, frames=range(10000), init_func=init1, blit=True)

# Set up the plot for the second simulation (orbiting particle)
fig2, ax2 = plt.subplots()
particle2, = ax2.plot([], [], 'bo', markersize=8)
trail2, = ax2.plot([], [], 'b-', alpha=0.5)  # Trail for the blue particle
center_point, = ax2.plot([], [], 'ko')  # Black point at the center

# Lists to store historical positions
particle2_history_x = []
particle2_history_y = []

# Particle parameters for the second simulation
initial_x2 = 0.0
initial_y2 = 0.0

# Set the axis limits for the second plot
ax2.set_xlim(-50, 50)
ax2.set_ylim(-50, 50)

# Initialization function for the second animation
def init2():
    particle2.set_data([], [])
    trail2.set_data([], [])
    center_point.set_data([], [])
    return particle2, trail2, center_point

# Lists to store historical positions for the second simulation
particle2_history_x_before = []
particle2_history_y_before = []
particle2_history_x_after = []
particle2_history_y_after = []

# Animation function for the second simulation
def update2(frame):
    global initial_x2, initial_y2, distance, angle, velocity2, check

    t2 = frame * dt

    # Update orbit parameters in real-time
    distance = prev_x1  # Distance from the first simulation
    angular_velocity = (lz / (mu * (abs(prev_x1**2)))) * (d0 / t0)  # Same speed as the first simulation
    # Calculate particle position in orbit
    angle += angular_velocity * dt * velocity_gain_factor
    x2 = initial_x2 + distance * np.cos(angle)
    y2 = initial_y2 + distance * np.sin(angle)

    particle2.set_data(x2, y2)

    # Update trail color based on check
    if check == 1:
        # Change the trail color to red when check is 1
        particle2_history_x_after.append(x2)
        particle2_history_y_after.append(y2)
        trail2.set_data(particle2_history_x_after, particle2_history_y_after)
    else:
        # Keep the trail color blue when check is not 1
        particle2_history_x_before.append(x2)
        particle2_history_y_before.append(y2)
        trail2.set_data(particle2_history_x_before, particle2_history_y_before)

    # Update center point
    center_x = 0
    center_y = 0
    center_point.set_data(center_x, center_y)

    if check == 0:
        trail2.set_color('purple')
    else:
        # Keep the trail color blue when check is not 1
        trail2.set_color('blue')

    return particle2, trail2, center_point
# Initial values for the second simulation
distance = prev_x1
angle = np.random.uniform(0, 2 * np.pi)
velocity2 = velocity1

# Create the second animation
animation2 = FuncAnimation(fig2, update2, frames=range(10000), init_func=init2, blit=True)

plt.show()
print(t0)
print(d0)