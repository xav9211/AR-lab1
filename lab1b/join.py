__author__ = 'xa92'

import csv

iter = 200
size = 14

def show(plate):
    matrix = ""
    for i in range(0, size*2):
        row = ""
        for j in range(0, size*2):
            row += str(plate[i][j]) + "  "
        matrix += row + "\n"
    return matrix

for i in xrange(iter):
    file1 = open("one/file1_" + str(i*10) + ".txt", "rb")
    file2 = open("two/file2_" + str(i*10) + ".txt", "rb")
    file3 = open("three/file3_" + str(i*10) + ".txt", "rb")
    file4 = open("four/file4_" + str(i*10) + ".txt", "rb")

    file = open("result/file_" + str(i*10) + ".txt", "wb")


    l1 = [map(float, line[:-2].split('  ')) for line in file1]
    l2 = [map(float, line[:-2].split('  ')) for line in file2]
    l3 = [map(float, line[:-2].split('  ')) for line in file3]
    l4 = [map(float, line[:-2].split('  ')) for line in file4]

    l = []
    l.append([1000.0]*28)
    for j in xrange(size):
        l.append([])
        l[j].extend(l1[j])
        l[j].extend(l2[j])

    for j in xrange(size):
        l.append([])
        l[j+size].extend(l3[j])
        l[j+size].extend(l4[j])

    file.write(show(l))

    file1.close()
    file2.close()
    file3.close()
    file4.close()
    file.close()