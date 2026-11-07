import sim as vrep
import Lab1_Agents_Task1_World as World
import sys, time, math, random

# Helpers
def A_setMovement(InSpeedLeft, InSpeedRight):
    return dict(speedLeft = InSpeedLeft, speedRight = InSpeedRight)
    
def A_run(motorSpeed):
    World.setMotorSpeeds(motorSpeed)

def A_UltraSensing(interval, realtime):
    # print some useful info, but not too often
    ultraSonicSensorLeft = World.getSensorReading("ultraSonicSensorLeft")
    ultraSonicSensorRight = World.getSensorReading("ultraSonicSensorRight")
    if realtime % interval == 0:
        print ('Time:',realtime,\
               'ultraSonicSensorLeft:',ultraSonicSensorLeft,\
               "ultraSonicSensorRight:", ultraSonicSensorRight)
    return {"ultraLeft": ultraSonicSensorLeft, "ultraRight": ultraSonicSensorRight}

def A_moveForward(speed=1, duration=5000, clockTime=-1, startTime=1000):
    while (World.getSimulationTime() < startTime):
        pass
    print("Starting to move forward with speed", speed, "for", duration, "ms.")
    World.execute(dict(speedLeft=speed, speedRight=speed),duration,clockTime)

def A_moveBackward(speed=1, duration=5000, clockTime=-1, startTime=1000):
    while (World.getSimulationTime() < startTime):
        pass
    print("Starting to move backward with speed", speed, "for", duration, "ms.")
    World.execute(dict(speedLeft=-speed, speedRight=-speed),duration,clockTime)

def A_turnLeft(speed=1, duration=5000, clockTime=-1, startTime=1000):
    while (World.getSimulationTime() < startTime):
        pass
    print("Starting to turn left with speed", speed, "for", duration, "ms.")
    World.execute(dict(speedLeft=speed, speedRight=speed+0.5),duration,clockTime)

def A_turnRight(speed=1, duration=5000, clockTime=-1, startTime=1000):
    while (World.getSimulationTime() < startTime):
        pass
    print("Starting to turn right with speed", speed, "for", duration, "ms.")
    World.execute(dict(speedLeft=speed+0.5, speedRight=speed),duration,clockTime)

def A_spin(speed=1, duration=5000, clockTime=-1, startTime=1000):
    while (World.getSimulationTime() < startTime):
        pass
    print("Starting to spin with speed", speed, "for", duration, "ms.")
    World.execute(dict(speedLeft=speed, speedRight=-speed),duration,clockTime)

def A_stopMotion():
    World.STOP()

def A_stopExecution():
    print("Stopping execution and exiting the program.")
    sys.exit(0)

def A_getCurrRobotPosition(robot):
    retCode, robotPos = vrep.simxGetObjectPosition(robot.clientID, robot.pioneerRobotHandle, -1, vrep.simx_opmode_oneshot_wait)
    return robotPos