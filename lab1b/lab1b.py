#!/usr/bin/env python
from mpi4py import MPI
import sys
import copy
import math

temp = 1000.0

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

def getPartPlate(sx, ex, sy, ey, plate):
    partOfPlate = []
    for i in range(sx, ex):
        partOfPlate.append(plate[i][sy:ey])
    return partOfPlate

def f(x, y):
    return 0

def show(plate, size):
    matrix = ""
    for i in range(1, size):
        row = ""
        for j in range(1, size):
            row += str(plate[i][j]) + "  "
        matrix += row + "\n"
    return matrix

def showF(plate, size):
    matrix = ""
    for i in range(0, size+1):
        row = ""
        for j in range(0, size+1):
            row += str(plate[i][j]) + "  "
        matrix += row + "\n"
    return matrix

def compute(plate, size):
    prev = copy.deepcopy(plate)
    for i in range(1, size):
        for j in range(1, size):
            plate[i][j] += computePoint(i, j, prev)

def computePoint(x, y, prev):
    dt = 0.05
    return ((prev[x-1][y] + prev[x][y-1] + prev[x+1][y] + prev[x][y+1] - 4*prev[x][y] + f(x,y)) * dt) / 4

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        start = MPI.Wtime()
        size = 1000
        plate = initialize(1000.0, 0, 0, 0, 0, size)
        args = []
        args.append(int(size/2))
        args.append(int(float(sys.argv[1])))

        plate1 = getPartPlate(0, int(math.floor(size/2)) + 1, 0, int(math.floor(size/2)) + 1, plate)
        comm.send(plate1, dest=1)
        comm.send(args, dest=1)

        plate2 = getPartPlate(0, int(math.floor(size/2)) + 1, int(math.floor(size/2)) - 1, size, plate)
        comm.send(plate2, dest=2)
        comm.send(args, dest=2)

        plate3 = getPartPlate(int(math.floor(size/2)) - 1, size, 0, int(math.floor(size/2)) + 1, plate)
        comm.send(plate3, dest=3)
        comm.send(args, dest=3)

        plate4 = getPartPlate(int(math.floor(size/2)) - 1, size, int(math.floor(size/2)) - 1, size, plate)
        # comm.send(plate4, dest=4)
        # comm.send(args, dest=4)

        for i in xrange(int(sys.argv[1])):
            start = MPI.Wtime()
            col = comm.recv(source=3, tag=2)
            comm.send([row2[1] for row2 in plate4], dest=3, tag=2)
            row = comm.recv(source=2, tag=1)
            comm.send(plate4[1], dest=2, tag=1)

            mid = MPI.Wtime()
            print "4: " + str(mid - start)

            plate4[0] = row
            for j in xrange(size/2 + 1):
                plate4[j][0] = col[j]
            # part4[1][1] = temp
            compute(plate4, size/2)
            print "4 (all): " + str(MPI.Wtime() - start) + " compute " + str(MPI.Wtime() - mid)
            # part4[1][1] = temp


        comm.recv(source=1)
        comm.recv(source=2)
        comm.recv(source=3)
        # comm.recv(source=4)
        end = MPI.Wtime()

        print end - start

    elif rank == 1:
        part1 = comm.recv(source=0)
        data = comm.recv(source=0)
        for i in xrange(data[1]):
            # start = MPI.Wtime()
            comm.send([row[data[0]-1] for row in part1], dest=2, tag=2)
            col = comm.recv(source=2, tag=2)
            comm.send(part1[data[0]-1], dest=3, tag=1)
            part1[data[0]] = comm.recv(source=3, tag=1)
            # print "1: " + str(MPI.Wtime() - start)
            for j in xrange(data[0] + 1):
                part1[j][data[0]] = col[j]
            # part1[data[0]-1][data[0]-1] = temp
            compute(part1, data[0])
            # part1[data[0]-1][data[0]-1] = temp
            # if i % 10 == 0:
            #     file1 = open("one/file1_" + str(i) + ".txt", "wb")
            #     file1.write(show(part1, data[0]))
            #     file1.close()

        comm.send("end", dest=0)


    elif rank == 2:
        part2 = comm.recv(source=0)
        data = comm.recv(source=0)
        for i in xrange(data[1]):
            # start = MPI.Wtime()
            col = comm.recv(source=1, tag=2)
            comm.send([row[1] for row in part2], dest=1, tag=2)
            comm.send(part2[data[0]-1], dest=0, tag=1)
            part2[data[0]] = comm.recv(source=0, tag=1)
            # print "2: " + str(MPI.Wtime() - start)
            for j in xrange(data[0] + 1):
                part2[j][0] = col[j]
            # part2[data[0]-1][1] = temp
            compute(part2, data[0])
            # part2[data[0]-1][1] = temp
            # if i % 10 == 0:
            #     file2 = open("two/file2_" + str(i) + ".txt", "wb")
            #     file2.write(show(part2, data[0]))
            #     file2.close()

        comm.send("end", dest=0)

    elif rank == 3:
        part3 = comm.recv(source=0)
        data = comm.recv(source=0)
        for i in xrange(data[1]):
            # start = MPI.Wtime()
            comm.send([row2[data[0]-1] for row2 in part3], dest=0, tag=2)
            col = comm.recv(source=0, tag=2)
            row = comm.recv(source=1, tag=1)
            comm.send(part3[1], dest=1, tag=1)
            # print "3: " + str(MPI.Wtime() - start)
            part3[0] = row
            for j in xrange(data[0] + 1):
                part3[j][data[0]] = col[j]
            # part3[1][data[0]-1] = temp
            compute(part3, data[0])
            # part3[1][data[0]-1] = temp
            # if i % 10 == 0:
            #     file3 = open("three/file3_" + str(i) + ".txt", "wb")
            #     file3.write(show(part3, data[0]))
            #     file3.close()

        comm.send("end", dest=0)

    else:
       print "Expected only 4 nodes"

main()