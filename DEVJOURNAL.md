# 🗒️ Dev Journal — Rover Navigation AI

---

## 🗺️ Architecture Decisions & Upgrade Path

### Current Version — Simplified Autonomous System
- 2D Occupancy Grid mapping (not full 3D)
- Partial SLAM — rover builds map as it explores
- A* path planning on partial map with replanning
- Flat terrain with box obstacles
- YOLOv8 camera based perception

### Future Version — Full Autonomous System
- 3D Point Cloud mapping
- Full SLAM (Simultaneous Localization and Mapping)
- Dynamic replanning with full SLAM integration
- Heightmap based 3D terrain
- LiDAR + Depth camera perception

### Why this progression?
Started simple to get a working end to end system first.
Each component is designed to be swappable — upgrading one
part doesn't break the rest. This is called modular architecture
and is standard practice in real robotics systems.

---

## Entry 1 — Project Setup & Planning

### What I Built
Set up the full project foundation — folder structure, virtual environment,
Git repository, GitHub remote, README and this journal.

### Why This Way

**Virtual Environment (`venv`)**
Keeps all the libraries we install for this project separate from system 
Python. This means if we install something here it won't affect other 
projects and vice versa. Standard practice in every Python project.

**Folder Structure**
Separated the project into components (perception, mapping, planning, 
simulation) from day one. This way as the project grows each part stays 
in its place and doesn't become a mess.

**Git + GitHub**
Git tracks every change we make locally. GitHub is the remote backup and 
portfolio piece. We commit at each meaningful step so the history tells 
the story of how the project was built.

**README**
The front page of the project. Written early so the project looks 
professional from day one. Will be updated as we add features.

### What I Learned
- PowerShell uses `New-Item` instead of `echo.` to create files
- `mkdir` in PowerShell doesn't accept multiple folder names at once
- Git does not track empty folders — only files get committed
- `.gitignore` itself is tracked by Git — it's not secret, just a config file
- `git init` creates a hidden `.git` folder which is the local repository
- `git add` = staging (putting files in a box)
- `git commit` = saving the snapshot (sealing the box with a label)  
- `git push` = sending it to GitHub (shipping the box)
- `git remote add origin` only needs to be run once — the link is saved permanently
- Branches let you work on features separately without touching `main`

### Tools Introduced
| Tool | Purpose |
|---|---|
| Python venv | Isolated project environment |
| Git | Local version control |
| GitHub | Remote repository + portfolio |
| PowerShell | Windows terminal inside VS Code |

### Key Concepts
**PyBullet** — A Python physics simulation library. It creates a virtual 
3D world where our rover can move, collide with objects and be tested 
before real hardware exists. Used by Google DeepMind and OpenAI for 
robotics research. Three layers: physics engine, the world, simulation loop.

---

## Entry 2 — PyBullet Simulation Environment

### What I Built
A basic 3D simulation world using PyBullet with a ground plane and a
Husky rover model loaded into it.

### Why This Way

**Simulation before AI components**
We need a world for the AI to live in first. Just like a video game —
you build the world before adding characters and logic. Without a
simulation we'd have no way to see, test or run anything we build.

**Husky URDF**
URDF (Unified Robot Description Format) is an XML file that describes
a robot's appearance, how its parts connect, and its physical properties.
PyBullet comes with built in URDF models — Husky is a real 4 wheeled
rover made by Clearpath Robotics. Perfect for our use case.

**240 steps per second**
PyBullet's simulation loop runs at 240 Hz (steps per second). This is
the standard rate for stable physics simulation — fast enough to be
accurate, not so fast it overloads the CPU.

**p.GUI vs p.DIRECT**
p.GUI opens a visible 3D window. p.DIRECT runs the simulation invisibly
in the background — useful later when we're running automated tests and
don't need to see the window.

### What I Learned
- PyBullet is just a Python library — no separate app to install
- It uses OpenGL to render the 3D window (same technology as video games)
- URDF files describe robots — shape, joints, weight, friction etc.
- Gravity has to be set manually in PyBullet — nothing is assumed
- The simulation loop steps physics forward continuously to keep it alive
- p.setAdditionalSearchPath tells PyBullet where to find built in models

### Tools Introduced
| Tool | Purpose |
|---|---|
| PyBullet | Physics simulation engine |
| pybullet_data | Built in URDF models that come with PyBullet |
| URDF | File format for describing robots |
| OpenGL | Graphics rendering (used internally by PyBullet) |

---

## Entry 3 — Adding Simple Obstacles to the Simulation

### What I Built
Added 5 static red box obstacles scattered around the rover in the
simulation world.

### Why This Way

**Why obstacles are needed**
Without obstacles there is no navigation problem to solve. The rover
needs things to detect, map and avoid. Obstacles are what make the
whole AI system necessary.

**Two shapes per obstacle**
Every object in PyBullet needs two shapes:
- Collision shape — used by the physics engine to detect collisions
- Visual shape — purely what we see in the window
They look the same but serve completely different purposes.

**mass=0 means static**
Setting mass to 0 makes an object static — fixed in place, unmovable.
If mass was greater than 0 the rover could push the boxes around.
Static obstacles are more realistic for walls, rocks, and terrain features.

**Simple boxes first**
Started with simple box shapes before complex terrain. This is standard
practice in robotics — get the system working simply first, then make
it realistic. We'll upgrade to heightmap terrain later.

### What I Learned
- PyBullet shapes need both a collision shape and a visual shape
- rgbaColor = [Red, Green, Blue, Alpha] — values between 0 and 1
- halfExtents means half the size on each axis — so [0.5,0.5,0.5] = 1x1x1m box
- mass=0 makes objects static (unmovable)
- Obstacle positions are set as [x, y, z] coordinates in meters

### Tools Introduced
| Tool | Purpose |
|---|---|
| createCollisionShape | Defines physics boundary of an object |
| createVisualShape | Defines visual appearance of an object |
| createMultiBody | Combines shapes into a physical object in the world |

---

## Entry 4 — Rover Movement (Differential Drive)

### What I Built
Added movement control to the rover using differential drive. The rover
can now move forward, backward, turn, and spin in place by controlling
wheel speeds independently.

### Why This Way

**Velocity Control**
We control wheels by setting their target spin speed using
setJointMotorControl2. This mimics how real motor controllers work —
you tell the motor what speed to run at and it applies the necessary
force to get there.

**Differential Drive**
The Husky uses differential drive — the same way a tank steers.
No steering wheel. Instead the difference in speed between left and
right wheels determines direction. Equal speeds = straight.
Opposite speeds = spin in place. This is the most common drive
system for ground rovers.

**240 steps = 1 second**
The simulation runs at 240Hz. So to run something for 2 seconds
we loop 240 × 2 = 480 times. This is how we control timing
precisely in simulation.

**Joint indices**
We found the wheel joints by inspecting the URDF with inspect_rover.py.
Joints 2,3,4,5 are the four wheels. Fixed joints (body, bumpers, plates)
cannot be controlled — only Revolute joints can spin.

### What I Learned
- setJointMotorControl2 controls individual joints (motors)
- VELOCITY_CONTROL mode sets target spin speed
- Positive velocity = forward, negative = backward
- Differential drive steers by speed difference between left and right
- 240 simulation steps = 1 real second at 240Hz
- Fixed joints connect parts rigidly — they cannot move
- Revolute joints rotate around an axis — these are our wheels

### Tools Introduced
| Tool | Purpose |
|---|---|
| setJointMotorControl2 | Controls joint motors in PyBullet |
| VELOCITY_CONTROL | Control mode for setting wheel speed |
| Differential Drive | Steering system using wheel speed differences |

---

## Entry 5 — Perception (Giving the Rover Eyes)

### What I Built
A perception pipeline that captures images from a virtual camera
mounted on the rover and detects red obstacles using OpenCV color
detection.

### Why This Way

**Virtual camera in PyBullet**
PyBullet can render images from any point in the simulation world.
We place a virtual camera on the rover so we get exactly what the
rover would see — not our outside observer view. This is how real
robots work — they only know what their sensors tell them.

**RGBA to BGR conversion**
PyBullet outputs images in RGBA format (4 channels including
transparency). OpenCV works in BGR format (3 channels). We convert
between them using cv2.cvtColor so OpenCV can process the image.

**Why HSV over RGB for color detection**
HSV separates the actual color (Hue) from brightness (Value).
A red box in shadow and a red box in bright light have very different
RGB values but similar HSV hue values. This makes detection much
more reliable across different lighting conditions.

**Why red wraps around in HSV**
Red is special in HSV — it appears at both ends of the hue spectrum
(0-10 and 160-180). So we need two masks and combine them with
bitwise_or to catch all red pixels.

**Contours**
After creating the mask we use findContours to trace the outlines
of white regions. Each contour = one detected obstacle. We filter
out tiny contours (under 500px area) to ignore noise.

**Morphological operations**
MORPH_OPEN removes small noisy spots from the mask.
MORPH_CLOSE fills small holes inside detected regions.
These clean up the mask before we find contours.

### What I Learned
- PyBullet can render images from any camera position in the world
- computeViewMatrix defines where the camera is and what it looks at
- computeProjectionMatrixFOV defines the camera lens properties
- Images are just numpy arrays — rows and columns of pixel values
- HSV is better than RGB for color detection
- Red wraps around the HSV hue spectrum — needs two ranges
- A mask is a black and white image — white = color match
- Contours are outlines of regions in a mask
- cv2.boundingRect gives us x, y, width, height of a detection

### Upgrade Note
Currently using OpenCV color detection for red boxes in simulation.
When upgrading to real hardware swap this for YOLOv8 running on
real camera feed for proper object detection on real world objects.

### Tools Introduced
| Tool | Purpose |
|---|---|
| cv2.cvtColor | Convert between color spaces |
| cv2.inRange | Create a mask for a color range |
| cv2.findContours | Find outlines of regions in a mask |
| cv2.boundingRect | Get bounding box of a contour |
| cv2.morphologyEx | Clean up masks using morphological operations |
| p.getCameraImage | Capture image from PyBullet virtual camera |
| p.computeViewMatrix | Define camera position and direction |
| p.computeProjectionMatrixFOV | Define camera lens properties |