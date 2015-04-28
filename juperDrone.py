from juperBluetooth import juperBluetooth
import datetime

def log(message):
    print ("[Main] {0} : {1}".format(datetime.datetime.now(), message))

if __name__ == "__main__":
    log ("Start")
    # init sensor
    # init motors
    # init Bluetooth
    comm = juperBluetooth()
    comm.start()
    
    while comm.isRunning:
        if (comm.hasCommand):
            print ("a")
            # do Something

        # Check sensor
        # Update Motors

    # Check motor if Drone is still flying
    #   if yes - do landing

    # End
    log ("End")

