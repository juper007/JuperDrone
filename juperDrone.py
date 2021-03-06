from juperBluetooth import juperBluetooth
from juperMotors import juperMotors
from juperSensor import juperSensor
from juperPID import juperPID
import datetime
import time
import thread

def log(message):
    print ("[Main] {0} : {1}".format(datetime.datetime.now(), message))

def dataLog():
    f = open('DataLog.csv', 'a')
    data = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(datetime.datetime.now(),
        sensorStatus[0],sensorStatus[1],sensorStatus[2],
        pid.x_corr, pid.y_corr,
        motorStatus[0], motorStatus[1], motorStatus[2], motorStatus[3]
        )

    f.write(data)

def doBluetoothCommand(comm):
    if (comm.hasCommand):
        command = comm.command.pop(0)

        if (command[0] == "01"):
            # Move up
            motors.moveUp(command[2])

        elif (command[0] == "02"):
            # Move down
            motors.moveDown(command[2])

        elif (command[0] == "03"):
            # Move left
            log(command)

        elif (command[0] == "04"):
            # Move right
            log(command)

        elif (command[0] == "05"):
            # Turn CW
            log(command)                

        elif (command[0] == "06"):
            # Turn CCW
            log(command)
        elif (command[0] == "99"):
            # Stop Motors
            motors.stopMotors()

        else:
            log(command)
        comm.hasCommand = False

if __name__ == "__main__":
    log ("Start")
    # init values
    timeStep = 0.1
    motors_pin_array = [17, 18, 22, 23]
    motors_correction = [0, 0, 0, 0]
    motorStatus = [0, 0, 0, 0]
    sensorStatus = [0, 0, 0]    

    # init sensor
    sensors = juperSensor()
    sensors.start()
    # init motors
    motors = juperMotors(motors_pin_array)
    pid = juperPID()

    # init Bluetooth
    bluetooth = juperBluetooth()
    bluetooth.start()
    
    while bluetooth.isRunning:
        if (bluetooth.isConnected):
            doBluetoothCommand(bluetooth)
            
            # Get sensor value
            sensorStatus = sensors.getCurrentAngleStatus()

            # Calculate PID
            motors_correction = pid.getPID(sensorStatus, timeStep)
            
            # Update Motors
            for i in range(4):
                #i=i
                motors.setMotorW(i, motors_correction[i])

            motorStatus = motors.getCurrentStatus()
           
            bluetooth.sendMotorStatus(motorStatus)
            bluetooth.sendSensorStatus(sensorStatus)

        dataLog()
        time.sleep(timeStep)

    # Check motor if Drone is still flying
    #   if yes - do landing

    # End
    motors.stopMotors()
    sensors.stop()
    log ("End")

