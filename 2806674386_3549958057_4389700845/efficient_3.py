import helper_3 as helper
import sys
import time

def get_input(file_name):
  with open(file_name) as fp: # load file
    x = fp.read().split()                             # split input buffer into lines

  final_str = []                                      # stores the final strings
  base_str = list(x[0])                               # start with first string

  for i in x[1:] + ["end"]:                           # start from 2nd line in the file
    if i.isdigit():
      k = int(i)
      base_str = base_str[:k+1] + base_str + base_str[k+1:]
    else:
      final_str.append("".join(base_str))             # end will make sure that both strings are appended
      base_str = i

  X, Y = final_str                                    # modified final strings
  return X, Y

def calculate_cost(s1,s2):
  lenX = len(s1)+1
  lenY = len(s2)+1
  OPT = [0]*(lenY)
  for i in range(lenY):
    OPT[i] = i* helper.gap_penalty
  for i in range(1,lenX):
    temp = [0] * (lenY)
    temp[0] = i * helper.gap_penalty
    for j in range(1, lenY):
       key = "".join([s1[i - 1], s2[j - 1]])
       MIN_Value = min(OPT[j-1]+helper.cost_dict[key],OPT[j] + helper.gap_penalty, temp[j-1] + helper.gap_penalty)
       temp[j] = MIN_Value
    OPT = temp
  return OPT

def get_OPT_point(leftx,rightx,y):
  lenY = len(y)+1
  left = calculate_cost(leftx,y)
  #print("Cost_DP = ",left)
  rightx_rev = "".join(reversed(rightx))
  y_rev = "".join(reversed(y))
  right = calculate_cost(rightx_rev,y_rev)
  MIN = float('inf')
  MIN_INDEX = -1
  for i in range(lenY):
    if(left[i]+right[len(y)-i]<MIN):
      MIN = left[i]+right[len(y)-i]
      MIN_INDEX = i
  return MIN_INDEX

def DC(X,Y):
  if (len(X)==0):
    temp = ""
    for i in range(len(Y)):
      temp+="_"
    l = []
    l.append(temp)
    l.append(Y)
    return l
  
  if(len(Y)==0):
    temp = ""
    for i in range(len(X)):
      temp+="_"
    l = []
    l.append(temp)
    l.append(X)
    return X,temp
  if (len(X)==1):
    MIN = -1
    MIN_Value = (len(Y)+1) * helper.gap_penalty
    for i in range(len(Y)):
      key = "".join([X[0], Y[i]])
      cost = helper.cost_dict[key]
      total_cost = cost + (len(Y)-1) * helper.gap_penalty
      if(total_cost<MIN_Value):
        MIN_Value=total_cost
        MIN = i
    if(MIN==-1):
      a1 = X
      for i in range(len(Y)):
        a1+= "_"
      l = []
      l.append(a1)
      Y1 = "_"+Y
      l.append(Y1)
      return l
    a1 = ""

    for i in range(MIN):
      a1+="_"
    a1+=X
    for i in range(MIN+1,len(Y)):
      a1+="_"
    l = []
    l.append(a1)
    l.append(Y)
    return l
  
  leftx = X[0:len(X)//2]
  rightx = X[len(X)//2:]
  y = Y
  #print("xl =",leftx)
  #print("xr=",rightx)
  #print("y=",y)
  optpoint = get_OPT_point(leftx,rightx,y)
  #print("opt=",optpoint)
  ans1 = DC(leftx,y[0:optpoint])
  ans2 = DC(rightx,y[optpoint:])
  result_string1 = ans1[0]+ans2[0]
  result_string2 = ans1[1]+ans2[1]
  return result_string1, result_string2

def get_cost(str1,str2):
  cost = 0

  for i in range(len(str1)):
    c1 = str1[i]
    c2 = str2[i]

    if(c1=='_' or c2=='_'):
      cost+=30
    else:
      key = "".join([c1, c2])
      cost+=helper.cost_dict[key]

  return cost

def space_efficient(filename):

  X,Y = get_input(filename)
  str1,str2 = DC(X,Y)
  cost = get_cost(str1,str2)
  return cost, str1, str2

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 <filename.py> <input.txt>")
        sys.exit()

    l = []
    start_time = time.time()
    cost, X, Y = space_efficient(sys.argv[1])
    print("Cost from input file" + sys.argv[1] + ":", cost)

    # Code for output file
    time_taken, mem = helper.calculate_time_mem(start_time)
    helper.create_output_file(sys.argv[2], start_time, cost, X, Y, time_taken, mem)
