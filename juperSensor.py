from L3GD20 import L3GD20
from LSM303 import Adafruit_LSM303
from kalmanfilter import KalmanFilterLinear
import time
import math
import numpy
import os
import threading

class juperSensor(threading.Thread):

    def __init__ (self):
        super(juperSensor, self).__init__()
        self.GyroSensor = L3GD20(busId = 1, slaveAddr = 0x6b, ifLog = False, ifWriteBlock=False)
        self.AccSensor = Adafruit_LSM303()

        self.GyroSensor.Set_PowerMode("Normal")
        self.GyroSensor.Set_FullScale_Value("250dps")
        self.GyroSensor.Set_AxisX_Enabled(True)
        self.GyroSensor.Set_AxisY_Enabled(True)
        self.GyroSensor.Set_AxisZ_Enabled(True)

        self.DelayTime = 0.02

        self.gyroStatus = [0, 0, 0]
        self.accStatus = [0,0,0]
        self.current_angle = [0, 0, 0]
        
        self.kf = KalmanFilterLinear(
            _A = numpy.eye(1),
            _B = 0,
            _H = numpy.eye(1),
            _x = numpy.matrix([0, 0, 0]),
            _P = numpy.eye(1),
            _Q = numpy.eye(1) * 0.001,
            _R = numpy.eye(1) * 0.01            
            )
        self.isRunning = True;

        self.GyroSensor.Init()
        self.GyroSensor.Calibrate()

    def run(self):
        while self.isRunning: 
            gyro_dxyz = self.GyroSensor.Get_CalOut_Value()
            self.gyroStatus = self.getAngleGyro(gyro_dxyz)
            self.accStatus = self.getAngleAcc(self.AccSensor.read())
            self.accStatus = self.kf.filter(numpy.matrix([0, 0, 0]), self.accStatus)
            self.current_angle = self.getAngleCombine()

            time.sleep(self.DelayTime)

    def stop(self):
        self.isRunning = False

    def getAngleGyro(self, gyro_dxyz):
        result = self.gyroStatus
        for i in range(3):
            result[i] = gyro_dxyz[i] * self.DelayTime 
        return result

    def getAngleAcc(self, acc):
        g = 9.80665
        pi = 3.141592
        result = [0,0,0]

        result[0] = math.atan2(acc[1], acc[2] + g) * 180 / pi
        result[1] = math.atan2(acc[0], acc[2] + g) * 180 / pi
        result[2] = math.atan2(acc[0], acc[1] + g) * 180 / pi
        return result

    def getAngleCombine(self):
        tau = 0.003
        result = [0,0,0]
        
        a = tau / (tau + self.DelayTime)
        for i in range(3):
            result[i] = a * (self.accStatus[i] + self.gyroStatus[i] * self.DelayTime) + (1 - a) * self.current_angle[i]

        return result

    def getCurrentAngleStatus(self):
        return self.current_angle