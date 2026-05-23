import pybullet as p
import pybullet_data
import time


def create_obstacles():
    """
    Creates simple box obstacles in the simulation world.
    Each obstacle needs two things:
    1. A collision shape - what the physics engine uses for collisions
    2. A visual shape - what we actually see in the window
    Then we combine them into a single body and place it in the world.
    """

    obstacles = []

    # Define obstacle positions [x, y, z]
    # We place them at different spots around the rover (which is at 0,0)
    obstacle_positions = [
        [2, 0, 0.5],    # directly in front
        [-2, 1, 0.5],   # behind and to the side
        [1, 2, 0.5],    # to the right
        [-1, -2, 0.5],  # to the left
        [3, 3, 0.5],    # far corner
    ]

    for position in obstacle_positions:

        # STEP 1: Create the collision shape
        # This is what the physics engine uses to detect collisions
        # halfExtents means half the size on each side
        # so [0.5, 0.5, 0.5] creates a 1x1x1 meter box
        collision_shape = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=[0.5, 0.5, 0.5]
        )

        # STEP 2: Create the visual shape
        # This is purely what we see - color, appearance
        # rgbaColor = [Red, Green, Blue, Alpha(opacity)]
        # [1, 0, 0, 1] = solid red
        visual_shape = p.createVisualShape(
            p.GEOM_BOX,
            halfExtents=[0.5, 0.5, 0.5],
            rgbaColor=[1, 0, 0, 1]
        )

        # STEP 3: Combine into a body and place it in the world
        # mass=0 means the obstacle is STATIC - it won't move when hit
        # if mass was > 0 the rover could push it around
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
    Creates a basic PyBullet simulation environment with:
    - A physics server (the engine running everything)
    - A ground plane (so objects don't fall forever)
    - A Husky rover model (our rover)
    - Gravity (like the real world)
    - Obstacles (things to navigate around)
    """

    # Connect to PyBullet and open the 3D window
    physics_client = p.connect(p.GUI)

    # Tell PyBullet where to find its built in URDF models
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    # Set gravity - real world is 9.8 m/s² downward
    p.setGravity(0, 0, -9.8)

    # Load the ground plane
    ground = p.loadURDF("plane.urdf")

    # Load the Husky rover slightly above ground
    rover = p.loadURDF("husky/husky.urdf", [0, 0, 0.1])

    # Add obstacles to the world
    obstacles = create_obstacles()
    print(f"✅ Added {len(obstacles)} obstacles to the world")

    # Position the camera for a good top-down-ish view
    p.resetDebugVisualizerCamera(
        cameraDistance=6.0,
        cameraYaw=45,
        cameraPitch=-45,
        cameraTargetPosition=[0, 0, 0]
    )

    print("✅ Simulation started! Close the window or press Ctrl+C to stop.")

    # Run the simulation loop
    try:
        while True:
            p.stepSimulation()
            time.sleep(1/240)

    except KeyboardInterrupt:
        print("🛑 Simulation stopped.")
        p.disconnect()


if __name__ == "__main__":
    create_simulation()
