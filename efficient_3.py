#from resource import *
import time
import psutil
import os
import gc

def get_input(file_name):
  with open(file_name) as fp: # load file
    x = fp.read().split()                           # split input buffer into lines

  final_str = []                                      # stores the final strings
  base_str = list(x[0])                               # start with first string

  for i in x[1:] + ["end"]:                           # start from 2nd line in the file
    if i.isdigit():
      k = int(i)
      base_str = base_str[:k+1] + base_str + base_str[k+1:]
    else:
      final_str.append("".join(base_str))         # end will make sure that both strings are appended
      base_str = i

  X, Y = final_str                                    # modified final strings
  return X, Y

def Cost(s1,s2):
  lenX = len(s1)+1
  lenY = len(s2)+1
  OPT = [0]*(lenY)
  for i in range(lenY):
    OPT[i] = i*gap_penalty
  for i in range(1,lenX):
    temp = [0] * (lenY)
    temp[0] = i * gap_penalty
    for j in range(1, lenY):
       key = "".join([s1[i - 1], s2[j - 1]])
       MIN_Value = min(OPT[j-1]+cost_dict[key],OPT[j]+gap_penalty,temp[j-1]+gap_penalty)
       temp[j] = MIN_Value
    OPT = temp
  return OPT

def getOPTpoint(leftx,rightx,y):
  lenY = len(y)+1
  left = Cost(leftx,y)
  #print("Cost_DP = ",left)
  rightx_rev = "".join(reversed(rightx))
  y_rev = "".join(reversed(y))
  right = Cost(rightx_rev,y_rev)
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
    MIN_Value = (len(Y)+1)*gap_penalty
    for i in range(len(Y)):
      key = "".join([X[0], Y[i]])
      cost = cost_dict[key]
      total_cost = cost + (len(Y)-1)*gap_penalty
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
  optpoint = getOPTpoint(leftx,rightx,y)
  #print("opt=",optpoint)
  ans1 = DC(leftx,y[0:optpoint])
  ans2 = DC(rightx,y[optpoint:])
  result_string1 = ans1[0]+ans2[0]
  result_string2 = ans1[1]+ans2[1]
  return result_string1, result_string2

def get_Cost(str1,str2):
  cost = 0

  for i in range(len(str1)):
    c1 = str1[i]
    c2 = str2[i]

    if(c1=='_' or c2=='_'):
      cost+=30
    else:
      key = "".join([c1, c2])
      cost+=cost_dict[key]

  return cost


def space_efficient(filename):

  X,Y = get_input(filename)
  str1,str2 = DC(X,Y)
  cost = get_Cost(str1,str2)
  return cost, str1, str2


def process_memory():                                  # memory calculation
  process = psutil.Process(os.getpid())
  memory_info = process.memory_info()
  memory_consumed = int(memory_info.rss/1024)
  return memory_consumed

if __name__ == "__main__":
    global gap_penalty
    gap_penalty = 30

    # string substitution dictionary
    global cost_dict
    cost_dict = {"AC": 110, "AG": 48, "AT": 94, "CG": 118, "CT": 48, "GT": 110, "AA": 0, "CC": 0, "GG": 0, "TT": 0,
                 "CA":110, "GA": 48, "TA": 94, "GC": 118, "TC": 48, "TG": 110}

    # for i in range(1, 6):
    #     leng, X, Y = space_efficient(f"SampleTestCases/input{i}.txt", gap_penalty, cost_dict)
    #     print(i)
    #     print("X=",X,"Y=",Y)
    #     with open(f"SampleTestCases/output{i}.txt", 'r') as fp:
    #         leng1, X1, Y1 = fp.read().split()[:3]
    #     print(f"length->{leng}", leng == int(leng1), X == X1, Y == Y1)

    l = []
    for i in range(1, 16):
      # start_time = time.time()
      leng, X, Y = space_efficient(f"datapoints/in{i}.txt")
      print(leng)
      # mem = process_memory()                              # memory calculation
      # end_time = time.time()
      # time_taken = (end_time - start_time)*1000
      # print(time_taken)
      # print(mem)

  # with open(f"datapoints/out{i}", 'w') as fp:     # to write to file
  #   fp.write(str(leng) +"\n")
  #   fp.write(X + "\n")
  #   fp.write(Y + "\n")
  #   fp.write(f"{mem}\n")
  #   fp.write(f"{time_taken}\n")


