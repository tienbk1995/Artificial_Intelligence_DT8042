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
TIME_OUT = 200000
MAX_BLOCKS_NUMBER = 12
AVOID_DISTANCE = 0.5  # metres

# Alternative actions to try when the robot is stuck
alternativeActions = [
    ("turnRight", ["ultraLeft"], ["turnRight"]),
    ("turnLeft", ["ultraRight"], ["turnLeft"]),
    ("spin", ["ultraLeft", "ultraRight"], ["spin"]),
    ("backward", ["ultraLeft", "ultraRight"], ["backward"])
]

# Get the current closest block index
def getCurrentClosestBlockIndex():
    blockInfo = act.A_EngergySensing(1000, World.getSimulationTime())
    blockHandle, blockId, distance, direction = World.findEnergyBlocks()[0]
    return blockInfo, blockId

# Initialize global variables
collectedBlocklst = []
targetStartTime = World.getSimulationTime()
currentBlockInfo, currentBlockIndex = getCurrentClosestBlockIndex() # Get initial closest block index
# currentBlockIndex = 0
memory = {
    "obstacleHistory": [],
}

# Run an action and remember the outcome in memory
def runAndRemObstacleHistory(robot,sensors,actions):
    # Get the current closest block index
    blockHandle,blockId,distance,direction = World.findEnergyBlocks()[0]
    blockName = 'ConcretBlock#'+str(blockId)
    retcode1, beforePosBlock = act.A_getBlockPositions(robot, blockName)
    retcode2, beforePosRobot = act.A_getCurrRobotPosition(robot)

    # Execute the actions
    startTime = World.getSimulationTime()

    # Execute the actions
    for action in actions:
        if action == "spin":
            act.A_spin(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=startTime)
        elif action == "backward":
            act.A_moveBackward(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=startTime)
        elif action == "turnRight":
            act.A_turnRight(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=startTime)
        elif action == "turnLeft":
            act.A_turnLeft(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=startTime)

    # After executing the actions, check the new positions of the robot and the block
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

    # Memory structure to store the outcome of the action
    memory["obstacleHistory"].append({
        "sensor": sensors,
        "actions": actions,
        "robot_distance": robot_distance,
        "progress": block_progress,
        "successful": successful,
        "startTime": startTime,
        "endTime": endTime
    })

# Get the count of failed actions in the last 3 attempts
def getFailedActionCount():
    return sum(
        1 for entry in memory["obstacleHistory"][-3:]
        if not entry["successful"]
    )

# choose an alternative action based on the robot's memory and current situation
# actions are chosen randomly from the predefined alternativeActions list
def chooseAlternativeAction():
    selectedAction = random.choice(alternativeActions)
    sensors = selectedAction[1]
    actions = selectedAction[2]
    return sensors, actions

# Navigation function to handle obstacle avoidance based on sensor readings and robot's memory
def navigation(robot=robot):
    
    if (obstacle["ultraLeft"] < OBSTACLE_THRESHOLD or obstacle["ultraRight"] < OBSTACLE_THRESHOLD): 
        # Obstacle ahead detected
        if getFailedActionCount() >= 2:
            print("Recent actions have been unsuccessful. Considering alternative strategies.")
            # Implement alternative strategies here by choosing an alternative action based on the robot's memory and current situation
            sensors, actions = chooseAlternativeAction()
            # Execute the alternative action and remember the outcome
            runAndRemObstacleHistory(robot, sensors, actions)
        else:
            # Execute the default obstacle avoidance strategy and remember the outcome
            runAndRemObstacleHistory(robot, ["ultraLeft", "ultraRight"], ["spin", "backward"])
        
    elif (obstacle["ultraLeft"] < OBSTACLE_THRESHOLD): # Obstacle on the left detected
        if getFailedActionCount() >= 2:
            print("Recent actions have been unsuccessful. Considering alternative strategies.")
            # Implement alternative strategies here by choosing an alternative action based on the robot's memory and current situation
            sensors, actions = chooseAlternativeAction()
            # Execute the alternative action and remember the outcome
            runAndRemObstacleHistory(robot, sensors, actions)
        else:
            # Execute the default obstacle avoidance strategy and remember the outcome
            runAndRemObstacleHistory(robot, ["ultraLeft"], ["turnRight"])

    elif (obstacle["ultraRight"] < OBSTACLE_THRESHOLD): # Obstacle on the right detected
        if getFailedActionCount() >= 2:
            print("Recent actions have been unsuccessful. Considering alternative strategies.")
            # Implement alternative strategies here, e.g., changing the path or avoiding certain areas.
            # For now, we can just log this information.
            sensors, actions = chooseAlternativeAction()
            # Execute the alternative action and remember the outcome
            runAndRemObstacleHistory(robot, sensors, actions)
        else:
            # Execute the default obstacle avoidance strategy and remember the outcome
            runAndRemObstacleHistory(robot, ["ultraRight"], ["turnLeft"])

# Nagivation function towards the block based on its direction and distance
def findBlock(blockInfo, collecting_pf=False):
    if (blockInfo["distance"] < COLLECTION_DISTANCE): # Block is close enough to collect
        act.A_stopMotion(robot)
        return collecting_pf() #call the collecting function passed as an argument
    elif (blockInfo["direction"] < 0): # Block is to the left
        act.A_turnLeft(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=0)
    elif (blockInfo["direction"] > 0): # Block is to the right
        act.A_turnRight(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=0)
    elif (blockInfo["direction"] == 0): # Block is straight ahead
        act.A_moveForward(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=0)
    else: # No specific action needed
        act.A_moveForward(speed=SPEED_LIMIT, duration=DURATION_LIMIT, clockTime=-1, startTime=0)
    return False

# Main control loop for the robot's operation
while robot:
    # Get the current simulation time
    simulationTime = World.getSimulationTime()

    # Get the current obstacle readings from the robot's sensors
    obstacle = act.A_UltraSensing(1000, simulationTime)

    # Get the current block information based on the current block index
    currentBlockInfo = act.A_EngergySensingSpecificBlock(currentBlockIndex)
    
    print (f"Current block info: {currentBlockInfo}")

    print (f"Current pursuing block index: {currentBlockIndex}")

    # Time elapsed since the robot started pursuing the current block
    elapsedTime = simulationTime - targetStartTime

    # Start navigation towards the block while avoiding obstacles
    navigation(robot)

    # If the robot has been pursuing the block exceeding the time limit, switch to the next block
    if elapsedTime >= TIME_OUT: # Target timeout reached, switch to next block

        print("Target timeout! Switching to next block.")

        # Get nearest block information
        currentBlockInfo, currentClosestBlockIndex = getCurrentClosestBlockIndex()

        # Try to collect the nearest block
        if findBlock(
            currentBlockInfo,
            lambda: act.A_collectNearestBlock(samplingTime=100)
        ) is True:
            collectedBlocklst.append(currentClosestBlockIndex)
            print("Nearest block collected!")

        # Update the list of available blocks, excluding already collected ones and the current block
        availableBlocks = [
            i for i in range(12)
            if i not in collectedBlocklst
            and i != currentBlockIndex
        ]

        # If there are no more available blocks, print a message and break the loop
        if not availableBlocks:
            print("No more available blocks!")
            break

        # Change the current block index to a random available block
        currentBlockIndex = random.choice(availableBlocks)

        # Reset timer immediately
        targetStartTime = World.getSimulationTime()

        # Print the new target block index
        print(f"Switching to block index: {currentBlockIndex}")

    else: # Continue pursuing the current block
        # Try to collect the specific block

        if findBlock(currentBlockInfo,
            lambda: act.A_collectSpecificBlock(robot, currentBlockIndex)
        ) is True:

            collectedBlocklst.append(currentBlockIndex)

            print("Collected block:", currentBlockIndex)

            # Update the list of available blocks, excluding already collected ones
            availableBlocks = [
                i for i in range(12)
                if i not in collectedBlocklst
            ]

            # If there are no more available blocks, print a message and break the loop
            if not availableBlocks:
                print("All blocks collected!")
                break

            # Change the current block index to a random available block
            currentBlockIndex = random.choice(availableBlocks)

            # Reset timer immediately
            targetStartTime = World.getSimulationTime()

            print("Next target:", currentBlockIndex)

    print("Collected blocks:", collectedBlocklst)


    


