import juperBluetooth from juperBluetooth
import datetime

def log(message):
	print ("[Main] %s : %s".format(datetime.datetime.now(), message)   

if __name__ == "__main__":

    # init sensor
    # init motors
    # init Bluetooth
    comm = juperBluetooth()
    comm.start()
    
    log ("Start")
    while comm.isRunning:
        if (comm.hasCommand):
            # do Something

        # Check sensor
        # Update Motors

    # Check motor if Drone is still flying
    #   if yes - do landing

    # End
    log ("End")

