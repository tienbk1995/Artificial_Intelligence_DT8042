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

    act.A_stopMotion(robot)
    act.A_stopExecution()
    # print(f"Cycle {count} completed.")
