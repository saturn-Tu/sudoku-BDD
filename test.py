from pyeda.inter import *
import sys
import math
sys.setrecursionlimit(10000)

expr_bdd = ""
size = 0
r_size = 0

def outputExactOne(vars):
  # output at lest one is true
  global expr_bdd
  expr_bdd += "("
  for n in range(len(vars)):
    var = vars[n]
    expr_bdd += "v" + var
    if n < len(vars)-1:
      expr_bdd += "|"
  expr_bdd += ")&"
  # output at most one is true
  for n1 in range(len(vars)):
    for n2 in range(len(vars)):
      expr_bdd += "(-" + vars[n1] + "|-" + vars[n2] + ")"
    if n1 < len(vars)-1:
      expr_bdd += "&"

def constructCnf():
  for n in range(size):
    var_offset = n*size*size
    # handle row constraint
    for row in range(size):
      row_mems = []
      for m in range(size):
        row_mems.append(row*size+m + var_offset+1)
      outputExactOne(row_mems)
    # handle column constraint
    

sudoku = []
file = open("sudoku_4x4_9.txt")
line = file.readline()
while line:
  str1 = line.split()
  sudoku.append(str1)
  line = file.readline()
file.close()
size = len(sudoku)
r_size = int(math.sqrt(size))
print(size, r_size)
print(sudoku)
outputExactOne(sudoku[0])
print(expr_bdd)

'''f = expr("a&b|c")
f = expr2bdd(f)
print(f.satisfy_count())'''