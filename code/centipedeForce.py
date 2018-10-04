from joy import *
from math import copysign,cos,sin,pi
from numpy import *
from numpy import linalg
import time
import ckbot.dynamixel as DX
import ckbot.logical as logical
import math
from copy import copy

# For plotting Buehler
import matplotlib
matplotlib.use('TkAgg') #Uses a backend that is usable in OSX as well
import matplotlib.pyplot as plt
import pylab
import numpy as np

nm = { 
0x0A : 'H', #10
0x14 : 'S3', #20
0x1E : 'S4', #30
0x28 : 'M', #40
0x62 : 'S2', #50
0x3C : 'S1', #60
0x46 : 'F'  #70
}


gait_params = { 'roll' : -1820, 'bend' : -1480, 'phi_off' : 0, 'omega': 1, 'a': 0, 'freq': 2.1} 


 
###Dec 24 Video
#gait_params = { 'roll' : -1370, 'bend' : -2180, 'phi_off' : 0, 'omega': 1, 'a': 0, 'freq': 1.5} 

class EnepodGaitApp( JoyApp ):
  def __init__(self,*arg,**kw):

    #self.bus = dynamixel.Bus()
    # set up protocol with hitec bus    
    #p = hitec.Protocol(bus = self.bus)
    kw.update(robot=dict(names=nm,count=7))
    JoyApp.__init__(self, confPath="$/cfg/JoyAppCentipede.yml", *arg,**kw)
    self.last = time.time()
    self.button_map = yaml.load(open('/home/birds/pyckbot/cfg/demo-cfg.yaml'))
    self.gp = copy(gait_params);

    self.roll = 0
    self.bend = 0
    self.theta = 0
    self.turn = 0
    self.max_turn = 1500
    self.dir = 1

  def rollfunc(self, theta):
    return self.gp['roll']*sin(theta)
 
  def bendfunc(self, theta):
    return  clip(self.gp['bend']*cos(self.theta+self.gp['phi_off']),-1700,1700)

  def workFunction( self, phase ):
    self.freq  = self.gp['freq']
    self.theta = self.dir*(self.gp['omega']*2*pi*phase  - (1./(2*pi))*cos(2*self.gp['omega']*2*pi*phase)*self.gp['a'])#+self.turn*sin(self.gp['omega']*phase*2*pi)

    #self.roll = self.gp['roll']*sin(self.theta)
    #self.bend = clip(self.gp['bend']*cos(self.theta+self.gp['phi_off']),-1700,1700)
   
    if 1:
      self.robot.at.H.set_pos(self.rollfunc(self.theta+self.turn*sin(self.gp['omega']*phase*2*pi)))
      self.robot.at.F.set_pos(-self.rollfunc(self.theta+self.turn*sin(self.gp['omega']*phase*2*pi)))
      self.robot.at.M.set_pos(-self.rollfunc(self.theta-self.turn*sin(self.gp['omega']*phase*2*pi)))


      self.robot.at.S1.set_pos(-self.bendfunc(self.theta))
      self.robot.at.S2.set_pos(-self.bendfunc(self.theta))
      self.robot.at.S3.set_pos(-self.bendfunc(self.theta))
      self.robot.at.S4.set_pos(self.bendfunc(self.theta))




  def onStart(self):
    self.last = time.time()
    self.plan = FunctionCyclePlan(self, self.workFunction,N=180,interval=0.01)
    self.plan.onStart = curry(progress,">>> START")
    self.plan.onStop = curry(progress,">>> STOP")
    self.plan.setFrequency(self.gp['freq'])
    self.dir = 1

    sf = StickFilter(self)
    sf.setLowpass( "joy0axis0", 5)
    sf.setIntegrator( "joy0axis1", lower=-2500, upper=2500, gain=100)
    sf.setIntegrator( "joy0axis2", lower=-5000, upper=5000, gain=100)

    sf.start()
    self.sf = sf
    self.userStickCtrl = self.onceEvery(0.05)
    self.timeToShow = self.onceEvery(0.25)
    self.timeToPlot = self.onceEvery(0.5)

  def onStop(self):
    self.robot.off()
  
  def onEvent(self, evt):
    if self.userStickCtrl():
      self.turn =  self.dir*clip(self.sf.getValue("joy0axis0"),-0.75,0.75)
      self.gp['bend'] = int(self.sf.getValue("joy0axis1"))/10 * 10
      self.gp['roll'] = int(self.sf.getValue("joy0axis2"))/10 * 10

    #if self.timeToPlot():
      #progress('time: %g' % (time.time()))

    if self.timeToShow():
      sv = self.sf.getValue("joy0axis0")
      progress("Roll: %f, Bend:%f, Freq: %f, Theta: %f, Turn: %g" % (self.gp['roll'],self.gp['bend'], self.gp['freq'],self.theta, self.turn),sameLine=True)

    if evt.type==JOYBUTTONDOWN:
      button = (key for key,value in self.button_map.items() if value == evt.button).next()
      progress( describeEvt(evt) )
      # start
      if button=='start':
        progress('start')
        if not self.plan.isRunning():
          self.plan.start()
          progress('--> starting plan')
      if button=='select':
        if self.plan.isRunning():
          self.plan.stop()
          self.robot.off()
          progress('STOP')
      if button=='t':
           self.gp['freq'] += .1
           self.plan.setFrequency(self.gp['freq'])
      if button=='x':
           self.gp['freq'] -= .1
           self.plan.setFrequency(self.gp['freq'])
      if button=='rb':
         self.dir *= -1
      if button=='lb':
         self.turn = 0
      return
    if evt.type==KEYDOWN:
      if evt.key==ord('e'): # 'e' increases eccentricity
          gs.ecc += 0.1
      if evt.key==ord('d'): # 'd' decreases eccentricity
          gs.ecc -= 0.1

    if evt.type in [JOYAXISMOTION]:
      self.sf.push(evt)
      return
    if evt.type!=TIMEREVENT:
      JoyApp.onEvent(self,evt)



if __name__=="__main__":
  print """
  Enepod
  -------------------------------
  
  When any key is pressed, a 7-module centipede commences locomotion.

  The application can be terminated with 'q' or [esc]
  """
  robot = None
  
 # import cProfile
  import joy
  joy.DEBUG[:]=[]
  app=EnepodGaitApp(robot=dict(names=nm,count=7))
#  app=GaitTestPlanApp()
  try:
    app.run()
  finally:
    for k in xrange(5):
      app.robot.off()
      time.sleep(0.2)

#  cProfile.run(  app.run()  , 'centipede_profile_stats')

