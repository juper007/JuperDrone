import bluetooth
import time

def log(message):
	print (message)

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

def communicationHandle(sock):
    data = ""
    while data != "END":
        data = sock.recv(1024).decode(encoding='UTF-8')
        cmd = data[0:3]
        print(data)

    return False   

if __name__ == "__main__":
	
    #bd_addr = "78:59:5E:81:2C:BC"
    target_addr = "B4:62:93:70:8E:F9" # S3
    target_uuid = "0B3C15DD-063A-4921-9BDA-103693A1E26F"

    isRunning = True
    while isRunning:
        try:
        	print ("Trying to find the service...")
        	socket = find_service(target_uuid, target_addr)
        	print ("Found Service : " + socket["host"], socket["port"])
        	socket = connectBluetooth(socket)
        	print ("Connected to bluetooth device")
        	print ("Waiting for data...")
        	isRunning = communicationHandle(socket)
        except:
            #landing(motors)
            log("Error")

        socket.close()
