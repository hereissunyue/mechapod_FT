import math
from time import sleep
import ckbot.logical as L
import numpy as np

nm = {  
	0x0A : 'H',
	0x3C : 'S4',
	0x14 : 'S3',
	0x28 : 'M',
	0x32 : 'S2',
	0x1E : 'S1',
	0x46 : 'F'
	}

class mechapod_FT:
	def __init__(self):
		""" initializing the connection """
		self.c = L.Cluster(names=nm, count=7)

	def set_zero(self):
		""" set all positions to zero """
		for m in [self.c.at.F,self.c.at.S1,self.c.at.S2,\
		self.c.at.M,self.c.at.S3,self.c.at.S4,self.c.at.H]:
			m.set_pos(0)
		sleep(1.0)

	def set_slack(self):
		""" set all motors to slack mode """
		for m in [self.c.at.F,self.c.at.S1,self.c.at.S2,\
		self.c.at.M,self.c.at.S3,self.c.at.S4,self.c.at.H]:
			m.go_slack(0)
		sleep(1.0)

	def run(self, max_roll, max_yaw, cycle, T, direction, turn):
		""" run the robot with specifications
		run(max_roll, max_yaw, cycle, T, direction)
		max_roll = the rolling along the spine
		max_yaw = the twisting around z axis
		cycle = the stride number
		T = period length affects the speed, T up speed low
		direction = the direction of the robot, 1 forward, -1 backward
		turn = the turning angle of the robot"""
		self.max_roll = max_roll
		self.max_yaw = max_yaw
		self.cycle = cycle
		self.T = T
		self.direction = direction
		self.turn = turn
		st = 0
		pause = 0.02
		# status of postion inside the period. 
		# Initially set to 0 and have to be reset back to 0 for every new run
		while st <= self.cycle:
			roll = self.max_roll*sin(2*pi*st)
			yaw = self.max_yaw*sin(2*pi*st)
			st = round(st + 1/self.T,5)
			self.c.at.F.set_pos(roll+self.turn)
			self.c.at.M.set_pos(-roll+self.turn)
			self.c.at.H.set_pos(-roll+self.turn)
			self.c.at.S1.set_pos(-1*self.direction*yaw)
			self.c.at.S4.set_pos(-1*self.direction*yaw) 
			sleep(pause)


if __name__=="__main__":
	try:
		test = mechapod_FT()
		test.set_zero()
	except KeyboardInterrupt:
		test.set_slack()
		raise