#!/usr/bin/env python
import copy
# import pygmyplot as pyg
# import Tkinter as TK
import time
import sys

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

def f(x, y):
    return 0

def show(plate, size):
    for i in range(1, size - 1):
        row = ""
        for j in range(1, size - 1):
            row += str(plate[i][j]) + "  "
        print row + "\n"

# def visualize(plate, size):
#
#     result = []
#     py = []
#
#     for i in range(1, size - 1):
#         result.extend(plate[i][1:size - 1])
#         for j in range(1, size - 1):
#             py.append((i, j))
#
#     tk = TK.Tk()
#     hm = pyg.xy_heat(py, result, master=tk)
#     TK.Button(tk, text="Quit", command=tk.destroy).pack()
#     tk.mainloop()

def compute(plate, size, iter):
    for i in xrange(iter):
        start = time.time()
        prev = copy.deepcopy(plate)
        for i in range(1, size - 1):
            for j in range(1, size - 1):
                plate[i][j] += computePoint(i, j, prev)
        print time.time() - start

def computePoint(x, y, prev):
    dt = 0.05
    return ((prev[x-1][y] + prev[x][y-1] + prev[x+1][y] + prev[x][y+1] - 4*prev[x][y] + f(x,y)) * dt) / 4

def main():
    start = time.time()
    size = 1000
    plate = initialize(100.0, 0, 0, 0, 0, size)
    compute(plate, size, int(sys.argv[1]))
    end = time.time()
    print end - start
    # show(plate, size)
    # visualize(plate, size)

main()