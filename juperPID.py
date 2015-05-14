from pid import pid

class juperPID(object):	
	def __init__(self):
		x_PID = pid()
    	y_PID = pid()

    def getPID(self, senserStatus):
    	result = [0,0,0,0]
    	x_Correction = x_PID.calc(target_angle[0], sensorStatus[0], timeStep)
        y_Correction = y_PID.calc(target_angle[1], sensorStatus[1], timeStep)

        result[0] = x_Correction / 2
        result[1] = x_Correction / 2 * -1
        result[2] = y_Correction / 2
        result[3] = y_Correction / 2 * -1
        return result
