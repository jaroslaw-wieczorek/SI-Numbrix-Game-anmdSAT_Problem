import math

import numpy
from bitstring import BitArray

from board.puzzle import Puzzle


class Encoding:

    def __init__(self, size):
        self.size = size
        self.n = size*size
        self.gb = int(math.ceil(math.log2(self.n)))

    def decode(self, puzzle, inputFile):
        with open(inputFile, "r") as f:
            content = f.readlines()[1:]
            satout = []
            if len(content) > 1:
                for line in content:
                    line = line[2:]
                    line = line.split()
                    for x in line:
                        satout.append(int(x))
                del satout[-1]

            else:
                content = content[0]
                content = content[2:-2]
                #content = [x.strip() for x in content]
                content = content.split()
                satout =[int(x) for x in content]
            values = []
            for i in range(1, self.n+1):
                ints = []
                ints = satout[0:self.n]
                satout = satout[self.n:]
                # ints <- first x literals from inputFile
                # remove the first x literals from inputFile
                # add the output of iConvert(ints) to values
                values.append(self.iconvert(ints))
            # use Puzzle as a template to typeset values into output file--
            answer = numpy.empty((self.size, 0)).tolist()
            count = 0
            it = iter(values)
            for row in answer:
                for x in range(0, self.size):
                    row.append(next(it))

                print(*row, sep=' ')
                #print("\n")




    def convert(self, ajdi, x):
        return [(ajdi -1)*self.n + x]

    def iconvert(self, ints):###############3
        for i in ints:
            if i > 0:
                return ((i - 1) % self.n) + 1

    def exists(self, id):###############3
        out = []
        for x in range(1, self.n+1):
            out.append(self.convert(id, x))
        return out

    def isunique(self, id):###############3
        CNF = []
        for x1 in range(1, self.n):
            for x2 in range(x1, self.n+1):
                #print(x1)
                #print(x2)
                #print("-----")
                CNF.append([[i * -1 for i in self.convert(id, x1)], [i * -1 for i in self.convert(id, x2)]])
        return CNF

    def arenotqual(self, id1, id2):###############3
        CNF = []
        for x in range(1, self.n+1):
            CNF.append([[i * -1 for i in self.convert(id1, x)], [i * -1 for i in self.convert(id2, x)]])
        return CNF

    def precedes(self, jd, ids): ###########
        CNF = []
        for x in range(1, self.n):
            clause = []
            clause.append([i * -1 for i in self.convert(jd, x)])
            for i in ids:
                clause.append(self.convert(i.ID, x + 1))
            CNF.append(clause)
        return CNF


    def isequal(self, ID, x): ##########
        return self.convert(ID, x)


    def encode(self, puzzle, outputfile): ###########
        CNF = []
        for b in puzzle.puzzle:
            for c in b:
                CNF.append(self.exists(c.ID))
        for b in puzzle.puzzle:
            for c in b:
                CNF.append(self.isunique(c.ID))
        for b in puzzle.puzzle:
            it = iter(b)
            for c in it:
                CNF.append(self.arenotqual(c.ID, next(it).ID))
        for b in puzzle.puzzle:
            for c in b:
                ids = puzzle.listNeighbourhood(c.ID)
                for clau in self.precedes(c.ID, ids):
                    CNF.append(clau)
        for b in puzzle.puzzle:
            for c in b:
                if c.value != 0:
                    CNF.append(self.isequal(c.ID, c.value))
        with open(outputfile, 'w') as file:
            file.write("p cnf ")
            file.write(str(self.n*self.n))
            file.write(" ")
            file.write(str(len(CNF)))
            file.write("\n")
            for clauso in CNF:
                clauso = str(clauso).replace("[","")
                clauso = str(clauso).replace("]","")
                clauso = str(clauso).replace(",","")
                print(clauso)
                file.write(clauso)
                file.write(" 0")
                file.write("\n")