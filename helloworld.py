from L3GD20 import L3GD20
from LSM303 import Adafruit_LSM303
from kalmanfilter import KalmanFilterLinear
import time
import math
import numpy
import os

def getAngleGyro(gyro, gyro_dxyz, dt):
	gyro[0] = gyro_dxyz[0] * dt
	gyro[1] = gyro_dxyz[1] * dt
	gyro[2] = gyro_dxyz[2] * dt
	return gyro

def getAngleAcc(acc):
	g = 9.80665
	pi = 3.141592
	result = [0,0,0]

	result[0] = math.atan2(acc[1], acc[2] + g) * 180 / pi
	result[1] = math.atan2(acc[0], acc[2] + g) * 180 / pi
	result[2] = math.atan2(acc[0], acc[1] + g) * 180 / pi
	return result

def getAngleCombine(gyro, acc, prev_angle, dt):
	tau = 0.003
	result = [0,0,0]
	
	a = tau / (tau + dt)
	result[0] = a * (acc[0] + gyro[0] * dt) + (1 - a) * prev_angle[0]
	result[1] = a * (acc[1] + gyro[1] * dt) + (1 - a) * prev_angle[1]
	a=1 # Ignore Accel sensor for Z axle
	result[2] = a * (acc[2] + gyro[2] * dt) + (1 - a) * prev_angle[2]

	return result

s = L3GD20(busId = 1, slaveAddr = 0x6b, ifLog = False, ifWriteBlock=False)
lsm = Adafruit_LSM303()

s.Set_PowerMode("Normal")
s.Set_FullScale_Value("250dps")
s.Set_AxisX_Enabled(True)
s.Set_AxisY_Enabled(True)
s.Set_AxisZ_Enabled(True)

dt = 0.02

gyro = [0, 0, 0]
current_angle = [0, 0, 0]

A = numpy.eye(1)
H = numpy.eye(1)
B = numpy.eye(1)*0
Q = numpy.eye(1)*0.001
#play with Q to tune the smoothness
R = numpy.eye(1)*0.01
xhat = numpy.matrix([0, 0, 0])
P= numpy.eye(1)

kf = KalmanFilterLinear(A,B,H,xhat,P,Q,R)

s.Init()
s.Calibrate()

while True:	
	gyro_dxyz = s.Get_CalOut_Value()
	gyro = getAngleGyro(gyro, gyro_dxyz, dt)
	acc = getAngleAcc(lsm.read())
	acc = kf.filter(numpy.matrix([0, 0, 0]), acc)
	current_angle = getAngleCombine(gyro, acc, current_angle, dt)

	os.system('clear')

	print("{:7.2f} {:7.2f} {:7.2f}".format(gyro[0], gyro[1], gyro[2]))
	print("{:7.2f} {:7.2f} {:7.2f}".format(acc[0], acc[1], acc[2]))
	print("{:7.2f} {:7.2f} {:7.2f}".format(current_angle[0], current_angle[1], current_angle[2]))
	time.sleep(dt)
