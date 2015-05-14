from juperBluetooth import juperBluetooth
from juperMotors import juperMotors
from juperSensor import juperSensor
from juperPID import juperPID
import datetime
import time
import thread

def log(message):
    print ("[Main] {0} : {1}".format(datetime.datetime.now(), message))

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

        else:
            log(command)
        comm.hasCommand = False

if __name__ == "__main__":
    log ("Start")

    # init values
    timeStep = 0.1
    motors_pin_array = [17, 18, 22, 23]
    motors_correction = [0, 0, 0, 0]

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
        doBluetoothCommand(bluetooth)

        # Get sensor value
        sensorStatus = sensors.getCurrentAngleStatus()

        # Calculate PID
        motors_correction = pid.gePID(sensorStatus, timeStep)

        # Update Motors
        for i in range(len(motors.motors)):
            motors.setMotorW(i, motors_correction[i])

        # Send Motors Status
        if (bluetooth.isConnected):
            bluetooth.sendMotorStatus(motors.getCurrentStatus())
            bluetooth.sendSensorStatus(sensorStatus)
        time.sleep(timeStep)

    # Check motor if Drone is still flying
    #   if yes - do landing

    # End
    sensors.stop();
    log ("End")

