import math
from time import sleep
import ckbot.logical as L
import numpy as np

nm = {  
    0x0A : 'F',
    0x3C : 'S1',
    0x14 : 'S2',
    0x28 : 'M',
    0x32 : 'S3',
    0x1E : 'S4',
    0x46 : 'H'
    }

c = L.Cluster(names=nm, count=7)
Max_roll = 2000
#Max_roll = 0
Max_yaw = 5000
#Max_yaw = 0

r = 0
y0 = 100
y = 0
tr = 2500    #60deg twist angle, just input 6000
# tr=250 is stright forward and backward
be0 = 100
be = 0
be_max= 0   # bend spine angle
Dr = 0
t = 0.00
t0 = 1.00
T = 40.00  #speed  higher = more points = slower T = [30, 100]


try:
    for m in [c.at.F,c.at.S1,c.at.S2,c.at.M,c.at.S3,c.at.S4,c.at.H]:
        m.set_pos(0)
    
    sleep(2)

    while be < be_max:
        c.at.S2.set_pos(be)
        c.at.S3.set_pos(-be)
        be += be0
        sleep(0.02)

    while y > -Max_yaw:
        c.at.F.set_pos(y+tr)
        c.at.M.set_pos(y-tr)
        c.at.H.set_pos(-1.5*(y+tr))
        y -= y0
        sleep(0.020)

    while t<= 6.25*T:
        r = Max_roll*math.sin(2*math.pi/T*t)
        y = -Max_yaw*math.cos(2*math.pi/T*t)
        c.at.F.set_pos(y+tr)
        #c.at.M.set_pos(-y+tr)
        c.at.M.set_pos(y-tr)
        c.at.H.set_pos(-1.5*(y+tr))
        c.at.S1.set_pos(r+Dr)
        c.at.S4.set_pos(r+Dr)  
        t += t0 
        sleep(0.020)  
    
    print "backwards"
    sleep(0.5)
    tr = 0
    #shake to straighten the robot back to start state 
    #for m in [c.at.S1,c.at.S2,c.at.S3,c.at.S4]:
        #m.set_pos(0)
        #m.go_slack()
        #for k in xrange(63):
            #s = math.sin(k/10.0)
            #r = int(math.sqrt(abs(s))*math.copysign(1,s)*4000)
            #c.at.F.set_pos(-r)
            #c.at.M.set_pos(r)
            #c.at.H.set_pos(r)

    #sleep(1)
    while t >= 6.25*T and t<= 6.75*T:
        t += t0

    while t >= 6.75*T and t<= 13*T:
        r1 = -Max_roll*math.sin(2*math.pi/T*t)
        y1 = -Max_yaw*math.cos(2*math.pi/T*t)
        r = r1 * math.cos(phi)-y1 * math.sin(phi)
        y = r1 * math.sin(phi)+y1 * math.cos(phi)
        c.at.F.set_pos(y+tr)
        c.at.M.set_pos(y+tr)
        c.at.H.set_pos(-(y+tr))
        c.at.S1.set_pos(r+Dr)
        c.at.S4.set_pos(r+Dr)  
        t += t0 
        sleep(0.020)
    

    for m in [c.at.F,c.at.S1,c.at.S2,c.at.M,c.at.S3,c.at.S4,c.at.H]:
        m.go_slack()
 


except KeyboardInterrupt:
    c.off()
    raise
