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


def plot_map(map_image, Xvec, Yvec):

    # Plotting the map of the environment in grayscale
    plt.imshow(map_image, cmap='gray', extent=(Xvec[0], Xvec[-1], Yvec[-1], Yvec[0]))
    plt.axis('on')
    plt.grid(True)
    plt.xlabel('X')
    plt.ylabel('Y')


def kinematic_model(t, S):

    dS = np.zeros_like(S)

    return dS


def pose2polar(pose):
    
    x = pose[0]
    y = pose[1]
    theta = pose[2]

    dx = -x
    dy = -y

    rho = np.sqrt(dx**2 + dy**2)
    alpha = np.arctan2(dy, dx) - theta               # substitute with atan2
    beta = - theta - alpha

    polar = np.array([rho, alpha, beta])

    return polar