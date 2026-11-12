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
import random

# connect to the server
robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))

SPEED_LIMIT = 2.0
DURATION_LIMIT = 500
OBSTACLE_THRESHOLD = 0.3
COLLECTION_DISTANCE = 0.5
TIME_OUT = 100000
MAX_BLOCKS_NUMBER = 12
AVOID_DISTANCE = 0.5  # metres

alternativeActions = [
    ("turnRight", ["ultraLeft"], ["turnRight"]),
    ("turnLeft", ["ultraRight"], ["turnLeft"]),
    ("spin", ["ultraLeft", "ultraRight"], ["spin"]),
    ("backward", ["ultraLeft", "ultraRight"], ["backward"])
]

collectedBlocklst = []
currentBlockIndex = 0
targetStartTime = World.getSimulationTime()

memory = {
    "obstacleHistory": [],
}

def runAndRemObstacleHistory(robot,sensors,actions):
    blockHandle,blockId,distance,direction = World.findEnergyBlocks()[0]
    blockName = 'ConcretBlock#'+str(blockId)
    retcode1, beforePosBlock = act.A_getBlockPositions(robot, blockName)
    retcode2, beforePosRobot = act.A_getCurrRobotPosition(robot)
    startTime = World.getSimulationTime()

    for action in actions:
        if action == "spin":
            act.A_spin(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=startTime)
        elif action == "backward":
            act.A_moveBackward(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=startTime)
        elif action == "turnRight":
            act.A_turnRight(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=startTime)
        elif action == "turnLeft":
            act.A_turnLeft(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=startTime)

    retcode1, afterPosBlock = act.A_getBlockPositions(robot, blockName)
    retcode2, afterPosRobot = act.A_getCurrRobotPosition(robot)
    endTime = World.getSimulationTime()
    # Robot distance traveled during the action
    dx = afterPosRobot[0] - beforePosRobot[0]
    dy = afterPosRobot[1] - beforePosRobot[1]
    robot_distance = math.hypot(dx, dy)
    # Progress towards the block during the action
    before_distance = math.hypot(
        beforePosRobot[0] - beforePosBlock[0],
        beforePosRobot[1] - beforePosBlock[1]
    )
    after_distance = math.hypot(
        afterPosRobot[0] - afterPosBlock[0],
        afterPosRobot[1] - afterPosBlock[1]
    )
    block_progress = before_distance - after_distance

    successful = block_progress > 0.05  # Consider it a success if the block has moved more than 5 cm

    memory["obstacleHistory"].append({
        "sensor": sensors,
        "actions": actions,
        "robot_distance": robot_distance,
        "progress": block_progress,
        "successful": successful,
        "startTime": startTime,
        "endTime": endTime
    })

def getFailedActionCount():
    return sum(
        1 for entry in memory["obstacleHistory"][-3:]
        if not entry["successful"]
    )

def chooseAlternativeAction():
    selectedAction = random.choice(alternativeActions)
    sensors = selectedAction[1]
    actions = selectedAction[2]
    return sensors, actions

def navigation(robot=robot):
    
    if (obstacle["ultraLeft"] < OBSTACLE_THRESHOLD or obstacle["ultraRight"] < OBSTACLE_THRESHOLD): 
        # Obstacle ahead detected
        if getFailedActionCount() >= 2:
            print("Recent actions have been unsuccessful. Considering alternative strategies.")
            # Implement alternative strategies here, e.g., changing the path or avoiding certain areas.
            # For now, we can just log this information.
            sensors, actions = chooseAlternativeAction()
            runAndRemObstacleHistory(robot, sensors, actions)
        else:
            runAndRemObstacleHistory(robot, ["ultraLeft", "ultraRight"], ["spin", "backward"])
        
    elif (obstacle["ultraLeft"] < OBSTACLE_THRESHOLD): # Obstacle on the left detected
        if getFailedActionCount() >= 2:
            print("Recent actions have been unsuccessful. Considering alternative strategies.")
            # Implement alternative strategies here, e.g., changing the path or avoiding certain areas.
            # For now, we can just log this information.
            sensors, actions = chooseAlternativeAction()
            runAndRemObstacleHistory(robot, sensors, actions)
        else:
            runAndRemObstacleHistory(robot, ["ultraLeft"], ["turnRight"])

    elif (obstacle["ultraRight"] < OBSTACLE_THRESHOLD): # Obstacle on the right detected
        if getFailedActionCount() >= 2:
            print("Recent actions have been unsuccessful. Considering alternative strategies.")
            # Implement alternative strategies here, e.g., changing the path or avoiding certain areas.
            # For now, we can just log this information.
            sensors, actions = chooseAlternativeAction()
            runAndRemObstacleHistory(robot, sensors, actions)
        else:
            runAndRemObstacleHistory(robot, ["ultraRight"], ["turnLeft"])



def findBlock(collecting_pf=False):
    if (blockInfo["distance"] < COLLECTION_DISTANCE): # Block is close enough to collect
        act.A_stopMotion(robot)
        return collecting_pf()
    elif (blockInfo["direction"] < 0): # Block is to the left
        act.A_turnLeft(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=0)
    elif (blockInfo["direction"] > 0): # Block is to the right
        act.A_turnRight(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=0)
    elif (blockInfo["direction"] == 0): # Block is straight ahead
        act.A_moveForward(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=0)
    else: # No specific action needed
        act.A_moveForward(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=0)
    return False

while robot:

    simulationTime = World.getSimulationTime()

    obstacle = act.A_UltraSensing(1000, simulationTime)

    blockInfo = act.A_EngergySensingSpecifcBlock(
        1000, simulationTime, currentBlockIndex
    )

    print (f"Current pursuing block index: {currentBlockIndex}")

    elapsedTime = simulationTime - targetStartTime

    navigation(robot)

    if elapsedTime >= TIME_OUT: # Target timeout reached, switch to next block

        print("Target timeout! Switching to next block.")

        # Get nearest block information
        blockInfo = act.A_EngergySensing(1000, simulationTime)

        currBlockHandle,currBlockName,currDistance,currDirection = World.findEnergyBlocks()[0]

        # Try to collect the nearest block
        if findBlock(
            lambda: act.A_collectNearestBlock(samplingTime=100)
        ) is True:
            collectedBlocklst.append(currBlockName)
            print("Nearest block collected!")


        availableBlocks = [
            i for i in range(12)
            if i not in collectedBlocklst
            and i != currentBlockIndex
        ]

        if not availableBlocks:
            print("No more available blocks!")
            break

        currentBlockIndex = random.choice(availableBlocks)

        # IMPORTANT: Reset timer immediately
        targetStartTime = World.getSimulationTime()

        print(f"Switching to block index: {currentBlockIndex}")

    else:

        if findBlock(
            lambda: act.A_collectSpecificBlock(robot, currentBlockIndex)
        ) is True:

            collectedBlocklst.append(currentBlockIndex)

            print("Collected block:", currentBlockIndex)

            availableBlocks = [
                i for i in range(12)
                if i not in collectedBlocklst
            ]

            if not availableBlocks:
                print("All blocks collected!")
                break

            currentBlockIndex = random.choice(availableBlocks)

            targetStartTime = World.getSimulationTime()

            print("Next target:", currentBlockIndex)

    print("Collected blocks:", collectedBlocklst)


    


