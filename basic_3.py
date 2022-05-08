import helper_3 as helper
import sys
import time

def basic_algo(filename, gap_penalty, cost_dict):
    with open(filename) as fp:                                  # load file
        x = fp.read().split()                                   # split input buffer into lines

    final_str = []                                              # stores the final strings
    base_str = list(x[0])                                       # start with first string

    for i in x[1:] + ["end"]:                                   # start from 2nd line in the file

        if i.isdigit():
            k = int(i)
            base_str = base_str[:k+1] + base_str + base_str[k+1:]
        else:
            final_str.append("".join(base_str))                 # end will make sure that both strings are appended
            base_str = i

    X, Y = final_str                                            # modified final strings

    lenX = len(X) + 1
    lenY = len(Y) + 1

    # optimal value
    OPT = [[0] * lenY for _ in range(lenX)]                     # OPT matrix

    for i in range(1, lenX):                                    # col init
        OPT[i][0] = i * gap_penalty

    for j in range(1, lenY):                                    # row init
        OPT[0][j] = j * gap_penalty

    for i in range(1, lenX):
        for j in range(1, lenY):
            key = "".join([X[i - 1], Y[j - 1]])
            OPT[i][j] = min(cost_dict[key] + OPT[i - 1][j - 1], gap_penalty + OPT[i - 1][j], gap_penalty + OPT[i][j - 1])

    # optimal solution
    i = lenX - 1
    j = lenY - 1

    X_new = list(X)                                             # list of original X
    Y_new = list(Y)                                             # list of original Y

    while i > 0 and j > 0:
        key = "".join(sorted([X[i - 1], Y[j - 1]]))
        if OPT[i][j] == cost_dict[key] + OPT[i - 1][j - 1]:     # no need for insertion
            i -= 1
            j -= 1

        elif OPT[i][j] == gap_penalty + OPT[i][j - 1]:
            X_new.insert(i, "_")                                # insert '_' in X since penalty is lower
            j -= 1
        else:
            Y_new.insert(j, "_")                                # insert '_' in Y since penalty is lower
            i -= 1


    # when either i or j is 0, append '_' at the start of opposite string
    while i > 0:
        Y_new.insert(0, "_")
        i -= 1

    while j > 0:
        X_new.insert(0, "_")
        j -= 1

    return OPT[lenX - 1][lenY - 1], "".join(X_new), "".join(Y_new)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 <filename.py> <input.txt>")
        sys.exit()

    start_time = time.time()
    cost, X, Y = basic_algo(sys.argv[1], helper.gap_penalty, helper.cost_dict)
    print("Cost from input file " + sys.argv[1] + ":", f"{cost}")

    # Code for output file
    time_taken, mem = helper.calculate_time_mem(start_time)
    helper.create_output_file(sys.argv[2], start_time, cost, X, Y, time_taken, mem)