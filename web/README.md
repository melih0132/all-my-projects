# Web Projects

This folder contains my web development projects, covering a wide range of web applications from backend services to frontend interfaces and game development. These projects demonstrate my proficiency in web technologies, frameworks, and various web development tools.

## Projects Included

### 1. [Backend - OOP](back/poo)
Backend projects focused on Object-Oriented Programming (OOP) principles in PHP.

- **[Automatisation](back/poo/automatisation)**: MVC architecture implementation with database integration
- **[Database](back/poo/db)**: Database operations and vehicle management system
- **[Objects](back/poo/objects)**: Progressive OOP examples from basic to complex implementations
- Demonstrates the use of classes, objects, inheritance, and OOP concepts
- PHP autoloading and class management

**Technologies**: PHP, SQL, Object-Oriented Programming, MVC Architecture

### 2. [Frontend](front)
Frontend projects including HTML, CSS, JavaScript, and modern web development techniques.

- **[AzerType Website](front/azertype-website)**: Typing practice website to learn typing faster
  - Interactive typing exercises
  - Word and sentence practice modes
  - Real-time typing speed calculation
  
- **[Projects](front/projects)**: Collection of frontend learning projects
  - **[DOM Projects](front/projects/dom)**: DOM manipulation exercises (01.1 to 01.5)
    - Image galleries and interactive elements
    - Event handling and dynamic content
    - Playlist management
  - **[Advanced DOM](front/projects/advanced-dom)**: Advanced DOM manipulation (02.1, 02.2)
    - Complex interactions and animations
  - **[AJAX Projects](front/projects/ajax)**: Asynchronous programming exercises (03.1, 03.2)
    - Fetch API and Axios implementations
    - Like button with server communication
    - Canvas mouse tracking
    - Data persistence

**Technologies**: HTML, CSS, JavaScript, AJAX, Fetch API, Axios, DOM API

### 3. [Phaser Projects](phaser-projects)
Projects built using the Phaser framework for HTML5 game development.

- Interactive web games and applications
- Real-time multiplayer functionality
- Socket.io integration for real-time communication
- Drawing applications, notifications, and quiz systems
- Public and private chat implementations

**Technologies**: Phaser.js, HTML5, JavaScript, Node.js, Socket.io, Express.js

## Technologies Used

### Languages & Frameworks
- **JavaScript**: Primary programming language for web development
- **PHP**: Server-side scripting language
- **HTML/CSS**: Core web markup and styling
- **Node.js**: JavaScript runtime environment

### Frontend Technologies
- **Phaser.js**: HTML5 game development framework
- **DOM API**: Document Object Model manipulation
- **AJAX**: Asynchronous JavaScript and XML
- **Fetch API**: Modern API for network requests
- **Axios**: HTTP client library
- **Responsive Design**: Mobile-first approach

### Backend Technologies
- **Express.js**: Web application framework for Node.js
- **PHP OOP**: Object-Oriented Programming in PHP
- **MVC Architecture**: Model-View-Controller pattern
- **PHP Autoloading**: Automatic class loading

### Real-time Communication
- **Socket.io**: Real-time bidirectional communication
- **WebSockets**: Persistent connections for live updates

### Databases
- **SQL**: Relational database queries
- **MySQL**: Database management system

### Development Tools
- **Git / GitHub**: Version control
- **npm**: Package manager for Node.js
- **Nodemon**: Development server auto-reload
- **Visual Studio Code**: Primary IDE

## Project Structure

```
web/
├── back/                    → Backend projects
│   └── poo/                 → Object-Oriented Programming projects
│       ├── automatisation/  → MVC automation project
│       │   ├── Category.php → Category model
│       │   ├── Game.php     → Game model
│       │   ├── Human.php    → Human model
│       │   ├── Vehicule.php → Vehicle model
│       │   ├── Model.php    → Base model class
│       │   ├── controller.php → Controller logic
│       │   ├── view.php     → View rendering
│       │   ├── db.php       → Database configuration
│       │   └── index.php    → Entry point
│       ├── db/              → Database project
│       │   ├── Vehicle.php  → Vehicle class
│       │   ├── Vehicule.php → Vehicle class (French)
│       │   ├── db.php       → Database connection
│       │   ├── index.php    → Main file
│       │   └── VEHICULE.sql → SQL schema
│       └── objects/          → OOP examples
│           ├── 1.1/          → Basic objects (SuperHero)
│           ├── 1.2/          → Advanced objects (SuperHero, SuperVilain)
│           └── 1.3/          → Complex objects with inheritance
├── front/                   → Frontend projects
│   ├── azertype-website/    → Typing practice website
│   │   └── LEARN_TO_WRITE_QUICK/
│   │       ├── index.html   → Main page
│   │       ├── style.css    → Styles
│   │       ├── main.js      → Main logic
│   │       ├── script.js    → Scripts
│   │       ├── popup.js     → Popup functionality
│   │       └── config.js    → Configuration
│   └── projects/            → Frontend learning projects
│       ├── dom/             → DOM manipulation projects
│       │   ├── 01.1/        → Image gallery
│       │   ├── 01.2/        → Interactive elements
│       │   ├── 01.3/        → Playlist management
│       │   ├── 01.4/        → Advanced interactions
│       │   └── 01.5/        → Complex DOM manipulation
│       ├── advanced-dom/    → Advanced DOM projects
│       │   ├── 02.1/        → Advanced interactions
│       │   └── 02.2/        → Complex animations
│       └── ajax/            → AJAX projects
│           ├── 03.1/        → Like button (Axios & Fetch)
│           │   ├── axias/   → Axios implementation
│           │   └── fetch/   → Fetch API implementation
│           └── 03.2/        → Mouse tracking
│               ├── canvas/  → Canvas mouse tracking
│               └── txt/     → Text file persistence
└── phaser-projects/         → Phaser game development
    ├── app/                 → Game applications
    │   ├── draw/            → Drawing application
    │   ├── notification/   → Notification system
    │   └── quiz/            → Quiz application
    ├── chat/                → Chat functionality
    │   ├── private-chat/    → Private chat feature
    │   └── public-chat/     → Public chat feature
    ├── private-chat/        → Standalone private chat
    └── public-chat/         → Standalone public chat
```

## Getting Started

Each project has its own structure and dependencies. To explore a project:

1. Navigate to the project directory
2. For PHP projects: Ensure PHP is installed and configure database if needed
3. For Node.js projects: Install dependencies using `npm install`, then run `npm start` or `node server.js`
4. For frontend projects: Open `index.html` in a web browser or use a local server
5. Read project-specific documentation if available

Feel free to explore the repositories for more detailed information on each project!
