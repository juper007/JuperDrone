from juperBluetooth import juperBluetooth
from juperMotors import juperMotors
import datetime
import time
import thread

def log(message):
    print ("[Main] {0} : {1}".format(datetime.datetime.now(), message))

if __name__ == "__main__":
    log ("Start")

    # init values
    timeStep = 0.1
    motors_pin_array = [17, 18, 22, 23]

    # init sensor
    # init motors
    motors = juperMotors(motors_pin_array)

    # init Bluetooth
    comm = juperBluetooth()
    thread.start_new_thread( comm.start, () )
    
    while comm.isRunning:
        #log("run")
        if (comm.hasCommand):
            # do Something
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

        # Get sensor value
        # Calculate PID
        # Update Motors
        # Send Motors Status
        if (comm.isConnected):
            comm.sendMotorStatus(motors.getCurrentStatus())
        time.sleep(timeStep)

    # Check motor if Drone is still flying
    #   if yes - do landing

    # End
    log ("End")

