import math
import sys
from pprint import pprint #for debugging

#ct = 0
##################################define Node class#################################
class Node(object): #derived from object
    def __init__(self,x,y):
        self.pos = (x,y)
        self.hStar = abs(x-self.goal[0]) + abs(y-self.goal[1])
        """
        #for debugging
        print("hohohohohohoh")
        print(self.pos)
        print(self.goal)
        print(self.hStar)
        """
        self.fStar = 0 #f*()
        self.parentNode = None
    def checkGoal(self):
        if(self.goal == self.pos):
            return True
        else:
            return False

#####################################define NodeList class##############################
class NodeList(list): #derived from list
    def find(self, x,y):
        tempList = []
        for tempNode in self:
            if tempNode.pos==(x,y):
                tempList = [tempNode]
        if(tempList != []):
            return tempList[0]
        else:
            return None
    def remove(self,node):
        del self[self.index(node)]
###########################################################################################
#get arguments and its length from command line
argList = sys.argv
numOfArgs = len(argList)

#check args num
if(numOfArgs != 6):
    print("Invalid arguments!")
    sys.exit()

f = open(argList[1])
line = f.readline()
count = 0
#define map as a string array
mapData = [];
while line:
    if(count == 0):
        tempLine = line.replace('\n', '')
        tempDim = line.split("\t")
        mapWidth = int(tempDim[0])
        mapHeight = int(tempDim[1])
    else:
        tempLine = line.replace('\n', '')
        tempLine = tempLine.replace('\t', '')
        mapData.append(tempLine)
    line = f.readline()
    count+=1
f.close
#pprint(mapData)

#set start pos and goal pos
Node.start = (int(argList[2]), int(argList[3]))
Node.goal = (int(argList[4]), int(argList[5]))
"""
#for debugging
print("start:")
print(Node.start)
print("goal")
print(Node.goal)
print(mapWidth)
print(mapHeight)
"""

#make open list and close list to store nodes
openList     = NodeList()
closeList    = NodeList()
startNode    = Node(Node.start[0], Node.start[1])
startNode.fStar = startNode.hStar
openList.append(startNode)
#print(openList)

#infinite loop
while(True):
    #if open list is empty, theree is no solution
    if(openList == []): #base case
        print("no route available")
        sys.exit()

    #find the node with minimum fStar and pass it to a new veriable n
    curNode = openList[0]
    tempFmin = curNode.fStar
    for everyNode in openList:
        if(everyNode.fStar < tempFmin):
            tempFmin = everyNode.fStar
            curNode = everyNode
    """
    #for debugging
    if(ct == 2):
        print("kokokookookok")
        print(n.fStar)
        sys.exit()
    ct += 1
    """
    openList.remove(curNode)
    closeList.append(curNode)

    #if the min node is goal then break
    if(curNode.checkGoal() == True): #base case
        endNode = curNode
        break

    gStar = curNode.fStar - curNode.hStar

    #check wich direction can the node move to
    for co in ((1,0),(-1,0),(0,1),(0,-1)):# right left up down
        x = curNode.pos[0] + co[0]
        y = curNode.pos[1] + co[1]

        #check after moving, if the node is within the map and not on a '1'
        if not(0 <= y < mapHeight and 0 <= x < mapWidth and mapData[y][x] != '1'):
            continue

        #check if the next node is in open or close list or it is a new node
        nextNode = openList.find(x,y)
        dist = abs(curNode.pos[0]-x) + abs(curNode.pos[1]-y)
        if(nextNode):
            #if the next node in open list and the fStar is smaller then update
            if(nextNode.fStar > gStar + nextNode.hStar + dist):
                nextNode.fStar = gStar + nextNode.hStar + dist
                nextNode.parentNode = curNode
        else:
            nextNode = closeList.find(x,y)
            if(nextNode):
                #if the next node in close list, and fStar is smaller, then update fStar, update parent, move to openList
                if(nextNode.fStar > gStar + nextNode.hStar + dist):
                    nextNode.fStar = gStar + nextNode.hStar + dist
                    nextNode.parentNode = curNode
                    openList.append(nextNode)
                    closeList.remove(nextNode)
            else:
                #this is a new node, put in open list
                nextNode = Node(x,y)
                nextNode.fStar = gStar + nextNode.hStar + dist
                nextNode.parentNode = curNode
                openList.append(nextNode)


#find the path by tracing from the endNode
curNode = endNode.parentNode
path = []
lastPos = curNode.pos
while True:
    if curNode.parentNode == None:
        break
    combined = [x - y for (x, y) in zip(curNode.pos, lastPos)]
    if(combined[0] == 1):
        path.insert(0, "LEFT")
    if(combined[0] == -1):
        path.insert(0, "RIGHT")
    if(combined[1] == 1):
        path.insert(0, "UP")
    if(combined[1] == -1):
        path.insert(0, "DOWN")
    lastPos = curNode.pos
    curNode = curNode.parentNode

result = ' '.join(path)
print(result)
