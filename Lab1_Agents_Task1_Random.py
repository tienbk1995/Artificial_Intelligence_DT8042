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

# connect to the server
robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))

while robot: # main Control loop
    # Perception Phase: Get information about environment #
    #####################################################
    simulationTime = World.getSimulationTime()
    ##############################################
    # Reasoning: figure out which action to take #
    ##############################################
    act.A_moveForward(speed=2, duration=15000, clockTime=-1, startTime=0)
    act.A_moveBackward(speed=1, duration=15000, clockTime=-1, startTime=20000)
    act.A_spin(speed=2, duration=5000, clockTime=-1, startTime=25000)
    # try to collect energy block (will fail if not within range)
    act.A_collectNearestBlock(samplingTime=1000)
    act.A_stopMotion()
    ########################################
    # Action Phase: Assign speed to wheels #
    ########################################
    # assign speed to the wheels
    act.A_stopExecution()
