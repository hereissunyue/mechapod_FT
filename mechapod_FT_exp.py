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

class mechapod_FT_exp:
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

	def run(self, max_roll, max_yaw, cycle, T, direction, turn_roll, turn_yaw):
		""" run the robot with specifications
		run(max_roll, max_yaw, cycle, T, direction,turn_roll, turn_yaw)
		max_roll = the rolling along the spine
		max_yaw = the twisting around z axis
		cycle = the stride number
		T = period length affects the speed, T up speed low, must be float number
		direction = the direction of the robot, 1 forward, -1 backward
		turn_roll = the turning parameter of the robot applied on the roll
		turn_yaw = the turning parameter of the robot applied on the yaw
		"""
		self.set_zero() # double check zero
		self.max_roll = max_roll
		self.max_yaw = max_yaw
		self.cycle = cycle
		self.T = T
		self.direction = direction
		self.turn_roll = turn_roll
		self.turn_yaw = turn_yaw
		st = 0
		pause = 0.02
		offset = -600 # mannually adjust the turing error not straight but better
		# status of postion inside the period. 
		# Initially set to 0 and have to be reset back to 0 for every new run
		try:
			while st <= self.cycle:
				roll = self.max_roll * sin(2 * pi * st)
				yaw = self.max_yaw * sin(2 * pi * st)
				st = round(st + 1/self.T,5)
				self.c.at.F.set_pos(roll + self.turn_roll + offset)
				self.c.at.M.set_pos(-roll + self.turn_roll + offset)
				self.c.at.H.set_pos(-roll + self.turn_roll + offset)
				self.c.at.S1.set_pos(-1 * self.direction * yaw + self.turn_yaw)
				self.c.at.S4.set_pos(-1 * self.direction * yaw + self.turn_yaw) 
				sleep(pause)
		except KeyboardInterrupt:
			self.set_zero()
			raise

if __name__=="__main__":
	test = mechapod_FT_exp()
	test.set_zero()