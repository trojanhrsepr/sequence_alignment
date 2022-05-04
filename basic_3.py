def basic_algo(var, gap_penalty, cost_dict):
    with open(f"SampleTestCases/input{var}.txt") as fp: # load file
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

    lenX = len(X) + 1
    lenY = len(Y) + 1

    # optimal value
    OPT = [[0] * lenY for _ in range(lenX)]             # OPT matrix

    for i in range(1, lenX):                            # col init
        OPT[i][0] = i * gap_penalty

    for j in range(1, lenY):                            # row init
        OPT[0][j] = j * gap_penalty

    for i in range(1, lenX):
        for j in range(1, lenY):
            key = "".join([X[i - 1], Y[j - 1]])
            OPT[i][j] = min(cost_dict[key] + OPT[i - 1][j - 1], gap_penalty + OPT[i - 1][j], gap_penalty + OPT[i][j - 1])

    # optimal solution
    i = lenX - 1
    j = lenY - 1

    X_new = list(X)                                     # list of original X
    Y_new = list(Y)                                     # list of original Y

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
    gap_penalty = 30

    # string substitution dictionary
    cost_dict = {"AC": 110, "AG": 48, "AT": 94, "CG": 118, "CT": 48, "GT": 110, "AA": 0, "CC": 0, "GG": 0, "TT": 0,
                 "CA":110, "GA": 48, "TA": 94, "GC": 118, "TC": 48, "TG": 110}

    for i in range(1, 6):
        leng, X, Y = basic_algo(i, gap_penalty, cost_dict)
        print(i)
        with open(f"SampleTestCases/output{i}.txt", 'r') as fp:
            leng1, X1, Y1 = fp.read().split()[:3]
        print(f"length->{leng}", leng == int(leng1), X == X1, Y == Y1)