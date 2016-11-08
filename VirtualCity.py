import sys
import os
from Tools import *
from random import *
from LocalBehaviour import *

c = 5
lmax = 20
lmin = -20
wmax = 20
wmin = -20

minrad = 0.25
maxrad = 0.35

settingspath = os.getcwd() + '/test.txt'
framepath = os.getcwd() + '/frame.txt'

objects = []
agents = []
roads = []
def erase():
    try:
        file = open(settingspath,"w")
        #file.write("#class posx posy h rad r g b")
        file.close
    except TypeError:
        return
    try:
        file = open(framepath,"w")
        #file.write("#class posx posy h rad r g b")
        file.close
    except TypeError:
        return

class building():
    def __init__(self,pos,size,color= None,nature=" ",draw=True):
        self.position = pos
        self.length = size[0]
        self.width = size[1]
	#if color==None:
	#  color = [random(),random(),random()]
        self.color = None
        self.classv = "building"
        self.nature = nature
        
        
        border0=(vector(pos.x-size[0]/2,pos.y-size[1]/2))
        border1=(vector(pos.x+size[0]/2,pos.y-size[1]/2))
        border2=(vector(pos.x+size[0]/2,pos.y+size[1]/2))
        border3=(vector(pos.x-size[0]/2,pos.y+size[1]/2))

        self.border = [border0,border1,border2,border3]
        self.bd = self.border
        self.line=[]
        for i in range(len(self.border)):
            li = line(self.border[i],self.border[(i+1)%len(self.border)])
            self.line.append(li)

        try:
            if draw:
              f=open(settingspath,'a')
              f.write("\nbuilding "+" "+str(pos.x)+"  "+str(pos.y)+" "+str(size[1])+" "+str(size[0])+" "+str(self.nature))
              f.close()
            
        except TypeError:
            print "cannot save his work"
            return

        objects.append(self)

class agent():
    def __init__(self,pos,rad,color=None,nature=""):
        nat=nature
        self.position = pos
        self.velocity = vector(0,0)
        self.radius = rad
        self.color = color
        self.orientation = 0
        self.classv = "agent"
        if nat=="":
            self.nature = "agent"
        else:
            self.nature=nat

        agents.append(self)

        id = agents.index(self)
        self.maingoal = objects[0] #Go to an object like building etc.
        self.path = [] #Path of the agent
#         self.bmotion = basicmotion(id,pos,rad,color)
        self.lbehaviour = localbehaviour()
#         self.gbehaviour = globalbehaviour()
        
        try:
            f=open(settingspath,'a')
            f.write("\nagent "+" "+str(pos.x)+"  "+str(pos.y)+" "+str(rad))
            f.close()
        except TypeError:
            print "cannot save his work"
            return

    def update_path(self):
        try:
            self.path = self.lbehaviour.findpath(self.position,self.maingoal.position)
            self.path.insert(0,self.maingoal.position)
        except KeyError:
            self.path = [self.maingoal.position]
	  

    def move(self):
      
        if self.path==[]:
            self.update_path()
            print self.path
            if len(self.path)==0:
                self.path = [self.maingoal.position]
#             self.bmotion.goals = self.path

        if self.maingoal.classv=="agent":
            self.bmotion.goals = [self.maingoal.position]
#         self.bmotion.update_position()
#         self.gbehaviour.updatestates()
#         self.position = self.bmotion.position
#         self.velocity = self.bmotion.velocity

