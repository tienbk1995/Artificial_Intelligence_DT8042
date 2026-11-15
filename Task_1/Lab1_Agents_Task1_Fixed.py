# Make sure to have the server side running in V-REP:
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simExtRemoteApiStart(19999)
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!
import Lab1_Agents_Task1_World as World
import Lab1_Agents_Lib as act
import math, time

# connect to the server
robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))


# Predefined movement sequence
actionSequence = [
    ("forward", 10000),
    ("turnRight", 500),
    ("backward", 500),
    ("turnLeft", 500),
]

blockInfo3 = act.A_calibrateBlockDistance(robot, "ConcretBlock#3")
blockInfo7 = act.A_calibrateBlockDistance(robot, "ConcretBlock#7")

while robot: # main Control loop

    simulationTime = World.getSimulationTime()

    for action, duration in actionSequence:

        if action == "forward":
            act.A_moveForward(speed=0.5, duration=duration)

        elif action == "backward":
            act.A_moveBackward(speed=0.5, duration=duration)

        elif action == "turnLeft":
            act.A_turnLeft(speed=0.5, duration=duration)

        elif action == "turnRight":
            act.A_turnRight(speed=0.5, duration=duration)

        elif action == "spin":
            act.A_spin(speed=0.5, duration=duration)

        # Try collecting the nearest block after each movement
        act.A_collectNearestBlock(samplingTime=1000)
