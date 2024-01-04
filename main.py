import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import library as lib

from rich.traceback import install
install(show_locals = True)


def main():

    X, Y, map_image, obstacleMap, xLM, yLM, Xvec, Yvec = lib.load_data()

    # Define Map Resolution
    mapRes = 10     # meters per pixel

    # Squeeze Xvec and Yvec -> both these variables must be one-dimensional vectors
    Xvec = np.squeeze(Xvec)
    Yvec = np.squeeze(Yvec)

    # Define Physical Values
    L = 3           # m - axles distance
    v_max = 4       # cm/s - max speed

    # Define Specific Poses
    P0 = np.array([42.38, 11.59, np.pi/2])
    P1 = np.array([33.07, 19.01, np.pi])

    plt.figure("Task 1")
    lib.plot_map(map_image, Xvec, Yvec)
    plt.plot(P0[0]*1e3, P0[1]*1e3, 'go', markersize=4)
    plt.plot(P1[0]*1e3, P1[1]*1e3, 'bo', markersize=4)
    plt.show()


    S0 = lib.pose2polar(P0)
    print(S0)

    

main()