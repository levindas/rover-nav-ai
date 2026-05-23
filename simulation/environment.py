import pybullet as p
import pybullet_data
import time


def create_simulation():
    """
    Creates a basic PyBullet simulation environment with:
    - A physics server (the engine running everything)
    - A ground plane (so objects don't fall forever)
    - A Husky rover model (our rover)
    - Gravity (like the real world)
    """

    # --- STEP 1: Connect to PyBullet ---
    # This starts the physics engine and opens the 3D window
    # p.GUI means we want a visual window (GUI)
    # p.DIRECT would run it invisibly (for when we don't need to see it)
    physics_client = p.connect(p.GUI)

    # --- STEP 2: Set the data path ---
    # PyBullet comes with built in URDF models (robot descriptions)
    # This line tells PyBullet where to find them on your computer
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    # --- STEP 3: Set gravity ---
    # Real world gravity is 9.8 m/s² downward (negative Z direction)
    # Without this everything would float
    p.setGravity(0, 0, -9.8)

    # --- STEP 4: Load the ground plane ---
    # "plane.urdf" is a built in flat ground surface
    # This stops our rover from falling forever
    ground = p.loadURDF("plane.urdf")

    # --- STEP 5: Load the Husky rover ---
    # "husky/husky.urdf" is a built in 4 wheeled rover model
    # [0, 0, 0.1] is the starting position (x, y, z)
    # We start it slightly above ground (z=0.1) so it doesn't clip into the floor
    rover = p.loadURDF("husky/husky.urdf", [0, 0, 0.1])

    # --- STEP 6: Set up the camera view ---
    # This positions the camera so we get a good view of the rover
    # distance = how far the camera is
    # yaw = horizontal rotation
    # pitch = vertical angle
    # target = what the camera looks at (our rover's position)
    p.resetDebugVisualizerCamera(
        cameraDistance=2.0,
        cameraYaw=45,
        cameraPitch=-30,
        cameraTargetPosition=[0, 0, 0]
    )

    print("✅ Simulation started! Close the window or press Ctrl+C to stop.")

    # --- STEP 7: Run the simulation loop ---
    # This keeps the simulation running and updates physics
    # p.stepSimulation() advances the physics by one tiny time step
    # time.sleep(1/240) runs at 240 steps per second (standard for PyBullet)
    try:
        while True:
            p.stepSimulation()
            time.sleep(1/240)

    except KeyboardInterrupt:
        print("🛑 Simulation stopped.")
        p.disconnect()


if __name__ == "__main__":
    create_simulation()
