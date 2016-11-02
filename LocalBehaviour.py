from voronoi import *
from Tools import *
#from crowd import *
import VirtualCity
from graphics import *
from random import *

roadfactor = 20
c = 1

def drawmap(roadmap):
    #from graphics import *
    window=GraphWin("Crowd Simulation",width=500, height=500)
    window.setCoords(0,0,40,40)
    #print VirtualCity.objects
    for b in VirtualCity.objects:
        if b.classv=="building" :
            p1 = Point(b.bd[0].x,b.bd[0].y)
            p2 = Point(b.bd[2].x,b.bd[2].y)
            #Line(p1,p2).draw(window)
            rec = Rectangle(p1,p2)
            rec.setFill("black")
            rec.draw(window)

        if b.classv=="road":
            p1 = Point(b.bd[0].x,b.bd[0].y)
            p2 = Point(b.bd[2].x,b.bd[2].y)
                #Line(p1,p2).draw(window)
            rec = Rectangle(p1,p2)
            rec.setFill("blue")
            rec.draw(window)
      
        if b.classv=="obstacle":
            p = Point(b.position.x,b.position.y)
            Circle(p,b.radius).draw(window)

    for b in VirtualCity.roads:
        for l in b.line:
            p1 = Point(l.start.x,l.start.y)
            p2 = Point(l.end.x,l.end.y)
            Line(p1,p2).draw(window)

    edges = roadmap.get_edges()
    
    for edge in edges:
        #print edge
        p1 = Point(edge[0][0],edge[0][1])
        p2 = Point(edge[1][0],edge[1][1])
        p1.draw(window)
        p2.draw(window)
        Line(p1,p2).draw(window)

    #raw_input()
            
def rectanglewithOffset(recv,offset):
    rec=[]
    for r in recv:
      rec.append([r.x,r.y])
    outlinex = []
    outliney = []
    for i in range(4):
        if outlinex.count(rec[i][0])==0:
            outlinex.append(rec[i][0])
        if outliney.count(rec[i][1])==0:
            outliney.append(rec[i][1])
    x0 = min(outlinex[0], outlinex[1])
    x1 = max(outlinex[0], outlinex[1])
    y0 = min(outliney[0], outliney[1])
    y1 = max(outliney[0], outliney[1])
    out = [x0,x1,y0,y1]
    outline = [out[0]-offset, out[1]+offset, out[2]-offset, out[3]+offset]
    return [[outline[0],outline[2]],[outline[1],outline[2]],[outline[1],outline[3]],[outline[0],outline[3]]]  

class localbehaviour(object):

            
    def add_buildingnodes(self):
        for o in VirtualCity.objects:
            self.roadmap.addnode(o.position)
            #if o.classv =="building":
            #    self.roadmap.addnode(o.doorpos)
            points = []
            offset = uniform(1.5,2.5)
            rec = rectanglewithOffset(o.bd,0.5*offset)
            for r in rec:
                points.append(vector(r[0],r[1]))
	    #self.connect(midPoint(rec[ob.doorint],rec[(ob.doorint+1)%4]),ob.doorpos)
	    #self.connect(ob.position,ob.doorpos)
            for point in points:
                self.connect_node(point)
	      #self.add(point,self.obstacles,self.roads)        
                
        
    def add_roadnodes(self):
        graph = self.roadmap
        for ob in VirtualCity.roads:
            rec = []
            rec.extend(ob.bd)
            for p in rec:
                if p.z<0:
                    p.z+=5
                if p.z>0:
                    p.z-=5
            for point1 in rec:
                for point2 in rec:
                    if point1!=point2 and point1.z==point2.z:
                        graph.addnode(point2)
                        graph.addnode(point1)
                        graph.addedge(point1,point2)

        #for o in VirtualCity.road:
            #for b in o.border:
                #self.roadmap.addnode(b)
        
    def add_randomnodes(self, number=5):
        nodes=[]
        while len(nodes)<=number:
            while True:
                xx = uniform(VirtualCity.lmin,VirtualCity.lmax)
                zz = uniform(VirtualCity.wmin,VirtualCity.wmax)
                point = vector(xx,0,zz)
                if len(nearobject(point))==0:
                       nodes.append(point)
                       break
        self.roadmap.addnodes(nodes)
        
        
    def connect_all(self):
        nodes = self.roadmap.get_nodes()
        for n1 in nodes:
            for n2 in nodes:
                n1=vector(node1[0],0,node1[1])
                n2=vector(node2[0],0,node2[1])
                if (not n1==n2) and (n1.z*n2.z>0 and n1.x*n2.x>0) and (not linenearobject(line(n1,n2))):
                    if linenearroad(line(n1,n2)):
                        continue
                    self.roadmap.addedge(n1,n2)
                       

    def connects(self):
      nodes = self.roadmap.get_nodes()
      for n1 in nodes:
          self.connect(n1)

    def connect(self,n1):
        nodes = self.roadmap.get_nodes()
        self.roadmap.addnode(n1)
        near=None
        dist=1000
        for n in nodes:
            n2=vector(n[0],n[1])
            if not(n1==n2):
                #and (not linenearobject(line(n1,n2))) and (not linenearroad(line(n1,n2))):
                near = n2
                dist = mag(n1-near)
        if near!=None:
            self.roadmap.addedge(n1,near)
        else:
            self.connect_node(n1)
        
        
                       
     
    def connect_node(self, n1):
        self.roadmap.addnode(n1)
        nodes = self.roadmap.get_nodes()
        for n in nodes:
            n2=vector(n[0],n[1])
            if (not n1==n2):
                #and (not linenearobject(line(n1,n2))) and (not linenearroad(line(n1,n2))):
                self.roadmap.addedge(n1,n2)
                       #if linenearroad(line(n1,n2)):
                       #wt = self.roadmap.edges[(n1,n2)][1]
                       #self.roadmap.set_edge_weight(n1,n2,wt*roadfactor)

    def testaccess(self):
        nodes = self.roadmap.get_nodes()
        node = nodes[0]
        
        for n in nodes:
            if not(node==n):
                try:
                    self.findpath(node,n)
                except KeyError:
                    return False
        return True
                

    def accessible(self):
        point = vector(0.0,0.0,0.0)
        self.connect(point)
        while not self.testaccess():
            self.roadmap.deletenode(point)
            while True:
                xx = uniform(VirtualCity.lmin+c,VirtualCity.lmax-c)
                zz = uniform(VirtualCity.wmin+c,VirtualCity.wmax-c)
                point = vector(xx,0,zz)
                if len(nearobject(point))==0:
                    self.connect(point)
                    break
            
        
        
    def findpath(self, node1, node2):
        #self.roadmap.addnodes([node1,node2])
        nodes = self.roadmap.get_nodes()
        if not ((node1.x,node1.y) in nodes):
            self.connect(node1)
        if not ((node2.x,node2.y) in nodes):
            self.connect(node2)
        self.path = self.roadmap.findpath(node1,node2)
        return self.path
        
    def __init__(self):
        self.roadmap = graph()
        self.path = []
        self.add_roadnodes()
        self.add_buildingnodes()
        #self.add_randomnodes()
        #self.generatevoronoi()
        #self.connect_all()
	#self.connects()
        #drawmap(self.roadmap)
	
       
'''
def generatevoronoi(self):
        pts = []
        added = []
        num = 0
        for b in VirtualCity.object:
            if b.classv=="building":
                for li in b.line:
                    if not li.start in added:
                        added.append(li.start)
                        pts.append(Site(li.start.x,li.start.z,num))
                        num = num+1
                    if not li.end in added:
                        added.append(li.end)
                        pts.append(Site(li.end.x,li.end.z,num))
                        num = num+1
##                    middle = (li.start+li.end)*0.5
##                    if not middle in added:
##                        added.append(middle)
##                        pts.append(Site(middle.x,middle.z,num))
##                        num = num+1
        for b in VirtualCity.road:
            for li in b.line:
                if not li.start in added:
                    added.append(li.start)
                    pts.append(Site(li.start.x,li.start.z,num))
                    num = num+1
                if not li.end in added:
                    added.append(li.end)
                    pts.append(Site(li.end.x,li.end.z,num))
                    num = num+1
##                middle = (li.start+li.end)*0.5
##                if not middle in added:
##                    added.append(middle)
##                    pts.append(Site(middle.x,middle.z,num))
##                    num = num+1
        others = [vector(VirtualCity.lmin,0,VirtualCity.wmin),vector(VirtualCity.lmax,0,VirtualCity.wmin)]
        others.extend([vector(VirtualCity.lmin,0,VirtualCity.wmax),vector(VirtualCity.lmax,0,VirtualCity.wmax)])
        for p in others:
            if not p in added:
                added.append(p)
                pts.append(Site(p.x,p.z,num))
                num = num+1
        
        compvoronoi = computeVoronoiDiagram(pts)
        sitelist = compvoronoi[0]
        edgelist = compvoronoi[2]
        edges = []
        for ed in edgelist:
            startind = ed[1]
            endind = ed[2]
            if startind!=-1 and endind!=-1:
                start = sitelist[startind]
                end = sitelist[endind]
                n1 = vector(start[0],0.0,start[1])
                n2 = vector(end[0],0.0,end[1])
                if not(n1==n2):
                    edges.append((n1,n2))
        
        for edg in edges:
            n1 = edg[0]
            n2 = edg[1]
            if n1.x>VirtualCity.lmin and n1.z>VirtualCity.wmin and n1.x<VirtualCity.lmax and n1.z<VirtualCity.wmax:
                self.roadmap.addnode(n1)
            if n2.x>VirtualCity.lmin and n2.z>VirtualCity.wmin and n2.x<VirtualCity.lmax and n2.z<VirtualCity.wmax:
                self.roadmap.addnode(n2)
        
        
        nodes = self.roadmap.get_nodes()
        for n1 in nodes:
            for n2 in nodes:
                if (not n1==n2)and ((n1,n2) in edges) and (not linenearobject(line(n1,n2))):
                   self.roadmap.addedge(n1,n2)
                   if linenearroad(line(n1,n2)):
                       wt = self.roadmap.edges[(n1,n2)][1]
                       self.roadmap.set_edge_weight(n1,n2,wt*roadfactor)
                        
            

'''
