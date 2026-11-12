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

SPEED_LIMIT = 2.0
DURATION_LIMIT = 500
OBSTACLE_THRESHOLD = 0.3
COLLECTION_DISTANCE = 0.5
TIME_OUT = 250000
MAX_BLOCKS_NUMBER = 12

currentBlockIndex = 0
targetStartTime = World.getSimulationTime()

def navigation():
    if (obstacle["ultraLeft"] < OBSTACLE_THRESHOLD or obstacle["ultraRight"] < OBSTACLE_THRESHOLD): 
        # Obstacle ahead detected
        act.A_spin(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=0)
        act.A_moveBackward(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=0)
    elif (obstacle["ultraLeft"] < OBSTACLE_THRESHOLD): # Obstacle on the left detected
        act.A_turnRight(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=0)
    elif (obstacle["ultraRight"] < OBSTACLE_THRESHOLD): # Obstacle on the right detected
        act.A_turnLeft(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=0)

def findBlock(collecting_pf=False):
    if (blockInfo["distance"] < COLLECTION_DISTANCE): # Block is close enough to collect
        act.A_stopMotion(robot)
        collecting_pf()
    elif (blockInfo["direction"] < 0): # Block is to the left
        act.A_turnLeft(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=0)
    elif (blockInfo["direction"] > 0): # Block is to the right
        act.A_turnRight(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=0)
    elif (blockInfo["direction"] == 0): # Block is straight ahead
        act.A_moveForward(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=0)
    else: # No specific action needed
        act.A_moveForward(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=0)

while robot: # main Control loop

    simulationTime = World.getSimulationTime()

    obstacle = act.A_UltraSensing(1000, simulationTime)
    blockInfo = act.A_EngergySensing(1000, simulationTime)

    # Check whether the current target has timed out
    elapsedTime = simulationTime - targetStartTime

    navigation()

    if elapsedTime < TIME_OUT:
        findBlock(act.A_collectNearestBlock)

    else:
        print("Target timeout! Switching to next block.")

        if currentBlockIndex < MAX_BLOCKS_NUMBER:
            currentBlockIndex += 1
        else:
            currentBlockIndex = 0

        print(f"Switching to block index: {currentBlockIndex}")

        # Reset timer for the next target
        targetStartTime = World.getSimulationTime()

        findBlock(
            lambda: act.A_collectSpecificBlock(
                robot, currentBlockIndex
            )
        )


    


