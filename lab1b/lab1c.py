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

def getPartPlate(rank, size, plate, plateSize):
    partSize = math.floor(plateSize / size)
    if rank == 0:
        partOfPlate = plate[:partSize + 2]
    else:
        first = partSize * rank
        last = partSize * rank + partSize + 2
        partOfPlate = plate[first:last]
    return partOfPlate

def f(x, y):
    return 0

def show(plate, size):
    matrix = ""
    for i in range(1, size):/home/xa92/subjects/IO
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
    worldSize = comm.Get_size()

    if rank == worldSize - 1:
        start = MPI.Wtime()
        loops = int(sys.argv[1])
        size = int(sys.argv[2])
        plate = initialize(1000.0, 0, 0, 0, 0, size)
        partSize = int(math.floor(size / worldSize))

        for i in xrange(worldSize - 1):
            tmpPlate = getPartPlate(i, worldSize, plate, size)
            comm.send(tmpPlate, dest=i)
            comm.send(loops, dest=i)
            comm.send(partSize, dest=i)

        first = partSize * (worldSize - 1)
        tmpPlate = plate[first:]

        print worldSize
        prev = worldSize-2
        for i in xrange(loops):
            if (worldSize - 1) % 2 == 1:
                row = comm.recv(source=prev)
                comm.send(tmpPlate[1], dest=prev)
            else:
                comm.send(tmpPlate[1], dest=prev)
                row = comm.recv(source=prev)

            tmpPlate[0] = row
            compute(tmpPlate, partSize)

        resultPlate = []
        for i in xrange(worldSize - 1):
            part = comm.recv(source=i)
            resultPlate.extend(part)
        resultPlate.extend(tmpPlate)
        end = MPI.Wtime()

        print showF(plate, size)

        # print end - start

    elif rank < worldSize - 1:
        last = worldSize-1
        part = comm.recv(source=last)
        loops = comm.recv(source=last)
        partSize = comm.recv(source=last)
        for i in xrange(loops):
            # start = MPI.Wtime()
            if rank == 0:
                comm.send(part[partSize-2], dest=1)
                part[partSize-1] = comm.recv(source=1)
            else:
                if (worldSize - 1) % 2 == 1:
                    rowE = comm.recv(source=rank+1)
                    rowS = comm.recv(source=rank-1)
                    comm.send(part[partSize-2], dest=rank+1)
                    comm.send(part[1], dest=rank-1)
                else:
                    comm.send(part[partSize-2], dest=rank+1)
                    comm.send(part[1], dest=rank-1)
                    rowE = comm.recv(source=rank+1)
                    rowS = comm.recv(source=rank-1)
                part[0] = rowS
                part[partSize-1] = rowE
            compute(part, partSize)
            # if i % 10 == 0:
            #     file1 = open("one/file1_" + str(i) + ".txt", "wb")
            #     file1.write(show(part1, data[0]))
            #     file1.close()

        comm.send(part, dest=worldSize-1)

    else:
       print "Expected only 4 nodes"

main()