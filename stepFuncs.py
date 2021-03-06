import arr
import staticVars as sv
from lkUtils import *

def gui(tour, lines, wndw):
    #draw vertices
    for coord in sv.guiCoords:
      index = sv.guiCoords.index(coord)
      name = sv.cityNames[index]
      wndw.create_oval((coord[0]-3, coord[1]-3, coord[0] + 3, coord[1] + 3), fill = "red")
      wndw.create_text(coord[0], coord[1] - 12, fill = "black", font = "Times 10 bold", text = name)

    #draw edges
    lines = addLines(tour, lines, 1, "black", wndw)
    
def findCandidates(vert, bFactor, node):
    #find candidates
    path = vert.array
    candidates = []
    nodeSublist = sv.wg[node]
    prevNode, nextNode = around(path, node)
    for i in range(len(nodeSublist)):
        if i != path[0] and i != node and i != prevNode and i != nextNode and not inSet(vert.removed, (node, i)): #checks if: recreating tour, self-directed, adjacent in path, already removed
            candidates += [[(node, i), nodeSublist[i]]]
    
    try: #candidates populated correctly
        candidates.sort(key = lambda c:c[1])
        candidates = candidates[:bFactor]
    except: #no candidates exist
        pass

    return candidates

def removeEdge(struct, edge):
    if edge == (431, 396) or edge == (396, 431):
        print("HERE")
    struct.array = removeUtil(struct.array, edge)
    if isinstance(struct, arr.Tour):
        removed = set()
        removed.add(edge)
        return arr.Vert(struct.array, set(), removed, sv.wg[edge[0]][edge[1]])

def addEdge(vert, candidate, reverse):
    edge = candidate[0]
    cost = candidate[1]
    if vert.gainSum - cost > 0:
        if reverse:
            vert.array.reverse()
        deltaPath = vert.array + [edge[1]]
        vert.array = deltaPath
        vert.gainSum -= sv.wg[edge[0]][edge[1]]
        vert.added.add(edge)
        return True
    else:
        return False #indicates that no candidate was feasible
    
def breakDelta(vert):
    triNode = vert.array[-1]
    x = vert.array[vert.array.index(triNode)+1]
    edge = (x, triNode)
    vert.array, edge = removeXW(vert.array, triNode, edge)
    vert.removed.add(edge)
    vert.gainSum += sv.wg[edge[0]][edge[1]]

def checkTour(vert):
    tour = vert.array + [vert.array[0]]
    edge = (tour[-2], tour[-1])
    tourCost = calculate(tour)
    return tour, tourCost

def deltaOps(vert, candidate, reverse):
    edgeAdded = addEdge(vert, candidate, reverse)
    if edgeAdded:
        breakDelta(vert)
        checkedTour, checkedCost = checkTour(vert)
        return checkedTour, checkedCost