import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat


def load_data(filename='Data/exercise.mat'):

    data = loadmat(filename)

    X = data['X']
    Y = data['Y']
    map_image = data['map']
    obstacleMap = data['obstacleMap']
    xLM = data['xLM']
    yLM = data['yLM']
    Xvec = data['Xvec']
    Yvec = data['Yvec']


    return X, Y, map_image, obstacleMap, xLM, yLM, Xvec, Yvec



def get_indices(x0, y0, X, Y, mapRes):

    # Compute indices
    j = int((x0 - X[0, 0] + mapRes) / mapRes) - 1   # column index
    i = int((Y[0, 0] - y0 + mapRes) / mapRes) - 1   # row index


    return i, j


def check_obstacles(map_indices, obstacleMap):
    '''
    Description: this function checks for the presence of obstacles in the provided indices.
    '''
    for i, j in map_indices:
        if obstacleMap[i, j] == 255:
            return True  # Obstacle found
    return False  # No obstacle


def plot_map(map_image, Xvec, Yvec):

    # Plotting the map of the environment in grayscale
    plt.imshow(map_image, cmap='gray', extent=(Xvec[0], Xvec[-1], Yvec[-1], Yvec[0]))
    plt.axis('on')
    plt.grid(True)
    plt.xlabel('X')
    plt.ylabel('Y')


def days2sec(days):
    
    return days * 24 * 60**2


def sec2days(sec):

    return sec / (24 * 60**2)


def Move2Pose(R, K=[1e-2, 2, -10]):
    '''
    Description: this function implements the Moving to a Pose control law.
    '''

    # Unpack State Variables
    rho = R[0]
    alpha = R[1]
    beta = R[2]

    # Define Gains
    Krho = K[0]
    Kalpha = K[1]
    Kbeta = K[2]

    # Compute Control
    v = Krho * rho
    omega = Kalpha * alpha + Kbeta * beta

    # Set Control Constraints
    v_max = 4e-2    # m/s - max speed
    
    if v > v_max:
        v = v_max

    # print(v, omega)
        
    return v, omega


def P2R(P, Pref):
    '''
    Description: this function converts the pose state variables [x, y, theta] to the polar state 
    variables [rho, alpha, beta] wrt a reference pose.
    '''

    if len(P.shape) == 1:
        
        if P.shape[0] != 3:
            raise Exception('Pose State dimensions are not correct!')
        
        x = P[0] - Pref[0]
        y = P[1] - Pref[1]
        theta = P[2]

        dx = -x
        dy = -y

        rho = np.sqrt(dx**2 + dy**2)
        alpha = np.arctan2(dy, dx) - theta
        beta = - alpha - theta + Pref[2]

        R = np.array([rho, alpha, beta])


    elif len(P.shape) == 2:
        
        [n, m] = P.shape

        if n != 3:
            raise Exception('Polar State dimensions are not correct!')
        
        R = np.zeros_like(P)

        for i in range(m):
            
            x = P[0, i] - Pref[0]
            y = P[1, i] - Pref[1]
            theta = P[2, i]

            dx = -x
            dy = -y

            rho = np.sqrt(dx**2 + dy**2)
            alpha = np.arctan2(dy, dx) - theta
            beta = - alpha - theta + Pref[2]

            R[:, i] = np.array([rho, alpha, beta])
    

    return R


def R2P(R, Pref):
    '''
    Description: this function converts the polar state variables [rho, alpha, beta] to the pose state variables [x, y, theta].
    '''

    if len(R.shape) == 1:
        
        if R.shape[0] != 3:
            raise Exception('Polar State dimensions are not correct!')
        
        rho = R[0]
        alpha = R[1]
        beta = R[2]

        theta = - alpha - beta + Pref[2]
        x = - rho * np.cos(alpha + theta) + Pref[0]
        y = - rho * np.sin(alpha + theta) + Pref[1]

        P = np.array([x, y, theta])
        


    elif len(R.shape) == 2:
        
        [n, m] = R.shape

        if n != 3:
            raise Exception('Polar State dimensions are not correct!')
        
        P = np.zeros_like(R)

        for i in range(m):
            
            rho = R[0, i]
            alpha = R[1, i]
            beta = R[2, i]

            theta = - alpha - beta + Pref[2]
            x = - rho * np.cos(alpha + theta) + Pref[0]
            y = - rho * np.sin(alpha + theta) + Pref[1]

            P[:, i] = np.array([x, y, theta])


    return P



def KinematicModel(t, S, K=[1e-2, 2, -10]):
    '''
    Description: S contains the polar state variables [rho, alpha, beta].
    '''

    # Unpack State Variables
    rho = S[0]
    alpha = S[1]
    beta = S[2]

    # Compute Control
    v, omega = Move2Pose(S, K)

    # Compute Derivatives
    drho = -np.cos(alpha) * v
    dalpha = np.sin(alpha) * v / rho - omega
    dbeta = - np.sin(alpha) * v / rho

    dS = np.array([drho, dalpha, dbeta])

    return dS