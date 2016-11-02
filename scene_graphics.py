import time
from graphics import *

settingspath = os.getcwd() + '/test.txt'
framepath = os.getcwd() + '/frame.txt'

agent = []
building = []
road = []
obstacle = []

def draw():
    settings = open(settingspath)
    settings.readline()
    while True:
        line = settings.readline()
        if line=="":
            break;
        line = line.split()
        x = float(line[1])
        y = float(line[2])

        if line[0]=="agent":
            rad = float(line[3])
            agent.append([[x,y,rad]])
	    
        if line[0]=="obstacle":
            rad = float(line[3])
            obstacle.append([[x,y,rad]])
        if line[0]=="building":
            l = float(line[3])
            b = float(line[4])
            building.append([[x,y,l,b,line[5]]])
        if line[0]=="road":
            l = float(line[3])
            b = float(line[4])
            h = float(line[5])
            road.append([[x,y,zz,l,b,h]])
    settings.close()
    print agent
    #print obstacle
    print building
    #print road
    draw_graphics()
    
def draw_graphics():
    print "graphics library"
    positions=[]
    window=GraphWin("Crowd Simulation",width=400, height=400)
    window.setCoords(0,0,40,40)
    for a in agent:
        val = Circle( Point(a[0][0],a[0][1]), a[0][2]-0.1)
        val.setFill("red")
        positions.append([a[0][0],a[0][1]])
        val.draw(window)
        a.append(val)

    for o in obstacle:
        val = Circle( Point(a[0][0],a[0][1]), a[0][2])
        val.draw(window)
        val.setFill("red")
        o.append(val)

    for a in building:
        bd1 = Point(a[0][0], a[0][1])
        bd2 = Point(a[0][0], a[0][1] + a[0][2])
        bd3 = Point(a[0][0] + a[0][3], a[0][1] + a[0][2])
        bd4 = Point(a[0][0] + a[0][3], a[0][1])

        #Line(bd1,bd2).draw(window)
        #Line(bd2,bd3).draw(window)
        #Line(bd3,bd4).draw(window)
        #Line(bd4,bd1).draw(window)

        rect = Rectangle(bd1,bd3)
        rect.draw(window)
        

        anchorPoint = rect.getCenter()
        text = Text(anchorPoint, a[0][4])
        text.setSize(8)
        text.draw(window)

        #a.append(val)
    #time.sleep(2)
    try: 
        file = open(framepath)
    except TypeError:
        print "cannot find frame file"
    file.readline()
    while True:
        line = file.readline()
        if line=="":
            break;
        line = line.split()
        i= int(line[0])
        newpos = [float(line[1]),float(line[2])]
        dpos = [newpos[0]-positions[i][0],newpos[1]-positions[i][1]]
        agent[i][1].move(dpos[0],dpos[1])
        positions[i]=newpos
        time.sleep(0.1)
    file.close()
draw()
