import csv

file1 = open("result.txt", "rb")
file2 = open("result1.txt", "rb")
file3 = open("result2.txt", "rb")

speedup1 = open("speedup1.txt", "wb")
speedup2 = open("speedup2.txt", "wb")
speedup3 = open("speedup3.txt", "wb")

efficiency1 = open("efficiency1.txt", "wb")
efficiency2 = open("efficiency2.txt", "wb")
efficiency3 = open("efficiency3.txt", "wb")

sekw1 = 37329.000000
sekw2 = 278.000000
sekw3 = 3519.000000


def getse(sekw, file, speedup, efficiency):
    ls = ""
    le = ""
    for line in file:
        elems = line.split(' ')
        s = sekw / float(elems[1])
        e = s / int(elems[0])
        ls += elems[0] + ' ' + str(s) + '\n'
        le += elems[0] + ' ' + str(e) + '\n'

    speedup.write(ls)
    efficiency.write(le)

getse(sekw1, file1, speedup1, efficiency1)
getse(sekw2, file2, speedup2, efficiency2)
getse(sekw3, file3, speedup3, efficiency3)


file1.close()
file2.close()
file3.close()
speedup1.close()
speedup2.close()
speedup3.close()
efficiency1.close()
efficiency2.close()
efficiency3.close()