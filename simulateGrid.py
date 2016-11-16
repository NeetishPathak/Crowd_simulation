import time
import sys
import math
import random
from graphics import *

testSetting = 1
gridsOn = 0
if testSetting == 1:
    settingspath = os.getcwd() + '/test1.txt'
    # settingspath = os.getcwd() + '/test1.txt'
    framepath = os.getcwd() + '/frame.txt'
    griDim = 25
    WIDTH = 1000
    HEIGHT = 600
    COORDS_X = 1000
    COORDS_Y = 600
else:
    settingspath = os.getcwd() + '/test2.txt'
    # settingspath = os.getcwd() + '/test1.txt'
    framepath = os.getcwd() + '/frame.txt'
    griDim = 5
    WIDTH = 400
    HEIGHT = 400
    COORDS_X = 40
    COORDS_Y = 40

class Grid:
    def __init__(self, width, height, nodeSize, nodeGap, window):
        self.opened = []
        self.closed = []
        self.width = width
        self.height = height
        self.nodeSize = nodeSize
        self.nodeGap = nodeGap
        self.window = window
        self.agent = []
        self.building = []
        self.triangle = []
        self.road = []
        self.obstacle = []
        self.polygon = []
        self.POI = []
        self.nodes = []
        self.start = ''
        self.end = ''
        self.blocks = []


    def draw(self):
        for i in range(self.width):
            row = []
            for j in range(self.height):
#                 x = (i*self.nodeSize)+((i+1)*self.nodeGap)
#                 y = (j*self.nodeSize)+((j+1)*self.nodeGap)
                
                x = i*griDim
                y = j*griDim
                # color start/end/obstacle blocks differently
                if (i+1, j+1) == self.start:
                    color = "red"
                elif (i+1, j+1) == self.end:
                    color = "green"
                elif (i+1, j+1) in self.blocks:
                    color = "black"
                else:
                    color = "#636363"

                node = Node(x, y, self.nodeSize, self.window, color, i, j)
                row.append(node)
                node.draw()

            self.nodes.append(row)
        # draw all the nodes at once
        self.window.flush()
        self.load_env()

    def load_env(self):
        settings = open(settingspath)
        settings.readline()
        while True:
            line = settings.readline()
            if line=="":
                break;
            line = line.split()
            x = float(line[1])
            y = float(line[2])
            if line[0]=="poi":
                num = line[3]
                self.POI.append([[x,y,num]])
            if line[0]=="agent":
                rad = float(line[3])
                self.agent.append([[x,y,rad]])
            if line[0]=="obstacle":
                rad = float(line[3])
                type = str(line[4])
                self.obstacle.append([[x,y,rad, type]])
            if line[0]=="building":
                l = float(line[3])
                b = float(line[4])
                self.building.append([[x,y,l,b,line[5]]])
            if line[0]=="triangle":
                p2 = float(line[3])
                p3 = float(line[4])
                p4 = float(line[5])
                p5 = float(line[6])
                self.triangle.append([[x,y,p2,p3,p4,p5,line[6]]])
            if line[0] =="polygon":
                p2 = float(line[3])
                p3 = float(line[4])
                p4 = float(line[5])
                p5 = float(line[6])
                p6 = float(line[7])
                p7 = float(line[8])
                self.polygon.append([[x,y,p2,p3,p4,p5,p6,p7,line[9]]])
            if line[0]=="road":
                l = float(line[3])
                b = float(line[4])
                h = float(line[5])
                self.road.append([[x,y,l,b,h]])
        settings.close()
        self.draw_graphics()

    def draw_graphics(self):
        print "graphics library"
        positions=[]

#         self.window.setCoords(0,0,480,480)
        for a in self.agent:
            x = a[0][0]
            y = a[0][1]
            z = a[0][2] - 0.1
            val = Circle( Point(x,y), z)
            val.setFill("red")
            positions.append([x,y])
            val.draw(self.window)
            a.append(val)
        
        for t in self.triangle:
            p1 = Point(t[0][0],t[0][1])
            p2 = Point(t[0][2],t[0][3])
            p3 = Point(t[0][4],t[0][5])
            poly = Polygon(p1,p2,p3)
            poly.setFill("#addd8e")
            poly.draw(self.window)
            t.append(poly)
        
        for p in self.polygon:
            p1 = Point(p[0][0],p[0][1])
            p2 = Point(p[0][2],p[0][3])
            p3 = Point(p[0][4],p[0][5])
            p4 = Point(p[0][6],p[0][7])
            cent_x = (p[0][0] + p[0][2] + p[0][4] + p[0][6])/4.0
            cent_y = (p[0][1] + p[0][3] + p[0][5] + p[0][7])/4.0
            poly = Polygon(p1,p2,p3,p4)
            poly.setFill("#bf78ce")
            poly.draw(self.window)
            if p[0][8] == "River":
                poly.setFill("#99d8c9")
            text = Text(Point(cent_x,cent_y),p[0][8])
            text.setSize(8)
            text.draw(self.window)
            p.append(poly)
        
        for a in self.building:
#             x = a[0][0] * 10 + a[0][0] * self.nodeGap
#             y = a[0][1] * 10 + a[0][1] * self.nodeGap
#             z = a[0][3] * 10 + a[0][3] * self.nodeGap
#             w = a[0][2] * 10 + a[0][2] * self.nodeGap
            
            p1 = int(a[0][0]/griDim) 
            p2 = int(a[0][1]/griDim) 
            
            self.blocks.append((p1,p2))
            l = a[0][3]
            h = a[0][2]
            print p1, p2
            print l, h
            itr1 = 0
            while(l>=griDim):
#                 self.blocks.append((p1+itr1,p2))
                itr2 = 0
                h = a[0][2]
                while(h>=griDim):
                    self.blocks.append((p1+itr1,p2+itr2))
#                     print "blocking ", p1+itr1,p2+itr2
#                     print "l,h ",l,h
                    itr2 += 1
                    h -=griDim
                itr1 += 1
                l -= griDim

            bd1 = Point(a[0][0], a[0][1])
#           bd2 = Point(a[0][0], a[0][1] + a[0][2])
            bd3 = Point(a[0][0] + a[0][3], a[0][1] + a[0][2])
            
#             bd1 = Point(x, y)
    #         bd2 = Point(a[0][0], a[0][1] + a[0][2])
#             bd3 = Point(x + z, y + w)
    #         bd4 = Point(a[0][0] + a[0][3], a[0][1])

            #Line(bd1,bd2).draw(window)
            #Line(bd2,bd3).draw(window)
            #Line(bd3,bd4).draw(window)
            #Line(bd4,bd1).draw(window)
            
            rect = Rectangle(bd1,bd3)
            if "College" == str(a[0][4]):
                color = 'Brown'
            elif 'Hospital' == str(a[0][4]):
                color = 'Blue'
            elif "Forest" == str(a[0][4]):
                color = "Green"
            elif "Pub" == str(a[0][4]):
                color = "Yellow"
            elif "Home" == str(a[0][4]):
                color = "White"
            elif "Office" == str(a[0][4]):
                color = "Magenta"
            elif "Gym" == str(a[0][4]):
                color = "Maroon"
            elif "Pool" == str(a[0][4]):
                color = "cyan"
            elif "Park" == str(a[0][4]):
                color = "Green"
            elif "Hostel" == str(a[0][4]):
                color = "Yellow"
            elif "Bridge" == str(a[0][4]):
                color = "Brown"
            elif "Mall" == str(a[0][4]):
                color = "#5ab4ac"
            elif "Restaurant" == str(a[0][4]):
                color = "#d8b365"
            else:
                color = "#addd8e"
            rect.setFill(color)
            rect.draw(self.window)
            anchorPoint = rect.getCenter()
            text = Text(anchorPoint, a[0][4])
            text.setSize(8)
            text.draw(self.window)
            a.append(rect)
    #     time.sleep(10)

        for r in self.road:
            r1= Point(r[0][0],r[0][1])
            r2 = Point(r[0][0] + r[0][3],r[0][1]+r[0][2])
            rd = Rectangle(r1,r2)
            rd.setFill("#636363")
            rd.setOutline("#636363")
            rd.draw(self.window)
            r.append(rd)

        for o in self.obstacle:
            val = Circle( Point(o[0][0],o[0][1]), o[0][2])
            type = o[0][3]
            if type == "road":
                val.setFill("#636363")
                val.setOutline("#636363")
            else:
                val.setFill("black")
            val.draw(self.window)
            o.append(val)
            
        for poi in self.POI:
#             x = poi[0][0] * 10 + poi[0][0] * self.nodeGap
#             y = poi[0][1] * 10 + poi[0][1] * self.nodeGap
            poi1 = Point(poi[0][0], poi[0][1])
            poi2 = Point(poi[0][0] + griDim, poi[0][1] + griDim)
#             poi1 = Point(x,y)
#             poi2 = Point(x + self.nodeSize, y + self.nodeSize)
            rct_poi = Rectangle(poi1,poi2)
            rct_poi.setFill("Red")
            rct_poi.draw(self.window)
            text = Text(rct_poi.getCenter(),poi[0][2])
            text.setSize(8)
            text.draw(self.window)
        print self.blocks   
        
        matrix = []
        for i in range(0,COORDS_X,griDim):
            m1 = []
            for j in range(0,COORDS_Y,griDim):
                x = i
                y = j
                m1.append((x*(COORDS_X/griDim) + y)/griDim)
                
                if gridsOn == 1:
                    rP = Rectangle(Point(x,y),Point(x + griDim,y + griDim))
                    rP.setOutline("white")
                    rP.draw(self.window)
                    t = Text(rP.getCenter(),(i*(COORDS_X/griDim) + j)/griDim)
                    t.setSize(8)
                    t.draw(self.window)
            matrix.append(m1)

    def AlternatePath(self,path):
        startNode = self.nodes[self.start[0]-1][self.start[1]-1]
        endNode = self.nodes[self.end[0]-1][self.end[1]-1]

        self.opened = []
        self.closed = []
        # add the start node to the opened list so the loop can start
        self.opened.append(startNode)

        # set the gScore of the start node to 0 because it is 0 units away from start
        startNode.setGScore(0)

        # fScore = gScore + hCost but gScore = 0 for first node therefore fScore = hCost = distance from start to end
        startNode.setFScore(self.getDistance(startNode, endNode))
        
        for cord in path:
            self.blocks.append((cord[0],cord[1]))

        #print self.blocks
            
        while self.opened:
            # current is an opened node with the lowest fScore
            current = self.opened[0]

            for node in self.opened:
                if node.fScore < current.fScore:
                    current = node

            if current == endNode:
                # found the path - display the path
                path1 = []
                node = endNode
                
                while node.getParent():
                    data = (node.getParent().row,node.getParent().column)
                    path1.append(data)
                    node = node.getParent()
                #path.pop()
                print path1
                self.reconstructPath(endNode)

                for cord in path:
                    self.blocks.remove((cord[0],cord[1]))
            
                return(True)

            self.opened.remove(current)
            self.closed.append(current)

            for neighbour in self.getNeighbours(current):
                if neighbour in self.closed:
                    continue    # ignore it because it has already been evaluated

                # the distance from start to a neighbour
                tempGScore = current.gScore + self.getDistance(current, neighbour)
                if neighbour not in self.opened:    # discover a new node
                    self.opened.append(neighbour)
                elif tempGScore >= neighbour.gScore:
                    continue    # this is not a better path

                # this path is the best path until now
                neighbour.setParent(current)
                neighbour.setGScore(tempGScore)
                neighbour.setFScore(tempGScore + self.getDistance(neighbour, endNode)) # fScore = gScore + hCost
            
        return False

    #Given a start and end point on the grid, this function calculates all the best paths between them.
    #All the neighbours of the node on the grid are examined and least cost path is selected.
    #Once a path is selected, all the nodes of that path are blocked and the function is called recursively
    #to find a another possible path. Once found, the nodes are unblocked again.
    def findPath(self,start,end,path):
        self.start = start
        self.end = end
        startNode = self.nodes[self.start[0]-1][self.start[1]-1]
        endNode = self.nodes[self.end[0]-1][self.end[1]-1]

        self.opened = []
        self.closed = []

        for cord in path:
            self.blocks.append((cord[0],cord[1]))

        # add the start node to the opened list so the loop can start
        self.opened.append(startNode)

        # set the gScore of the start node to 0 because it is 0 units away from start
        startNode.setGScore(0)

        # fScore = gScore + hCost but gScore = 0 for first node therefore fScore = hCost = distance from start to end
        startNode.setFScore(self.getDistance(startNode, endNode))

        while self.opened:
            # current is an opened node with the lowest fScore
            current = self.opened[0]

            for node in self.opened:
                if node.fScore < current.fScore:
                    current = node

            if current == endNode:
                # found the path - display the path
                path = []
                node = endNode
                
                while node.getParent():
                    data = (node.getParent().row,node.getParent().column)
                    path.append(data)
                    node = node.getParent()
                #path.pop()
                print path
                
                self.reconstructPath(endNode)
                #print self.AlternatePath(path)
                print self.findPath(self.start,self.end,path)

                for cord in path:
                    self.blocks.remove((cord[0],cord[1]))
            
                return(True)

            self.opened.remove(current)
            self.closed.append(current)

            for neighbour in self.getNeighbours(current):
                if neighbour in self.closed:
                    continue    # ignore it because it has already been evaluated

                # the distance from start to a neighbour
                tempGScore = current.gScore + self.getDistance(current, neighbour)
                if neighbour not in self.opened:    # discover a new node
                    self.opened.append(neighbour)
                elif tempGScore >= neighbour.gScore:
                    continue    # this is not a better path

                # this path is the best path until now
                neighbour.setParent(current)
                neighbour.setGScore(tempGScore)
                neighbour.setFScore(tempGScore + self.getDistance(neighbour, endNode)) # fScore = gScore + hCost

        
        return False    # failure to find a path

    def getDistance(self, node, endNode):
        xDistance = node.column - endNode.column
        yDistance = node.row - endNode.row

        hCost = math.sqrt((xDistance**2) + (yDistance**2))

        return(hCost)

    def getNeighbours(self, node):
        neighbours = []
        row = node.row
        column = node.column
        # add corners if the path can go diagonally
        #adjacentCoordinates = [(row-1, column), (row, column-1), (row, column+1), (row+1, column)]
        adjacentCoordinates = [(row-1, column), (row, column-1), (row, column+1), (row+1, column), (row-1, column-1), (row-1, column+1), (row+1, column-1), (row+1, column+1)]

        for coord in adjacentCoordinates:
            if (coord[0], coord[1]) not in self.blocks and coord[0] >= 0 and coord[0] <= self.width-1 and coord[1] >= 0 and coord[1] <= self.height-1:
                # valid node
                neighbours.append(self.nodes[coord[0]][coord[1]])

        return(neighbours)

    def reconstructPath(self, endNode):
        endNode.changeColor("green")
        current = endNode.getParent()
        
        while current.getParent():
            current.changeColor("yellow")
            time.sleep(0.2)
            self.window.flush()
            current = current.getParent()
        
        current.changeColor("blue")
        self.window.flush()

class Node:
    def __init__(self, x, y, size, window, color, row, column):
        self.x = x
        self.y = y
        self.size = size
        self.window = window
        self.color = color
        self.row = row
        self.column = column
        self.parent = None
        self.fScore = sys.maxsize
        self.gScore = sys.maxsize

    def draw(self):
        node = Rectangle(Point(self.x, self.y), Point(self.x + self.size, self.y + self.size))
        node.setFill(self.color)
        node.setOutline(self.color)
        node.draw(self.window)

    def setFScore(self, fScore):
        self.fScore = fScore

    def setGScore(self, gScore):
        self.gScore = gScore

    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return(self.parent)

    def changeColor(self, newColor):
        node = Rectangle(Point(self.x, self.y), Point(self.x + self.size, self.y + self.size))
        node.setFill(newColor)
        node.setOutline(newColor)
        node.draw(self.window)


def main():
    # size in terms of # of nodes
    gridWidth = WIDTH
    gridHeight = HEIGHT
    # size of each node in pixels
    nodeSize = 10
    # gap between each node in pixels
    gap = 2
    # subtracting 5px just makes it look nicer
    screenWidth = (gridWidth * nodeSize) 
    screenHeight = (gridHeight * nodeSize) + ((gridHeight ) * gap) 
    print screenHeight
    print screenWidth
    # create window
    window = GraphWin("A* Simulation", WIDTH, HEIGHT, autoflush=False)
    window.setBackground("#636363")
    window.setCoords(0,0,COORDS_X,COORDS_Y)
#     window.flush()

    grid = Grid(COORDS_X/griDim, COORDS_Y/griDim, griDim, gap, window)
    #grid.start = (1,5)
    #grid.end = (30,5)
    grid.draw()

    if grid.findPath((8,1),(4,7),[]):
        print("Path Successful")
    else:
        print("Path Not Found")
        for row in grid.nodes:
            for node in row:
                node.changeColor("red")
        window.flush()
    window.getMouse();

main()
