from tkinter import *
import staticVars as sv
from euclidean import *
from lkUtils import *

""" GRAPHICS """
def gui(tour, lines):
    #draw vertices
    for coord in sv.guiCoords:
      index = sv.guiCoords.index(coord)
      name = sv.cityNames[index]
      sv.wndw.create_oval((coord[0]-3, coord[1]-3, coord[0] + 3, coord[1] + 3), fill = "red")
      sv.wndw.create_text(coord[0], coord[1] - 12, fill = "black", font = "Times 10 bold", text = name)

    #draw edges
    last = sv.guiCoords[tour[len(tour)-1]]
    for i in range(len(tour)-1):
      node = tour[i]
      nxt = tour[i+1]
      a = sv.wndw.create_line(sv.guiCoords[node][0], sv.guiCoords[node][1], sv.guiCoords[nxt][0], sv.guiCoords[nxt][1], fill = "black")
      lines.update({(node, nxt): a})
    a = sv.wndw.create_line(sv.guiCoords[tour[0]][0], sv.guiCoords[tour[0]][1], last[0], last[1], fill = "black")


""" STEPS TWO AND SEVEN"""
#find 5 longest edges in a tour not already added in
def longEdges(tour, added):
    flat_wg = []
    longest = []
    for i in range(len(sv.wg)):
        for j in range(len(sv.wg[i])):
            edge = (i, j)
            cost = sv.wg[i][j]
            flat_wg += [[edge, cost]]
    flat_wg.sort(key = lambda c:c[1], reverse = True)
    for [edge, cost] in flat_wg:
        if inTour(tour, edge) and edge not in added and len(longest) < 5:
            longest += [edge]
    return longest
    
def removeEdge(tour, edge, removed, lines, gainSum):
    #highlight node
    node = edge[0]
    nodeX = sv.guiCoords[node][0]
    nodeY = sv.guiCoords[node][1]
    sv.wndw.create_oval((nodeX-3, nodeY-3, nodeX + 3, nodeY + 3), fill = "blue")

    #pick an edge connecting the node to remove
    print("-Pick an edge and remove it")
    path = []
    path = removeFromTour(tour, edge)
    gainSum += sv.wg[edge[0]][edge[1]]
    removed.add(edge)
    sv.wndw.delete(lines[edge])
    del lines[edge]
    print("--Removing {} produces path: {}".format(edge, stringify(path)))
    print("--Removed set contains: {}".format(removed))

    #calculate the gain-sum
    print("-Calculate the gain-sum")
    print("--Gain-sum = {}\n".format(gainSum))

    return path, node, removed, gainSum


""" STEPS THREE AND EIGHT"""
def findCandidates(path, node, removed):
    #order 5 neighbors of the node by shortest to greatest distance
    print("-Order 5 neighbors of the node by shortest to greatest distance")
    candidates = []
    nodeSublist = sv.wg[node]
    prevNode, nextNode = around(path, node)
    for i in range(len(nodeSublist)):
        if i != node and i != prevNode and i != nextNode and (node, i) not in removed: #checks if: self-directed, adjacent in path, already removed
            candidates += [[(node, i), nodeSublist[i]]]
    
    candidates.sort(key = lambda c:c[1])
    candidates = candidates[:5]
    print("--Candidates: {}".format(stringify(candidates)))

    return candidates

def addEdge(path, node, added, lines, gainSum, candidates):
    #check candidates against gain-sum and pick first edge that keeps it positive
    print("-Check 5 candidates against gain-sum and pick first edge that keeps it positive")
    edge = None
    for [candidateEdge, candidateCost] in candidates:
        if gainSum - candidateCost > 0:
            edge = candidateEdge
            break
    print("--Chosen edge: {}".format(edge))

    #add chosen edge
    print("-Add first edge to improve gain-sum")
    try:
        deltaPath = path + [edge[1]]
        gainSum -= sv.wg[edge[0]][edge[1]]
        added.add(edge)
        a = sv.wndw.create_line(sv.guiCoords[edge[0]][0], sv.guiCoords[edge[0]][1], sv.guiCoords[edge[1]][0], sv.guiCoords[edge[1]][1], fill = "black")
        lines.update({edge: a})
        print("--Adding {} produces delta path: {}".format(edge, stringify(deltaPath)))
        print("--Added set contains: {}".format(added))
    except:
        print("\n!!! NO FEASIBLE CANDIDATES. HALT SCAN. !!!")
        return None


""" STEPS FOUR AND NINE """
def formDelta():
    #this is a place-holder. Delta path formed by step 3
    print("-This is a place-holder. Delta path formed by steps 2+3, or 7+8\n")


""" STEPS FIVE AND TEN """
def generateTour():
    #remove edge xw of the cycle incident with w that was not just added
    print("-Remove edge xw of the cycle incident with w that was not just added")
    print("--Stub")


    #join the two hanging ends of the path to form a tour
    print("-Join the two hanging ends of the path to form a tour")
    print("--Stub")


    #update GUI to reflect tour
    print("-Update GUI")
    print("--Stub")


    #restore GUI to continue scan
    print("-Restore GUI")
    print("--Stub\n")


""" STEPS SIX AND TEN"""
def compareTour():
    #compare tour with best seen so far
    print("-Compare tour with the best seen so far. Replace as necessary")
    print("--Stub\n")
