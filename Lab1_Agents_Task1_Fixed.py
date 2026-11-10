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

while robot: # main Control loop

    simulationTime = World.getSimulationTime()

    # initial_pos = act.A_getCurrRobotPosition(robot)

    # act.A_moveForward(speed=0.5, duration=3000)

    # new_pos = act.A_getCurrRobotPosition(robot)

    # actual_distance = math.sqrt(
    #     (new_pos[0] - initial_pos[0])**2 +
    #     (new_pos[1] - initial_pos[1])**2
    # )

    # print("Actual distance:", actual_distance)

    # robot_pos = act.A_getCurrRobotPosition(robot)
    # block_pos = act.A_getBlockPositions(robot, "ConcretBlock#3")

    # print("Robot:", robot_pos)
    # print("First block:", block_pos)
    # dx = abs(block_pos[0] - robot_pos[0])
    # dy = abs(block_pos[1] - robot_pos[1])

    # steps = round((dx + dy) / 0.5)

    # print("Steps to first block:", steps)

    act.A_calibrateBlockDistance(robot, "ConcretBlock#3")

    act.A_calibrateRobot(robot, speed=0.5, durations=(1000, 2000, 3000), targetDistance=1.6615)

    act.A_moveForward(
        speed=0.5,
        duration=27000
    )

    # act.A_turnRight(
    #     speed=2,
    #     duration=1000
    # )

    # act.A_moveForward(
    #     speed=2,
    #     duration=3000
    # )

    # act.A_turnLeft(
    #     speed=2,
    #     duration=1000
    # )

    # Attempt to collect a block
    # act.A_collectNearestBlock(samplingTime=1000)
    act.A_stopMotion(robot)
    act.A_stopExecution()

