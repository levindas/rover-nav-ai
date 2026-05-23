import pybullet as p
import pybullet_data

# Start PyBullet silently (no window needed - just inspecting)
p.connect(p.DIRECT)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Load the rover
rover = p.loadURDF("husky/husky.urdf", [0, 0, 0.1])

# Print all joints
print(f"\n🔍 Husky rover has {p.getNumJoints(rover)} joints:\n")

for i in range(p.getNumJoints(rover)):
    joint_info = p.getJointInfo(rover, i)
    joint_index = joint_info[0]
    joint_name = joint_info[1].decode("utf-8")  # convert bytes to string
    joint_type = joint_info[2]

    # Joint types: 0=Revolute, 1=Prismatic, 4=Fixed
    type_name = {0: "Revolute", 1: "Prismatic",
                 4: "Fixed"}.get(joint_type, "Other")

    print(f"  Joint {joint_index}: {joint_name} ({type_name})")

p.disconnect()
