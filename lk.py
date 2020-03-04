import staticVars as sv
from stepFuncs import *

def lin(tour, cost):
    #tour: The tour resulting from Farthest Insertion. Stored as a list
    #cost: The summarized edge costs of tour
    
    """ STORE DYNAMIC VARIABLES """
    #store starting tour as variable for node/edge scan initiation
    orig = list(tour)

    #best tour
    best = list(tour) #prevents pointer issue

    #track old configurations
    oldConfigs = []

    #line IDs
    lines = {}

    #draw onto GUI  
    print("<<< INITIALIZE GUI >>>\n")
    gui(tour, lines)

    #edge sets
    added = set()
    removed = set()

    #working path or tour
    nodeArray = []

    #node of interest
    node = None

    #gain-sum
    gainSum = 0


    """ STEP TWO """
    def step2():
        nonlocal nodeArray, node, removed, lines, gainSum #declare nonlocal if overwriting variables in scope of lin()
        print("<<< STEP 2 >>>")

        #list the 5 longest edges in descending order
        print("-List the 5 longest edges in tour")
        longest = longEdges(tour, added)        
        print("--Longest: {}".format(stringify(longest)))

        #remove edges
        nodeArray, node, removed, lines, gainSum = removeEdge(tour, longest[0], removed, lines, gainSum)

        #update button
        button.configure(text = "Add Edge", command = step3)


    """ STEP THREE """
    def step3():
        nonlocal oldConfigs, nodeArray, added, lines, gainSum
        print("<<< STEP 3 >>>")
        #find 5 candidates
        candidates = findCandidates(nodeArray, node, removed) #needs parameter to specify where to add from

        #add a candidate edge
        oldConfigs, nodeArray, added, lines, gainSum, found = addEdge(nodeArray, node, added, lines, gainSum, candidates)

        #if found, acknowledge best tour
        if found:
            print("Best tour: {}".format(stringify(best)))
            button.configure(text = "Done", command = step10)
        else:
            button.configure(text = "Break Delta", command = step5a)


    """ STEP FIVEa """
    def step5a():
        nonlocal nodeArray, gainSum, lines, removed
        print("<<< STEP 5a >>>")
        nodeArray, gainSum, lines, removed = breakDelta(nodeArray, lines, gainSum, removed, True)

        #update button
        button.configure(text = "Visualize Tour", command = step5b)


    """ STEP FIVEb """
    def step5b():
        nonlocal nodeArray, lines, gainSum
        print("<<< STEP 5b >>>")
        nodeArray, lines, gainSum = generateTour(nodeArray, lines, gainSum)

        #update button
        button.configure(text = "Compare Tour", command = step6a)
    

    """ STEP SIXa """
    def step6a():
        nonlocal best
        print("<<< STEP 6a >>>")
        best = compareTour(nodeArray, best)
        print("--Best tour: {}\n".format(stringify(best)))
        #update button
        button.configure(text = "Restore Delta", command = step6b)

    """ STEP SIXb """
    def step6b():
        nonlocal nodeArray, lines, gainSum
        print("<<< STEP 6b >>>")
        nodeArray, lines, gainSum = restoreDelta(nodeArray, oldConfigs)

        #update button
        button.configure(text = "Break Delta", command = step7)


    """ STEP SEVEN """
    def step7():
        nonlocal nodeArray, gainSum, lines, removed
        print("<<< STEP 7 >>>")
        nodeArray, gainSum, lines, removed = breakDelta(nodeArray, lines, gainSum, removed, False)

        #update button
        button.configure(text = "Add Edge", command = step8)


    """ STEP EIGHT """
    def step8():
        nonlocal oldConfigs, nodeArray, added, lines, gainSum
        print("<<< STEP 8 >>>")
        #specify last node
        node = nodeArray[-1]
        
        #find 5 candidates
        candidates = findCandidates(nodeArray, node, removed) #needs parameter to specify where to add from

        #add a candidate edge
        oldConfigs, nodeArray, added, lines, gainSum, found = addEdge(nodeArray, node, added, lines, gainSum, candidates)
        
        #if found, acknowledge best tour
        if found:
            print("Best tour: {}".format(stringify(best)))
            button.configure(text = "Done", command = step10)
        else:
            button.configure(text = "Break Delta", command = step5a)


    """ STEP TEN """
    def step10():
        nonlocal nodeArray, added, removed
        print("<<< STEP 10 >>>")
        
        #prepare for next node/edge scan
        nodeArray, added, removed = prepareScan(orig, nodeArray, best, lines)

    
    """ FINALIZE """
    #run GUI on loop
    button = Button(sv.root, text = "Remove Edge", command = step2, relief = RIDGE, bd = 4)
    button.pack(side = BOTTOM, pady = 15)
    sv.root.mainloop()
