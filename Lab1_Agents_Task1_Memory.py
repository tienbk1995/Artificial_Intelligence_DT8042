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
TIME_OUT = 50000
MAX_BLOCKS_NUMBER = 12
AVOID_DISTANCE = 0.5  # metres

alternativeActions = [
    ("turnRight", ["ultraLeft"], ["turnRight"]),
    ("turnLeft", ["ultraRight"], ["turnLeft"]),
    ("spin", ["ultraLeft", "ultraRight"], ["spin"]),
    ("backward", ["ultraLeft", "ultraRight"], ["backward"])
]

currentBlockIndex = 0
targetStartTime = World.getSimulationTime()

memory = {
    "obstacleHistory": [],
}

def rememberObstaclePosition(robot,sensors,actions):
    blockHandle,blockName,distance,direction = World.findEnergyBlocks()[0]
    blockName = 'ConcretBlock#'+str(blockName)
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

    retCode, robotPosition = act.A_getCurrRobotPosition(robot)
    
    if (obstacle["ultraLeft"] < OBSTACLE_THRESHOLD or obstacle["ultraRight"] < OBSTACLE_THRESHOLD): 
        # Obstacle ahead detected
        if getFailedActionCount() >= 2:
            print("Recent actions have been unsuccessful. Considering alternative strategies.")
            # Implement alternative strategies here, e.g., changing the path or avoiding certain areas.
            # For now, we can just log this information.
            sensors, actions = chooseAlternativeAction()
            rememberObstaclePosition(robot, sensors, actions)
        else:
            rememberObstaclePosition(robot, ["ultraLeft", "ultraRight"], ["spin", "backward"])
        
    elif (obstacle["ultraLeft"] < OBSTACLE_THRESHOLD): # Obstacle on the left detected
        if getFailedActionCount() >= 2:
            print("Recent actions have been unsuccessful. Considering alternative strategies.")
            # Implement alternative strategies here, e.g., changing the path or avoiding certain areas.
            # For now, we can just log this information.
            sensors, actions = chooseAlternativeAction()
            rememberObstaclePosition(robot, sensors, actions)
        else:
            rememberObstaclePosition(robot, ["ultraLeft"], ["turnRight"])

    elif (obstacle["ultraRight"] < OBSTACLE_THRESHOLD): # Obstacle on the right detected
        if getFailedActionCount() >= 2:
            print("Recent actions have been unsuccessful. Considering alternative strategies.")
            # Implement alternative strategies here, e.g., changing the path or avoiding certain areas.
            # For now, we can just log this information.
            sensors, actions = chooseAlternativeAction()
            rememberObstaclePosition(robot, sensors, actions)
        else:
            rememberObstaclePosition(robot, ["ultraRight"], ["turnLeft"])


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

    navigation(robot)

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
    # time.sleep(0.1)  # Add a small delay to avoid overwhelming the simulation
    print(f"memory: {memory}")


    


