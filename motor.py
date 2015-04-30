from RPIO import PWM
import time

class motor:
    def __init__(self, pin, WMin = 0, WMax = 100):
        self.pin = pin
        self.min = WMin
        self.max = WMax
        self.PWM = PWM
        self.current_PW = 0

    def start(self):
        if not self.PWM.is_setup:
            self.PWM.setup(pulse_incr_us=1)
            self.PWM.init_channel(0, 3000)

    def stop(self):
        self.setW(0)
        self.PWM.clear_channel(0)
        self.PWM.cleanup()

    def setW(self, value):
        PW = 0
        if value > self.WMax:
            value = self.WMax
        elif value < self.min:
            value = self.min

        PW = int(1000 + (value * 10))
        self.PWM.add_channel_pulse(0, self.pin, 0, PW)

        self.current_PW = value

    def getW(self):
        return slef.current_PW

