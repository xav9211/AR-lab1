__author__ = 'xa92'
import copy
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
import numpy as np

def initialize(up, left, bottom, right, mid, size):
    result = [[mid]*size for _ in range(size)]
    if up != mid:
        for i in range(size):
            result[0][i] = up

    if left != mid:
        for i in range(size):
            result[i][0] = left

    if bottom != mid:
        for i in range(size):
            result[size-1][i] = bottom

    if right != mid:
        for i in range(size):
            result[i][size-1] = right

    return result

def show(plate, size):
    for i in range(1, size - 1):
        row = ""
        for j in range(1, size - 1):
            row += str(plate[i][j]) + "  "
        print row + "\n"

def visualize(plate, size):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    result = []
    py = []
    for i in range(1, size - 1):
        result.extend(plate[i][1:size - 1])
        py.extend([i]*(size-2))

    x = np.array(range(1, size - 1)*(size-2))
    y = np.array(py)
    z = np.array(result)

    xi = np.linspace(min(x), max(x))
    yi = np.linspace(min(y), max(y))

    X, Y = np.meshgrid(xi, yi)
    Z = griddata(x, y, z, xi, yi)
    # print(X)

    surf = ax.plot_surface(Y, X, Z, rstride=5, cstride=5, cmap=cm.jet,
                       linewidth=1, antialiased=True)

    ax.set_zlim3d(np.min(z), np.max(z))
    fig.colorbar(surf)

    plt.show()

def compute(plate, size, err):
    while True:
        prev = copy.deepcopy(plate)
        for i in range(1, size - 1):
            for j in range(1, size - 1):
                plate[i][j] = computePoint(prev[i-1][j], prev[i][j-1], prev[i+1][j], prev[i][j+1])
        if not checkErr(prev, plate, size, err):
            break

def computePoint(yp, xp, yn, xn):
    return (yp + xp + yn + xn)/4

def checkErr(prev, plate, size, err):
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            absDif = abs(prev[i][j] - plate[i][j])
            if absDif > err:
                return True
    return False


def main():
    size = 30
    plate = initialize(100, 100, 0, 0, 0, size)
    compute(plate, size, 1)
    show(plate, size)
    # visualize(plate, size)

main()