def process_segment(P_start, P_end, K, rho_tol, t0=0, tf=days2sec(10), freq=1):
    
    # Compute Initial Relative State
    R0 = P2R(P_start, P_end)

    # Define Time Domain
    tspan = np.arange(t0, tf + 1, 1 / freq)

    # Initialize variables for Euler integration
    R = np.zeros((R0.shape[0], len(tspan)))
    dR = np.zeros((R0.shape[0], len(tspan)))
    controls = np.zeros((2, len(tspan)))
    R[:, 0] = R0
    reached_target = False

    # Perform Euler Integration
    for i in range(1, len(tspan)):
        dt = tspan[i] - tspan[i-1]

        # Unpack State Variables
        rho, alpha, beta = R[:, i-1]

        # Compute Control
        v, omega = Move2Pose(R[:, i-1], K)

        # Compute Derivatives
        drho = -np.cos(alpha) * v
        dalpha = np.sin(alpha) * v / rho - omega
        dbeta = -np.sin(alpha) * v / rho

        # Euler Integration
        controls[:, i] = np.array([v, omega])
        dR[:, i] = np.array([drho, dalpha, dbeta])
        R[:, i] = R[:, i-1] + dR[:, i] * dt

        # Check for Arrival
        if rho <= rho_tol:
            reached_target = True
            break

    if reached_target:
        R = R[:, :i + 1]
        dR = dR[:, :i + 1]
        controls = controls[:, :i + 1]
        tspan = tspan[:i + 1]

    return R2P(R, P_end), controls, tspan

# Define Viapoints
viapoints = np.array([[34.5*1e3, 15*1e3, np.pi/2], P1])
[41541.8043] [15452.0639]

# Select Gains and Tolerance
K = np.array([1e-4, 1.4e-3, -1e-3])
rho_tol = 0.1  # m

# Initialize Variables
P = np.empty((3, 0))  # Assuming P is 3xN
u = np.empty((2, 0))  # Assuming controls is 2xN
tspan = np.array([])

P_start = P0
t_start = 0

# Perform the Integration for all Via Points
for i in range(len(viapoints)):

    P_int, controls_int, tspan_int = process_segment(P_start, viapoints[i], K, rho_tol, t_start)

    # Stack the results
    P = np.hstack((P, P_int))
    u = np.hstack((u, controls_int))
    tspan = np.concatenate((tspan, tspan_int))

    # Check for obstacles
    P_indices = np.array([get_indices(P_int[0:2, i], X, Y, mapRes) for i in range(P_int.shape[1])])
    if check_obstacles(P_indices, obstacleMap):
        print('\n\nThe Trajectory intersects with an Obstacle!\n')
        break

    # Show Trajectory in Obstacle Map
    plt.figure()
    plt.imshow(obstacleMap, cmap='gray', extent=(Xvec[0], Xvec[-1], Yvec[-1], Yvec[0]))
    plt.plot(P_int[0, :], P_int[1, :], '#6beb34', linestyle='-', linewidth=1)
    plt.plot(P_start[0], P_start[1], 'go', markersize=4)
    plt.plot(viapoints[i][0], viapoints[i][1], 'bo', markersize=4)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

    P_start = P_int[:, -1]          # store the real final state -> start of next segment
    t_start = tspan_int[-1]         # store the real final time -> start of next segment

P1r = P[:, -1]  # Store the real final state


# Log Results
print('\nTask 1\n' + '_' * 70, '\n\nThe Initial State is:\t', P0)
print('The Final State is:\t', P[:, -1])
print('The Desired State is:\t', P1)
print('\nThe Delta State is:\t', P[:, -1] - P1)
print('Final Time is:\t\t {:.2f} days'.format(sec2days(tspan[-1])))


# Show Trajectory in Map
plt.figure(figsize=(8, 6))
plot_map(map_image, Xvec, Yvec)
plt.plot(P[0, :], P[1, :], '#6beb34', linestyle='-', linewidth=1)
plt.plot(P0[0], P0[1], 'go', markersize=4)
plt.plot(P1[0], P1[1], 'bo', markersize=4)
plt.savefig('Images/nav_traj.jpg', format='jpg', dpi=300)
plt.show()

# Show Trajectory in Obstacle Map
plt.figure()
plt.imshow(obstacleMap, cmap='gray', extent=(Xvec[0], Xvec[-1], Yvec[-1], Yvec[0]))
plt.plot(xLM, yLM, 'yo', markersize=5, linewidth=2)
plt.plot(P[0, :], P[1, :], '#6beb34', linestyle='-', linewidth=1)
plt.plot(P0[0], P0[1], 'go', markersize=4)
plt.plot(P1[0], P1[1], 'bo', markersize=4)
plt.xlabel(r'$x \ [m]$')
plt.ylabel(r'$y \ [m]$')
plt.savefig('Images/nav_traj_obst.jpg', format='jpg', dpi=300)
plt.show()


# Visualize the Control Variables
plt.figure()

plt.subplot(1, 2, 1)    # Linear Velocity
plt.plot(tspan/60**2, controls[0, :], label='v')
plt.xlabel('$t \ [hrs]$')
plt.ylabel('$v \ [m/s]$')
plt.grid(True)

plt.subplot(1, 2, 2)    # Angular Velocity
plt.plot(tspan/60**2, controls[1, :], label='omega')
plt.xlabel('$t \ [hrs]$')
plt.ylabel(r'$\omega \ [rad/s]$')
plt.grid(True)

plt.tight_layout()
plt.savefig('Images/controls.jpg', format='jpg', dpi=300)
plt.show()
