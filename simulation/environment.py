import pybullet as p
import pybullet_data
import time

# Wheel joint indices we found from inspect_rover.py
FRONT_LEFT_WHEEL = 2
FRONT_RIGHT_WHEEL = 3
REAR_LEFT_WHEEL = 4
REAR_RIGHT_WHEEL = 5

# All wheel joints together for easy access
ALL_WHEELS = [FRONT_LEFT_WHEEL, FRONT_RIGHT_WHEEL,
              REAR_LEFT_WHEEL, REAR_RIGHT_WHEEL]

# Left side and right side wheels for differential drive steering
LEFT_WHEELS = [FRONT_LEFT_WHEEL, REAR_LEFT_WHEEL]
RIGHT_WHEELS = [FRONT_RIGHT_WHEEL, REAR_RIGHT_WHEEL]


def move_rover(rover, left_speed, right_speed, max_force=10):
    """
    Moves the rover using differential drive.

    left_speed  : speed for left wheels  (positive = forward)
    right_speed : speed for right wheels (positive = forward)
    max_force   : maximum motor force in Newtons

    Examples:
        move_rover(rover,  5,  5)  → move forward
        move_rover(rover, -5, -5)  → move backward
        move_rover(rover,  2,  5)  → turn left
        move_rover(rover,  5,  2)  → turn right
        move_rover(rover, -5,  5)  → spin in place left
        move_rover(rover,  5, -5)  → spin in place right
        move_rover(rover,  0,  0)  → stop
    """

    for wheel in LEFT_WHEELS:
        p.setJointMotorControl2(
            bodyUniqueId=rover,
            jointIndex=wheel,
            controlMode=p.VELOCITY_CONTROL,
            targetVelocity=left_speed,
            force=max_force
        )

    for wheel in RIGHT_WHEELS:
        p.setJointMotorControl2(
            bodyUniqueId=rover,
            jointIndex=wheel,
            controlMode=p.VELOCITY_CONTROL,
            targetVelocity=right_speed,
            force=max_force
        )


def create_obstacles():
    """
    Creates simple box obstacles in the simulation world.
    """
    obstacles = []

    obstacle_positions = [
        [2, 0, 0.5],
        [-2, 1, 0.5],
        [1, 2, 0.5],
        [-1, -2, 0.5],
        [3, 3, 0.5],
    ]

    for position in obstacle_positions:
        collision_shape = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=[0.5, 0.5, 0.5]
        )

        visual_shape = p.createVisualShape(
            p.GEOM_BOX,
            halfExtents=[0.5, 0.5, 0.5],
            rgbaColor=[1, 0, 0, 1]
        )

        obstacle = p.createMultiBody(
            baseMass=0,
            baseCollisionShapeIndex=collision_shape,
            baseVisualShapeIndex=visual_shape,
            basePosition=position
        )

        obstacles.append(obstacle)

    return obstacles


def create_simulation():
    """
    Creates the simulation world and runs a simple movement demo.
    The rover will:
    1. Move forward for 2 seconds
    2. Turn right for 1 second
    3. Move forward for 2 seconds
    4. Stop
    """

    # Connect and set up world
    physics_client = p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.8)

    # Load ground and rover
    ground = p.loadURDF("plane.urdf")
    rover = p.loadURDF("husky/husky.urdf", [0, 0, 0.1])

    # Add obstacles
    obstacles = create_obstacles()
    print(f"✅ Added {len(obstacles)} obstacles")

    # Set up camera
    p.resetDebugVisualizerCamera(
        cameraDistance=6.0,
        cameraYaw=45,
        cameraPitch=-45,
        cameraTargetPosition=[0, 0, 0]
    )

    print("✅ Simulation started!")
    print("📋 Running movement demo...")

    try:
        # --- MOVEMENT DEMO ---
        # Each step runs for a number of simulation steps
        # 240 steps = 1 second (because we run at 240Hz)

        # Phase 1: Move forward for 2 seconds
        print("➡️  Moving forward...")
        for _ in range(240 * 2):
            move_rover(rover, left_speed=5, right_speed=5)
            p.stepSimulation()
            time.sleep(1/240)

        # Phase 2: Turn right for 1 second
        print("↩️  Turning right...")
        for _ in range(240 * 1):
            move_rover(rover, left_speed=5, right_speed=-5)
            p.stepSimulation()
            time.sleep(1/240)

        # Phase 3: Move forward again for 2 seconds
        print("➡️  Moving forward again...")
        for _ in range(240 * 2):
            move_rover(rover, left_speed=5, right_speed=5)
            p.stepSimulation()
            time.sleep(1/240)

        # Phase 4: Stop
        print("🛑 Stopping...")
        move_rover(rover, left_speed=0, right_speed=0)

        # Keep window open so we can see the final position
        print("✅ Demo complete! Close the window or press Ctrl+C to exit.")
        while True:
            p.stepSimulation()
            time.sleep(1/240)

    except KeyboardInterrupt:
        print("🛑 Simulation stopped.")
        p.disconnect()


if __name__ == "__main__":
    create_simulation()
