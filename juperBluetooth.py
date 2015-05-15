import bluetooth
import datetime
import time
import threading

class juperBluetooth(threading.Thread):

    def __init__(self):
        super(juperBluetooth, self).__init__()
        #bd_addr = "78:59:5E:81:2C:BC"
        self.target_addr = "B4:62:93:70:8E:F9" # S3
        self.target_uuid = "0B3C15DD-063A-4921-9BDA-103693A1E26F"
        self.isRunning = True
        self.isConnected = False
        self.socket = None
        self.command = []
        self.hasCommand = False

    def log(self, message):
        print ("[BluetTooth] {0} : {1}".format(datetime.datetime.now(), message))

    def connectBluetooth(self, target):
        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        socket.connect((target["host"], target["port"]))
        self.isConnected = True
        return socket

    def find_service(self, serviceId, addr):
        isFound = False
        while (isFound == False):            
            target = bluetooth.find_service(address = addr, uuid = serviceId)
            if (len(target) > 0):
                return target[0]
                isFound = True
            time.sleep(1)

    def run(self):
        self.isRunning = True
        while self.isRunning:
            try:
                self.log("Finding the service...")
                self.socket = self.find_service(self.target_uuid, self.target_addr)
                self.log("Found Service : " + str(self.socket["host"]) + "," + str(self.socket["port"]))
                self.socket = self.connectBluetooth(self.socket)
                self.log("Connected to bluetooth device")
                self.log("Waiting for data...")
                self.isRunning = self.communicationHandle()
            except Exception as inst:
                self.log(type(inst))
                self.socket.close()

     ###########################################################
     # Receive Protocol
     #
     # 00|0|00 : End Communication
     # 01|0|XX : Move Up - XX set value
     # 02|0|XX : Move Down - XX set value
     # 03|S|XX : Move Left - XX set angle, S On(1)/Off(0)
     # 04|S|XX : Move Right - XX set angle, S On(1)/Off(0)
     # 05|S|XX : Turn CW - XX set value, S On(1)/Off(0)
     # 06|S|XX : Turn CCW - XX set value, S On(1)/Off(0)
     #
     # Send Protocol
     # 20|X|{ AA, BB, CC, DD} : Motor Status - X motor count, AA BB CC DD Value
     # 21|X|{ AA, BB, CC}  : Sensor Status - X Sensor count, AA BB CC Value
     #
     ###########################################################

    def communicationHandle(self):
        data = ""
        while data != "00000":
            data = self.socket.recv(1024).decode(encoding='UTF-8')
            cmd = data[0:2]
            swc = data[2:3]
            val = int(data[3:5])
            self.command.append([cmd, swc, val])
            self.hasCommand = True
        return False

    def sendMotorStatus(self, motorStatus):
        data = "20" + str(len(motorStatus))
        for val in motorStatus:
            val = int(round(val, 1) * 10)
            data = data + "{:0>3d}".format(val)
        self.socket.send(data)

    def sendSensorStatus(self, sensorStatus):
        data = "21" + str(len(sensorStatus))
        for val in sensorStatus:
            val = int(round(val, 2) * 100)
            data = data + "{:0>5d}".format(val)
        self.socket.send(data)


        