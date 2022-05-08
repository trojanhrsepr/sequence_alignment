import basic_3 as basic
import efficient_3 as efficient
import time
import psutil
import os
import gc

# Gap Penalty constant
gap_penalty = 30

# String substitution dictionary
cost_dict = {"AC": 110, "AG": 48, "AT": 94, "CG": 118, "CT": 48, "GT": 110, "AA": 0, "CC": 0, "GG": 0, "TT": 0,
            "CA":110, "GA": 48, "TA": 94, "GC": 118, "TC": 48, "TG": 110}

# Memory utilization
def process_memory():                                
  process = psutil.Process(os.getpid())
  memory_info = process.memory_info()
  memory_consumed = int(memory_info.rss/1000)
  return memory_consumed

# Calculates time taken and memory utilization
def calculate_time_mem(start_time):
  mem = process_memory()                          
  end_time = time.time()
  time_taken = (end_time - start_time)*1000
  print("Time taken for algorithm: " + str(time_taken) + "ms")
  print("Memory usage by algorithm: " + str(mem) + "KB")
  return time_taken, mem

# Creates output file
def create_output_file(filename, start_time, cost, X, Y, time_taken, mem):
  with open(filename, 'w') as fp:       # to write to file
    fp.write(str(cost) +"\n")
    fp.write(X + "\n")
    fp.write(Y + "\n")
    fp.write(f"{time_taken}\n")
    fp.write(f"{mem}\n")

# Create plots for basic and efficient from datapoints
def plot_graphs():                                       

    # Run Basic Algorithm
    for i in range(1, 16):
        start_time = time.time()
        cost, X, Y = basic.basic_algo(f"datapoints/in{i}.txt", gap_penalty, cost_dict)
        print("Cost from input file datapoints/in"+ str(i) +".txt" + ":", cost)
        calculate_time_mem(start_time)
    print("End of calculation from Basic")

    # Run Efficient Algorithm
    for i in range(1, 16):
      start_time = time.time()
      cost, X, Y = efficient.space_efficient(f"datapoints/in{i}.txt")
      print("Cost from input file datapoints/in"+ str(i) +".txt" + ":", cost)
      calculate_time_mem(start_time)
    print("End of calculation from Efficient")

if __name__ == "__main__":
    plot_graphs()

