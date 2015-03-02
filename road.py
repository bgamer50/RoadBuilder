from func import shash
from copy import deepcopy as copy

#This is the Road class, responsible for holding all road information.  Ultimately, the most important info is its path and junctions.
class Road:
    path = [] #List of each place on the grid it passes through. WILL BE REMOVED
    #the path's start and end are junctions.
    junctions = [] #constant length of 2 WILL BE REMOVED
    numLanes = 2 #default is a 2-lane road
    classification = 1 #See below
    speed = 25
    toll = 0
    name = ""
    ID = None
        
    def __init__(self, n, points): #POINTS MUST BE IN ORDER!!!!!
		self.name = n
		self.numLanes = 2
		self.classification = 1
		self.speed = 25
		self.toll = 0
		self.ID = None
	
#Road Classifications - Affect how cars use the roads.  Users can modify these under advanced settings; the road chooses one by default.
#1. generic
    #This is the profile of a standard 2-lane road usually.  It's the default profile given.
#2. highway
    #This is meant for roads primarily used for thru traffic with speed limits upwards of 45 MPH.
    #Restrictions: Speed Limit must be over 45 MPH and road must have > 2 lanes.
#3. highway-2L
    #This is meant for 2-lane highways with speed limits upwards of 45 MPH.
    #Restrictions: Speed Limit must be over 45 MPH and road must have only 2 lanes.
#4. freeway
    #The freeway profile is heavily restricted.  Even in advanced settings, users cannot choose it.  This is for fast-moving highways with no lights.
    #Restrictions: Speed Limit must be >= 55 MPH and road must not have any lights or stop signs except at its start and end point.
#5. freeway-lev2
    #Reserved only for freeways with very high speed limits.
    #Restrictions: Speed Limit must be >= 65 MPH and road
#6. residential
    #For roads used only for residential purposes.
    #Restrictions: None