import time, os
from reader import *
from euclidean import *

def solve(filepath):
    #clear the console
    clear = lambda: os.system('cls')
    clear()
    
    print("Pick a path generation algorithm (random by default):")
    print("""-farthest: Farthest Insertion
-nearest: Nearest Neighbor
-fixed: Fixed Tour defined in code\n""")
    algo = input()
    clear()

    print("Choose a solmax:\n")
    rawsol = input()
    solmax = int(rawsol)
    clear()

#     print("Pick to run in step mode, at pace, or fast as possible:")
#     print("""-step
# -slow
# -medium
# -fast
# -max"\n"")
    # option = input()
    # clear()
    option = "step"

    #import after accepting input or else GUI runs annoyingly
    from revision import lin
    import staticVars as sv
    from genAlgos.fi import farthestInsertion
    from genAlgos.nn import nearestNeighbor
    from lkUtils import calculate, stringify
    from genAlgos.rand import randomTour

    #form GUI and weighted graph
    sv.cityNames, sv.rawCoords, sv.guiCoords = reader(filepath, sv.height, sv.width)
    sv.wg = weightedGraph(sv.rawCoords)

    #create initial tour
    start = time.time()
    tour = None
    cost = None
    if algo == "farthest":
        tour, cost = farthestInsertion(sv.rawCoords, sv.guiCoords, sv.cityNames, sv.height, sv.width, "2", False)
    elif algo == "nearest":
        tour, cost = nearestNeighbor(sv.rawCoords, sv.guiCoords, sv.cityNames, sv.height, sv.width, "2", False)
    elif algo == "fixed":
        tour = [5,3,13,8,10,1,11,9,12,2,7,0,6,4,5] #14
        cost = calculate(tour)
    else:
        tour, cost = randomTour(sv.rawCoords, sv.cityNames, False)
    
    #print tour info
    end = time.time()
    runtime = end - start
    print("Initial Cost: {} units".format(round(cost)))
    print("Initial Tour: {}".format(stringify(tour)))
    print("Tour generation runtime: {} sec\n".format(round(runtime)))

    #run lin-kernighan
    print("<<< RUN LIN-KERNIGHAN (SOLMAX = {})>>>".format(solmax))
    lin(tour, cost, solmax, runtime, option)