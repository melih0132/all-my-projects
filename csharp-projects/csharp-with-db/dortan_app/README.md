# DortanApp

A WPF (Windows Presentation Foundation) application integrated with PostgreSQL database, specifically designed for managing activity reservations in a town hall. This project allows town hall staff to choose from existing activities or create new ones, and input reservation dates accordingly.

## Overview

DortanApp is a software application developed using WPF and integrated with a PostgreSQL database. The application provides a user-friendly interface for managing activity reservations, allowing staff to efficiently handle activity creation, selection, and reservation management.

## Features

- User-friendly interface for managing reservations
- Ability to create and manage activities
- Database integration for storing and retrieving data
- Efficient handling of reservation dates
- Activity selection and creation
- Reservation conflict detection and prevention

## Technologies Used

### Languages & Frameworks
- **C#**: Primary programming language
- **WPF**: Windows Presentation Foundation framework
- **XAML**: Markup language for UI design

### Databases & ORM
- **PostgreSQL**: Relational database management
- **Entity Framework Core**: Object-relational mapping (if applicable)
- **SQL**: Database queries and operations

### Development Tools
- **Visual Studio**: Primary IDE
- **Git / GitHub**: Version control
- **pgAdmin**: PostgreSQL administration tool (optional)

## Project Structure

```
dortan_app/
├── Dortan_IHM/             → Solution folder
│   └── DortanApp/          → Main application
│       ├── *.xaml          → XAML UI files
│       ├── *.cs            → C# source files
│       └── *.csproj        → Project file
├── Dortan_IHM.sln          → Solution file
├── Fonctionnalités.pdf     → Features documentation
└── README.md               → Project documentation
```

## Getting Started

### Prerequisites

- Visual Studio (latest version recommended)
- .NET SDK
- PostgreSQL (installed and running)
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/melih0132/PROJECTS.git
```

2. Navigate to the project directory:
```bash
cd csharp-projects/csharp-with-db/dortan_app
```

3. Open the project in Visual Studio:
   - Launch Visual Studio
   - Open the solution file `Dortan_IHM.sln` located in the project directory

4. Restore dependencies:
   - Right-click on the solution in the Solution Explorer
   - Select "Restore NuGet Packages"

5. Database setup:
   - Ensure PostgreSQL is installed and running on your machine
   - Create a new database for DortanApp
   - Update the database connection string in the application's configuration file (App.config or appsettings.json) to match your PostgreSQL setup
   - Run any database migration scripts if provided

6. Build and run:
   - Build the solution by selecting "Build Solution" from the Build menu
   - Once the build is successful, run the application by pressing `F5` or selecting "Start Debugging" from the Debug menu

## Usage

### Managing Activities
- Use the interface to add new activities or modify existing ones
- Each activity can have specific details such as name, description, and available slots
- Activities can be created, edited, or deleted through the user interface

### Reservations
- Select an activity and input the reservation dates
- The system will handle conflicts and ensure that reservations do not overlap
- View and manage existing reservations
- Track reservation history and availability

Feel free to explore the codebase for more detailed information!
