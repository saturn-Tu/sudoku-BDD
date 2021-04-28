from pyeda.inter import *
import sys
import math
sys.setrecursionlimit(100000000)

expr_bdd = ""
rows_list = []
cols_list = []
blocks_list = []
size = 0
r_size = 0

def initialLists():
  global rows_list
  global cols_list
  global blocks_list
  global size
  global r_size
  # initial three list as number of size of zero
  for n in range(size):
    rows_list.append([0]*size)
    cols_list.append([0]*size)
  for r in range(r_size):
    blocks_list.append([])
    for c in range(r_size):
      blocks_list[r].append([0]*size)
  for r in range(size):
    for c in range(size):
      r_r = int(r/r_size)
      r_c = int(c/r_size)
      value = int(sudoku[r][c])-1
      if value >= 0:
        rows_list[r][value] = 1
        cols_list[c][value] = 1
        blocks_list[r_r][r_c][value] = 1

def outputExactOne(vars):
  # output at lest one is true
  global expr_bdd
  if len(expr_bdd) > 0:
    expr_bdd += "&"
  expr_bdd += "("
  for n in range(len(vars)):
    var = "v"+str(vars[n])
    expr_bdd += var
    if n < len(vars)-1:
      expr_bdd += "|"
  expr_bdd += ")"
  if len(vars) > 1:
    expr_bdd += "&"
  # output at most one is true
  for n1 in range(len(vars)):
    for n2 in range(n1+1, len(vars)):
      var1 = "v"+str(vars[n1])
      var2 = "v"+str(vars[n2])
      expr_bdd += "(~" + var1+ "|~" + var2 + ")"
      if n1 < len(vars)-2 or n2 < len(vars)-1:
        expr_bdd += "&"

def constructCnf():
  for n in range(size):
    var_offset = n*size*size
    # handle row constraint
    for row in range(size):
      row_mems = []
      skip_flg = 0
      for col in range(size):
        # have pre-assigned a value, all row with same value can skip
        if rows_list[row][n] == 1:
          skip_flg = 1
          break
        # have pre-assigned a value, continue. then check three list constraint 
        if int(sudoku[row][col]) > 0 or cols_list[col][n] == 1 or blocks_list[int(row/r_size)][int(col/r_size)][n] == 1:
          continue
        row_mems.append(row*size+col + var_offset+1)
      # if find pre-assigned, skip adding constraint
      if skip_flg == 0 and len(row_mems) > 0:
        outputExactOne(row_mems)
    # handle column constraint
    for col in range(size):
      col_mems = []
      skip_flg = 0
      for row in range(size):
        # have pre-assigned a value, all row with same value can skip
        if cols_list[col][n] > 0:
          skip_flg = 1
          break
        # have pre-assigned a value, continue. then check three list constraint 
        if int(sudoku[row][col]) > 0 or rows_list[row][n] == 1 or blocks_list[int(row/r_size)][int(col/r_size)][n] == 1:
          continue
        col_mems.append(row*size+col + var_offset+1)
      # if find pre-assigned, skip adding constraint
      if skip_flg == 0 and len(col_mems) > 0:
        outputExactOne(col_mems)
    # handle block constraint
    for r_b in range(r_size):
      for c_b in range(r_size):
        block_mems = []
        skip_flg = 0
        var_idx = r_b*r_size*size+c_b*r_size + var_offset+1
        for count in range(size):
          # have pre-assigned a value, skip
          if blocks_list[r_b][c_b][n] > 0:
            skip_flg = 1
            break
          # have pre-assigned a value, skip
          pre_idx = var_idx
          if count%r_size == r_size-1:
            var_idx = var_idx + size-r_size+1
          else:
            var_idx = var_idx + 1
          # skip continue after updating var_idx
          row = r_b*r_size+int(count/r_size)
          col = c_b*r_size+(count%r_size)
          if int(sudoku[row][col]) > 0 or rows_list[row][n] == 1 or cols_list[col][n] == 1:
            continue
          block_mems.append(pre_idx)
        # if find pre-assigned, skip adding constraint
        if skip_flg == 0 and len(block_mems) > 0:
          outputExactOne(block_mems)
  # handle one space only place one number
  for r in range(size):
    for c in range(size):
      r_r = int(r/r_size)
      r_c = int(c/r_size)
      space_mems = []
      global expr_bdd
      if int(sudoku[r][c]) == 0:
        for n in range(size):
          var_offset = n*size*size
          var_idx = r*size+c + var_offset+1
          # fill in pre-define answer
          if rows_list[r][n] == 0 and cols_list[c][n] == 0 and blocks_list[r_r][r_c][n] == 0:
            space_mems.append(var_idx)
        if len(space_mems) > 0:
          outputExactOne(space_mems)

sudoku = []
# file = open("sudoku_4x4_9.txt")
# file = open("sudoku_9x9_125.txt")
file = open(sys.argv[1])
line = file.readline()
while line:
  str1 = line.split()
  sudoku.append(str1)
  line = file.readline()
file.close()
size = len(sudoku)
r_size = int(math.sqrt(size))
initialLists()
constructCnf()
print(expr_bdd)
f = expr(expr_bdd)
s_count = f.satisfy_count()
print(s_count)

o_file = open(sys.argv[2], "w")
o_file.write(str(s_count))
o_file.close()