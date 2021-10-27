import sys
import numpy as np
import pdb


def select_random_path(E):
    # pentru linia 0 alegem primul pixel in mod aleator
    line = 0
    col = np.random.randint(low=0, high=E.shape[1], size=1)[0]
    path = [(line, col)]
    for i in range(E.shape[0]):
        # alege urmatorul pixel pe baza vecinilor
        line = i
        # coloana depinde de coloana pixelului anterior
        if path[-1][1] == 0:  # pixelul este localizat la marginea din stanga
            opt = np.random.randint(low=0, high=2, size=1)[0]
        elif path[-1][1] == E.shape[1] - 1:  # pixelul este la marginea din dreapta
            opt = np.random.randint(low=-1, high=1, size=1)[0]
        else:
            opt = np.random.randint(low=-1, high=2, size=1)[0]
        col = path[-1][1] + opt
        path.append((line, col))

    return path

def select_dynamic_programming_path(E):
    cost = np.zeros(E.shape)

    cost[0, :] = E[0, :]

    for i in range(1, E.shape[0]):
        for j in range(E.shape[1]):
            cost[i][j] = cost[i - 1][j]
            if j > 0:
                cost[i][j] = min(cost[i][j], cost[i - 1][j - 1])
            if j < E.shape[1] - 1:
                cost[i][j] = min(cost[i][j], cost[i - 1][j + 1])
            cost[i][j] += E[i][j]

    c_act, l_act = np.argmin(cost[-1, :]), E.shape[0] - 1

    path = [(l_act, c_act)]

    while l_act > 0:
        c_new = c_act
        if c_act > 0 and cost[l_act - 1][c_act - 1] < cost[l_act - 1][c_new]:
            c_new = c_act - 1
        if c_act < E.shape[1] - 1 and cost[l_act - 1][c_act + 1] < cost[l_act - 1][c_new]:
            c_new = c_act + 1
        
        l_act -= 1
        c_act = c_new

        path.append((l_act, c_act))

    path = path[::-1]

    return path


def select_path(E, method):
    if method == 'aleator':
        return select_random_path(E)
    elif method == 'programareDinamica':
        return select_dynamic_programming_path(E)
    else:
        print('The selected method %s is invalid.' % method)
        sys.exit(-1)