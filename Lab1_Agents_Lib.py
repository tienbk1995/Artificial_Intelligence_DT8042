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

def A_EngergySensing(interval, realtime):
    data = World.getSensorReading("energySensor")
    if realtime % interval == 0 or realtime == 0:
        print ('Time:',realtime,\
               'distance:',data.distance, 'direction:', data.direction)
    return {"distance": data.distance, "direction": data.direction}

def A_moveForward(speed=1, duration=5000, clockTime=-1, startTime=1000):
    while (World.getSimulationTime() < startTime):
        time.sleep(0.005) # Wait until the specified start time
    print("Starting to move forward with speed", speed, "for", duration, "ms.")
    World.execute(dict(speedLeft=speed, speedRight=speed),duration,clockTime)   

def A_moveBackward(speed=1, duration=5000, clockTime=-1, startTime=1000):
    while (World.getSimulationTime() < startTime):
        time.sleep(0.005) # Wait until the specified start time
    print("Starting to move backward with speed", speed, "for", duration, "ms.")
    World.execute(dict(speedLeft=-speed, speedRight=-speed),duration,clockTime)

def A_turnLeft(speed=1, duration=5000, clockTime=-1, startTime=1000):
    while (World.getSimulationTime() < startTime):
        time.sleep(0.005) # Wait until the specified start time
    print("Starting to turn left with speed", speed, "for", duration, "ms.")
    World.execute(dict(speedLeft=speed, speedRight=speed+0.5),duration,clockTime)

def A_turnRight(speed=1, duration=5000, clockTime=-1, startTime=1000):
    while (World.getSimulationTime() < startTime):
        time.sleep(0.005) # Wait until the specified start time
    print("Starting to turn right with speed", speed, "for", duration, "ms.")
    World.execute(dict(speedLeft=speed+0.5, speedRight=speed),duration,clockTime)

def A_spin(speed=1, duration=5000, clockTime=-1, startTime=1000):
    while (World.getSimulationTime() < startTime):
        time.sleep(0.005) # Wait until the specified start time
    print("Starting to spin with speed", speed, "for", duration, "ms.")
    World.execute(dict(speedLeft=speed, speedRight=-speed),duration,clockTime)

def A_collectNearestBlock(samplingTime=1000):
    currentTime = World.getSimulationTime()
    if not hasattr(A_collectNearestBlock, "nextSamplingTime"):
        A_collectNearestBlock.nextSamplingTime = currentTime
    if currentTime >= A_collectNearestBlock.nextSamplingTime:
        print("Trying to collect a block...")
        print(World.collectNearestBlock())
        A_collectNearestBlock.nextSamplingTime += samplingTime

def A_stopMotion(robot):
    World.STOP()
    # Wait for the simulator to process the command
    vrep.simxGetPingTime(robot.clientID)
    print("Stop command sent and acknowledged.")

def A_stopExecution():
    print("Stopping execution and exiting the program.")
    sys.exit(0)

def A_getCurrRobotPosition(robot):
    retCode, robotPos = vrep.simxGetObjectPosition(robot.clientID, robot.pioneerRobotHandle, -1, vrep.simx_opmode_oneshot_wait)
    return retCode, robotPos

def A_getBlockPositions(robot, blockName): # blockName is a string, e.g., "ConcretBlock#3"
    retCode, handle = vrep.simxGetObjectHandle(robot.clientID, blockName, vrep.simx_opmode_oneshot_wait)
    retCode, position = vrep.simxGetObjectPosition(robot.clientID, handle, -1, vrep.simx_opmode_oneshot_wait)
    return retCode, position

def A_calculateRobotSpeed(robot, samplingTime=100):

    currentTime = World.getSimulationTime()
    retCode, currentPos = A_getCurrRobotPosition(robot)

    # Initialize previous measurements
    if not hasattr(A_calculateRobotSpeed, "prevTime"):
        A_calculateRobotSpeed.prevTime = currentTime
        A_calculateRobotSpeed.prevPos = currentPos
        return None

    elapsedTime = (currentTime - A_calculateRobotSpeed.prevTime) / 1000.0

    # Wait for the next sampling interval
    if elapsedTime < samplingTime / 1000.0:
        return None

    previousPos = A_calculateRobotSpeed.prevPos

    dx = currentPos[0] - previousPos[0]
    dy = currentPos[1] - previousPos[1]

    vx = dx / elapsedTime
    vy = dy / elapsedTime

    speed = math.sqrt(vx**2 + vy**2)

    # Update previous measurements
    A_calculateRobotSpeed.prevTime = currentTime
    A_calculateRobotSpeed.prevPos = currentPos

    return {
        "vx": vx,
        "vy": vy,
        "speed": speed
    }


def A_calibrateRobot(
    robot,
    speed=0.5,
    durations=(1000, 2000, 3000),
    targetDistance=0.5
):
    """
    Measure the robot's actual movement speed for different durations.

    The robot must face a clear, straight path.

    Returns:
        calibrated_speed: Measured average speed in m/s.
        results: List containing individual calibration measurements.
    """

    results = []

    print("\n========== ROBOT CALIBRATION ==========")
    print(f"Motor speed: {speed}")
    print(f"Target distance: {targetDistance:.4f} m")

    for duration in durations:

        # Record initial robot position and simulation time
        retCode, initial_pos = A_getCurrRobotPosition(robot)

        if retCode != vrep.simx_return_ok:
            print("Error retrieving initial robot position.")
            continue

        initial_time = World.getSimulationTime()

        # Execute forward movement
        A_moveForward(
            speed=speed,
            duration=duration,
            startTime=0
        )

        # Record final robot position and simulation time
        retCode, final_pos = A_getCurrRobotPosition(robot)
        final_time = World.getSimulationTime()

        if retCode != vrep.simx_return_ok:
            print("Error retrieving final robot position.")
            continue

        # Calculate displacement in the XY plane
        dx = final_pos[0] - initial_pos[0]
        dy = final_pos[1] - initial_pos[1]

        distance = math.hypot(dx, dy)

        # Calculate actual simulation elapsed time
        elapsed_time = (final_time - initial_time) / 1000.0

        if elapsed_time <= 0:
            print("Invalid elapsed time. Skipping measurement.")
            continue

        # Calculate average speed
        actual_speed = distance / elapsed_time

        # Calculate distance error
        distance_error = distance - targetDistance

        # Store measurement results
        results.append({
            "duration": duration,
            "elapsed_time": elapsed_time,
            "distance": distance,
            "speed": actual_speed,
            "error": distance_error
        })

        print(f"\nCommand duration: {duration} ms")
        print(f"Actual elapsed time: {elapsed_time:.3f} s")
        print(f"Distance travelled: {distance:.4f} m")
        print(f"Average speed: {actual_speed:.5f} m/s")
        print(f"Distance error: {distance_error:.4f} m")

    # Check whether any valid measurements were collected
    if not results:
        print("\nCalibration failed: no valid measurements.")
        return 0, results

    # Calculate weighted average speed
    total_distance = sum(r["distance"] for r in results)
    total_time = sum(r["elapsed_time"] for r in results)

    if total_time <= 0:
        print("\nCalibration failed: invalid total elapsed time.")
        return 0, results

    calibrated_speed = total_distance / total_time

    # Estimate duration required to travel the target distance
    estimated_duration = (targetDistance / calibrated_speed) * 1000

    print("\n========== CALIBRATION RESULT ==========")
    print(f"Calibrated speed: {calibrated_speed:.5f} m/s")
    print(f"Target distance: {targetDistance:.4f} m")
    print(f"Estimated duration: {estimated_duration:.0f} ms")

    return calibrated_speed, results


def A_calibrateBlockDistance(robot, blockHandle, gridSize=0.5):

    # Get robot's current position
    retCode, robotPos = A_getCurrRobotPosition(robot)

    # Get block's current world position
    retCode, blockPos =A_getBlockPositions(robot, blockHandle)

    if retCode != vrep.simx_return_ok:
        print("Error retrieving block position:", retCode)
        return None

    # Calculate coordinate differences
    dx = blockPos[0] - robotPos[0]
    dy = blockPos[1] - robotPos[1]

    # Euclidean distance
    distance = math.hypot(dx, dy)

    # Manhattan distance in grid steps
    horizontalSteps = round(abs(dx) / gridSize)
    verticalSteps = round(abs(dy) / gridSize)

    totalSteps = horizontalSteps + verticalSteps

    print("\n========== BLOCK DISTANCE ==========")
    print("Robot position:", robotPos)
    print("Block position:", blockPos)
    print("Horizontal difference:", round(dx, 4), "m")
    print("Vertical difference:", round(dy, 4), "m")
    print("Euclidean distance:", round(distance, 4), "m")
    print("Horizontal steps:", horizontalSteps)
    print("Vertical steps:", verticalSteps)
    print("Total grid steps:", totalSteps)

    return {
        "distance": distance,
        "horizontalSteps": horizontalSteps,
        "verticalSteps": verticalSteps,
        "totalSteps": totalSteps,
        "blockPosition": blockPos
    }