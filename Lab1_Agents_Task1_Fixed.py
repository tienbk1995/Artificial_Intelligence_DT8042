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

blockInfo3 = act.A_calibrateBlockDistance(robot, "ConcretBlock#3")
blockInfo7 = act.A_calibrateBlockDistance(robot, "ConcretBlock#7")

count = 0
while robot: # main Control loop

    simulationTime = World.getSimulationTime()

    calibrated_speed3, estimated_duration3 = act.A_calibrateRobot(
        robot, 
        speed=0.5, 
        durations=(1000, 2000, 3000), 
        targetDistance=blockInfo3["distance"])
    print(f"total_time3: {estimated_duration3} ms")

    act.A_moveForward(
        speed=0.5,
        duration=estimated_duration3
    )
    # count += 1
    # # Attempt to collect a block
    act.A_collectNearestBlock(samplingTime=1000)

    act.A_stopMotion(robot)

    calibrated_speed7, estimated_duration7 = act.A_calibrateRobot(
        robot, 
        speed=0.5, 
        durations=(1000, 2000, 3000), 
        targetDistance=blockInfo7["distance"])
    print(f"total_time7: {estimated_duration7} ms")

    act.A_moveForward(
        speed=0.5,
        duration=estimated_duration3
    )

    act.A_turnLeft(
        speed=0.5,
        duration=1000
    )

    act.A_collectNearestBlock(samplingTime=1000)

    act.A_stopMotion(robot)
    act.A_stopExecution()
    # print(f"Cycle {count} completed.")
