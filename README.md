# 🤖 Rover Navigation AI

A software-only autonomous navigation system built in simulation — designed to be the AI brain of a real rover prototype.

The system uses **computer vision**, **SLAM-based mapping**, and **path planning algorithms** to allow a rover to perceive its environment, build a map, and navigate to a destination independently.

> ⚙️ Hardware-ready: Built in simulation now, designed to plug into real rover hardware later.

---

## 🧠 Core Components

| Component | Description | Tech Used |
|---|---|---|
| Perception | Detects obstacles using camera feed | OpenCV, YOLOv8 |
| Mapping | Builds a 2D map of the environment | SLAM, Occupancy Grid |
| Path Planning | Finds optimal route to destination | A* Algorithm |
| Simulation | Virtual environment to test the system | PyBullet |

---

## 🗂️ Project Structure
rover-nav-ai/
├── perception/        # Computer vision, obstacle detection
├── mapping/           # SLAM, occupancy grid
├── planning/          # Path planning algorithms
├── simulation/        # PyBullet environment
├── utils/             # Shared helper functions
├── tests/             # Unit tests
├── docs/              # Documentation, diagrams
├── main.py            # Entry point
└── requirements.txt   # Dependencies

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- NVIDIA GPU recommended (RTX 4060 used in development)

### Installation

```bash
# Clone the repo
git clone https://github.com/levindas/rover-nav-ai.git
cd rover-nav-ai

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 📦 Dependencies

- `pybullet` — Robot simulation
- `opencv-python` — Computer vision
- `torch` — Deep learning (YOLOv8 backbone)
- `ultralytics` — YOLOv8
- `numpy` — Numerical computing
- `matplotlib` — Visualization

---

## 📍 Roadmap

- [x] Project structure setup
- [ ] Simulation environment (PyBullet)
- [ ] Obstacle detection (YOLOv8 + OpenCV)
- [ ] Mapping (Occupancy Grid)
- [ ] Path Planning (A*)
- [ ] Full pipeline integration

---

## 👤 Author

**Levinda Hansaka Samarakoon**
Built as a portfolio project — part of a larger goal to deploy this as a real autonomous rover prototype.