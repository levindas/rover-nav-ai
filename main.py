import pybullet as p
import pybullet_data
import time
from perception.detector import run_perception_demo


def main():
    # Set up simulation
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.8)

    # Load world
    p.loadURDF("plane.urdf")
    rover = p.loadURDF("husky/husky.urdf", [0, 0, 0.1])

    # Add a red obstacle directly in front of rover
    collision_shape = p.createCollisionShape(
        p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.5])
    visual_shape = p.createVisualShape(
        p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.5], rgbaColor=[1, 0, 0, 1])
    p.createMultiBody(0, collision_shape, visual_shape, [2, 0, 0.5])

    # Set camera view
    p.resetDebugVisualizerCamera(6.0, 45, -45, [0, 0, 0])

    # Step simulation a few times to let everything settle
    for _ in range(100):
        p.stepSimulation()
        time.sleep(1/240)

    # Run perception demo
    run_perception_demo(rover)

    p.disconnect()


if __name__ == "__main__":
    main()
