from juperBluetooth import juperBluetooth
from juperMotors import juperMotors
import datetime

def log(message):
    print ("[Main] {0} : {1}".format(datetime.datetime.now(), message))

if __name__ == "__main__":
    log ("Start")

    timeStep = 0.02

    # init sensor
    # init motors
    motors = juperMotors([17, 18, 22, 23])

    # init Bluetooth
    comm = juperBluetooth()
    comm.start()
    
    while comm.isRunning:
        if (comm.hasCommand):
            # do Something
            command = comm.command.pop(0)
            if (command[0] == "01"):
                log(command)
                # Move up
            elif (command[0] == "02"):
                # Move down
                log(command)
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
            comm.hasCommand = False

        # Get sensor value
        # Calculate PID
        # Update Motors
        sleep(timeStep)

    # Check motor if Drone is still flying
    #   if yes - do landing

    # End
    log ("End")

