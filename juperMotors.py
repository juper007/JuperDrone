from motor import motor

class juperMotors(object):
    def __init__(self, pin_array):
        self.motors = []
        
        for pin in range(len(pin_array)):
            m = motor(pin)
            m.start()
            m.setW(0)
            self.motors.append(motor(pin))

    def setMotorW(self, index, offset):
        current_value = self.motors[index].getSetValue
        self.motors[index].setW(current_value + offset)

    def moveUp(self, offset):
        for i in range(len(self.motors)):
            self.setMotorW(i, offset)

    def moveDown(self, offset):
        for i in range(len(self.motors)):
            self.setMotorW(i, offset * -1)

    def getCurrentStatus(self):
        status = []
        for m in self.motors:
            status.append(m.getSetValue)
        return status
