from pid import pid
import datetime

class juperPID(object): 
    def __init__(self):
        self.x_PID = pid(0.070, 0.025, 0.010, 15)
        self.y_PID = pid(0.070, 0.025, 0.010, 15)
        self.x_corr = 0
        self.y_corr = 0
        self.target_angle = [0,0]

    def log(self, message):
        print ("[PID] {0} : {1}".format(datetime.datetime.now(), message))

    def getPID(self, senserStatus, timeStep):
        result = [0,0,0,0]
        self.x_corr = self.x_PID.calc(self.target_angle[0], senserStatus[0], timeStep)
        self.y_corr = self.y_PID.calc(self.target_angle[1], senserStatus[1], timeStep)

        result[0] = (self.x_corr / 2) + -(self.y_corr / 2)
        result[1] = (self.x_corr / 2) + (self.y_corr / 2)
        result[2] = -(self.x_corr / 2) + -(self.y_corr / 2)
        result[3] = -(self.x_corr / 2) + (self.y_corr / 2)
        return result
