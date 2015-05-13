from motor import motor
import datetime

class juperMotors(object):
    def __init__(self, pin_array):
        self.motors = []
        self.motorCount = len(pin_array)
        self.pins = pin_array

        for pin in pin_array:
            m = motor(pin)
            m.start()
            m.setW(0)
            self.motors.append(motor(pin))

    def log(self, message):
        print ("[Motor] {0} : {1}".format(datetime.datetime.now(), message))

    def setMotorW(self, index, offset):
        current_value = self.motors[index].getSetValue()
        self.motors[index].setW(current_value + offset)

    def moveUp(self, offset):        
        for i in range(self.motorCount):
            self.setMotorW(i, offset)
        self.log("Move Up - " + str(offset))

    def moveDown(self, offset):
        for i in range(self.motorCount):
            self.setMotorW(i, offset * -1)
        self.log("Move Down - " + str(offset))

    def getCurrentStatus(self):
        status = []
        for m in self.motors:
            status.append(m.getSetValue())
        return status
