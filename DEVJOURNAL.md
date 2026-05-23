# 🗒️ Dev Journal — Rover Navigation AI

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