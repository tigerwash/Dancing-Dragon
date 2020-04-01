# excise 05 class
# ARCH 591
# Longtai Liao 

import rhinoscriptsyntax as rs
import scriptcontext as sc
import random as rnd


class Attractor():
    
    def __init__(self, POS, POINTID, MAG):
        self.pos = POS
        self.pointID = POINTID
        self.mag = MAG
        
    def GetInfluenceVec(self, agent):
        
         #create vector from current agent position and current attractor point
         newVec = rs.VectorCreate(self.pos, agent.pos)   # for the agent.pos, the agent is the input,  agent.pos means the paramate "pos" coming from the input of function getInfluenceVec(self, agent) which is located in Agent()
         #unitize vector
         newVec = rs.VectorUnitize(newVec)
         #measure distance bewteen attractor point and agent
         dist = rs.Distance(self.pos, agent.pos)
         #scale vector based on distance and magnitude
         newVec = rs.VectorScale(newVec, self.mag/dist)
         #return newVec value
         return newVec

#add length parameter to the function 
class Agent():
    
    def __init__(self, POS, POINTID, VEC, LENGTH):
        self.pos = POS
        self.pointID = POINTID
        self.vec = VEC
        self.trailPts = []
        self.trailPts.append(self.pos) #this is the same as the line 77
        self.trailEndPts = []
        self.trailID = "imnotacurveyet!"
        self.length = LENGTH 
        
    def test(self):
        print self.pos
        print self.pointID
        print self.vec
        
    def update(self, ATTRACTORPOPULATION):
        #print ATTRACTORPOPULATION[0].pos
        self.updateVecAttr(ATTRACTORPOPULATION)
        #self.updateVecBoundary()
        self.move()
        self.drawpipes()
        
    def updateVecAttr(self,ATTRACTORPOPULATION):
         
         #call GetInfluenceVec function in Attractor Class for each attractor point
         #send agent data for current agent point
         for myAttractor in ATTRACTORPOPULATION:
             
            vec = myAttractor.GetInfluenceVec(self)     # input myAttractor into GetInfluenceVec(). the (self) is attractor points in attractorPopulation which is in main(). 
            #update agent point vector with returned vector
            self.vec = rs.VectorAdd(self.vec, vec)
        
    def move(self):
        #print 'imnotworkingyet!'
        self.pos = rs.PointAdd(self.pos, self.vec)
        self.trailPts.append(self.pos)
        #rs.AddPoint(self.pos)
        if len(self.trailPts)>self.length:
            self.trailEndPts = self.trailPts[-(self.length-1):] #get the end part of the trail line 
        else :
            self.trailEndPts = self.trailPts 
    #draw pipes by slice the end of the curves 
    def drawpipes(self):
        #do not try to make a curve if the list only contains one point
        if self.trailID != "imnotacurveyet!":
            #delete variable
            rs.DeleteObject(self.trailID)
            rs.DeleteObject(self.pipes)
        self.trailID = rs.AddCurve(self.trailEndPts,3)
        #self.pipes = rs.AddPipe(self.trailID,0,(0.3+2*rnd.random()))
        #for pipe in self.trailID:
        r = 0.1+1*rnd.random() # pipe radio 
        R = r*150
        self.pipes = rs.AddPipe(self.trailID,0,r)
        #rs.HideObjects(curves)
        rs.ObjectColor(self.pipes,(R%255,(R+150)%255,(R+75)%255))
        #for line in self.trailID:
            #rs.AddPipe(line,0,4)
            




def main():

    #collect base points 
    pointGUIDs = rs.GetObjects('select points to make agents', rs.filter.point)
    attractorGUIDs = rs.GetObjects('select points to make attractors', rs.filter.point)
    #define pipe length  
    pipelength = rs.GetInteger('set the length of the pipe', 15 )
    #set up the agent
    vec = [1,1,1]
    agentPopulation = []
    for pointGUID in pointGUIDs:
        
        coord = rs.PointCoordinates(pointGUID)
        agentPopulation.append(Agent(coord, pointGUID, vec, pipelength))   #get the poins which draw lines 
    
    #set up attractor
    magnitude = 10
    attractorPopulation = []
    for attractorGUID in attractorGUIDs:
        
        coord = rs.PointCoordinates(attractorGUID)
        attractorPopulation.append(Attractor(coord, attractorGUID, magnitude))  #get the list of attractor points 
    
    #agentPopulation[0].test()
    
    #set up looped call
    while not sc.escape_test():
        
        for agent in agentPopulation:
            
            agent.update(attractorPopulation)  #continue the line 
    
    
main()