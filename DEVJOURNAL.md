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