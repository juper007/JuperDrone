import bluetooth
import datetime
import time

class juperBluetooth(object):
	def __init__(self):
		#bd_addr = "78:59:5E:81:2C:BC"
    	self.target_addr = "B4:62:93:70:8E:F9" # S3
    	self.target_uuid = "0B3C15DD-063A-4921-9BDA-103693A1E26F"
    	self.isRunning = False
    	self.socket = None
    	self.command = []
    	self.hasCommand = False

    def log(self, message):
    	print ("[BluetTooth] %s : %s".format(datetime.datetime.now(), message))

    def connectBluetooth(target):
	    socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	    socket.connect((target["host"], target["port"]))
	    return socket

	def find_service(serviceId, addr):
	    isFound = False
	    while (isFound == False):
	        target = bluetooth.find_service(address = addr, uuid = serviceId)
	        if (len(target) > 0):
	            return target[0]
	            isFound = True
	        time.sleep(1)

	 ###########################################################
	 # Protocol
	 #
	 # 00|00 : End Communication
	 # 01|XX : Move Up - XX set value
	 # 02|XX : Move Down - XX set value
	 # 03|XX : Move Left - XX set angle, XX = 00 stop moving
	 # 04|XX : Move Right - XX set angle, XX = 00 stop moving
	 # 05|XX : Turn CW - XX set value, XX = 00 stop turning
	 # 06|XX : Turn CCW - XX set value, XX = 00 stop turning
	 #
	 ###########################################################

	def communicationHandle(self, sock):
	    data = "00"
	    while data != "00":
	        data = sock.recv(1024).decode(encoding='UTF-8')
	        cmd = data[0:2]
	        val = data[2:4]
	        self.command.append([cmd, val])
	        self.hasCommand = True
	    return False

    def start(self):
    	self.isRunning = True
    	while self.isRunning:
	        try:
	        	self.log("Finding the service...")
		    	self.socket = find_service(self.target_uuid, self.target_addr)
		    	self.("Found Service : " + self.socket["host"], self.socket["port"])
		    	self.socket = connectBluetooth(socket)
		    	self.log("Connected to bluetooth device")
		    	self.log("Waiting for data...")
		    	isRunning = communicationHandle(socket)
	        except:

	        socket.close()
	    