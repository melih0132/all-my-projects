# Python Projects

Welcome to the Python Projects section of my repository! Here, you'll find a collection of various Python-based applications and scripts that I have developed.

## Projects

### [app](app)
A collection of Python applications and utilities.

1. **[little-things](app/little-things)**
   - A set of small, useful Python programs.
   - Includes scripts for tasks like file management, data manipulation, and automation.
   - Features:
     - Desktop wallpaper changer (`app_wallpaper.py`)
     - Task manager (`gestionnaire_taches.py`)
     - File renaming utilities (`rename-files/`)
     - Various utility scripts
   - Technologies: Python, OS modules

2. **[quiz-json](app/quiz-json)**
   - A quiz program that retrieves questions and answers from a JSON data source.
   - Demonstrates the use of JSON data handling in Python.
   - Features:
     - Multiple choice questions
     - Score tracking
     - JSON data management
   - Technologies: Python, JSON, Random

3. **[ranking](app/ranking)**
   - A project for ranking things.
   - Covers topics such as sorting, searching, and data manipulation.
   - Features:
     - Custom ranking algorithms
     - Data visualization
     - Export functionality
   - Technologies: Python, Pandas, Matplotlib

### [iut](iut)
Academic projects and assignments from IUT (Institut Universitaire de Technologie).
- Various Python programming exercises and solutions.
- Features:
  - Algorithm implementations (`algo/`)
  - Cryptography projects (`crypto/`)
  - Data structures
  - Problem-solving exercises
- Technologies: Python, NumPy, Matplotlib

## Technologies Used

The Python projects in this repository utilize the following technologies:

- **Python:** The primary programming language used for all the projects.
- **JSON:** Data format used for storing and retrieving quiz questions and answers.
- **Operating System Interaction:** Some projects interact with the operating system to perform tasks like changing the desktop wallpaper.
- **Data Processing:** Pandas, NumPy for data manipulation and analysis.
- **Visualization:** Matplotlib for data visualization.
- **Automation:** Schedule for task automation.

## Project Structure
```
python/
├── app/                     → Python applications
│   ├── little-things/       → Small utility scripts
│   │   ├── app_wallpaper.py → Desktop wallpaper changer
│   │   ├── gestionnaire_taches.py → Task manager
│   │   └── rename-files/    → File renaming utilities
│   ├── quiz-json/           → Quiz application using JSON
│   │   ├── quiz_game.py     → Main quiz game
│   │   └── quiz_data.json   → Quiz data
│   └── ranking/             → Ranking project
│       └── ranking.py        → Ranking algorithm
├── iut/                     → Academic projects
│   ├── algo/                → Algorithm implementations
│   │   ├── TD/              → Tutorial exercises
│   │   ├── REVISIONS/       → Revision exercises
│   │   └── ANNEXES/         → Course materials
│   └── crypto/              → Cryptography projects
│       ├── TRAVAUX/         → Assignments and practical work
│       └── ANNEXES/          → Course materials
└── README.md                → Project documentation
```

## Getting Started

To run any of these projects:

1. Ensure Python 3.x is installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Navigate to the project directory
4. Run the main script:
   ```bash
   python src/main.py
   ```

For more detailed instructions, please refer to each project's README file.
