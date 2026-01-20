# Python Projects

This folder contains my Python development projects, covering a wide range of applications from utility scripts to academic assignments. These projects demonstrate my proficiency in Python programming, data processing, and various Python technologies.

## Projects Included

### 1. [Applications](applications)
A collection of Python applications and utilities.

- **[utilities](applications/utilities)**: A set of small, useful Python programs
  - Desktop wallpaper changer (`app_wallpaper.py`)
  - Task manager (CLI and GUI versions)
  - Rock-paper-scissors game
  - File renaming utilities with intelligent batch analysis (`file-renamer/music_formatter.py`)
- **[quiz-game](applications/quiz-game)**: A quiz program that retrieves questions and answers from a JSON data source
  - Multiple choice questions
  - Score tracking
  - JSON data management
- **[ranking](applications/ranking)**: A ranking management application
  - Create and manage rankings for various items
  - SQLite database for data persistence
  - Export functionality to CSV
  - Backup database functionality
  - Interactive GUI built with Tkinter

**Technologies**: Python, JSON, SQLite, Tkinter

### 2. [Academic](academic)
Academic projects and assignments from university studies.

- **[algorithms](academic/algorithms)**: Algorithm implementations and exercises
  - Data structures (linked lists, trees)
  - Recursive algorithms (Tower of Hanoi, tree traversals)
  - Fractal generation (Koch snowflake, various fractals)
  - Image processing
  - ASCII art generation
  - Base conversion algorithms
  - Object-oriented programming examples
  - Various algorithmic challenges and exercises
- **[cryptography](academic/cryptography)**: Cryptography projects and assignments
  - Symmetric encryption (AES, Caesar cipher with encryption/decryption)
  - Asymmetric encryption (RSA implementation and scripts)
  - Modular arithmetic operations (modular exponentiation, modular inverse)
  - Euler's totient function (φ)
  - Hash functions using Python's hashlib

**Technologies**: Python, NumPy, Matplotlib

## Technologies Used

### Languages & Frameworks
- **Python**: Primary programming language
- **NumPy**: Numerical computing library
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Data visualization
- **Tkinter**: GUI development
- **SQLite**: Database management

### Data Processing
- **JSON**: Data format for storing and retrieving data
- **CSV**: Comma-separated values file handling
- **File I/O**: File system operations

### Development Tools
- **Python 3.x**: Runtime environment
- **pip**: Package manager
- **Git / GitHub**: Version control

## Project Structure

```
python/
├── applications/              → Python applications
│   ├── utilities/            → Small utility scripts
│   │   ├── app_wallpaper.py  → Desktop wallpaper changer
│   │   ├── gestionnaire_taches.py → Task manager (CLI)
│   │   ├── gestionnaire_taches_app.py → Task manager (GUI)
│   │   ├── pierre_papier_ciseaux.py → Rock-paper-scissors game
│   │   └── file-renamer/     → File renaming utilities
│   │       ├── music_formatter.py → Intelligent music file formatter
│   │       ├── README.md     → Documentation
│   │       └── requirements.txt → Dependencies
│   ├── quiz-game/            → Quiz application using JSON
│   │   ├── quiz_game.py      → Main quiz game
│   │   ├── quiz_data.json    → Quiz data
│   │   └── README.md         → Documentation
│   └── ranking/              → Ranking project
│       ├── ranking.py        → Ranking application with GUI
│       └── README.md         → Documentation
└── academic/                 → Academic projects
    ├── algorithms/           → Algorithm implementations
    │   ├── 01_hanoi.py, 06_spoil_hanoi.py → Tower of Hanoi
    │   ├── 04_linkedList.py → Linked list implementation
    │   ├── 05_tree.py, tree.py → Tree data structures
    │   ├── 02_fract.py, flocon_koch.py → Fractal generation
    │   ├── 05_image.py → Image processing
    │   ├── 02_asciiart.py, ascii_art.py → ASCII art
    │   ├── recursions.py → Recursive algorithms
    │   ├── 02_bases.py → Base conversion
    │   ├── 03_poo.py → OOP examples
    │   └── Various exercise files (ex1_v1.py, ex2.py, exo1.py, etc.)
    └── cryptography/         → Cryptography projects
        ├── aes.py → AES encryption
        ├── chiffrement cesar.py, dechiffrement cesar.py → Caesar cipher
        ├── chiffrement par bloc avec AES.py → Block cipher with AES
        ├── rsa.py, rsa_script.py → RSA encryption
        ├── exponentiation_modulaire.py → Modular exponentiation
        ├── inverse_modulaire.py → Modular inverse
        ├── phi_euleur.py → Euler's totient function
        └── hashlib.py → Hash functions
```

## Getting Started

Each project has its own README with detailed instructions. To explore a project:

1. Navigate to the project directory
2. Read the project's README.md for specific setup instructions
3. Follow the installation and configuration steps
4. Run the project according to its documentation

Feel free to explore the repositories for more detailed information on each project!
