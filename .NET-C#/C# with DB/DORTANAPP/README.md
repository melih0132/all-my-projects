# DortanApp

## Overview

**DortanApp** is a software application developed using WPF (Windows Presentation Foundation) and integrated with a database, specifically designed for managing the reservation of activities in a town hall. This project allows town hall staff to choose from existing activities or create new ones, and input reservation dates accordingly.

## Features

- User-friendly interface for managing reservations
- Ability to create and manage activities
- Database integration for storing and retrieving data
- Efficient handling of reservation dates

## Technologies Used

- **Programming Languages:** C#
- **Framework:** WPF
- **Database:** PGSQL
- **Tools:** Visual Studio, Git

## Installation

To run DortanApp locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/melih0132/PROJETS/tree/main/DORTANAPP
   ```

2. **Navigate to the Project Directory:**
   Open a terminal or command prompt and navigate to the directory where you cloned the repository.
   ```bash
   cd PROJECTS/.NET-C#/C# with DB/DORTANAPP
   ```

3. **Open the Project in Visual Studio:**
   Launch Visual Studio and open the solution file (`.sln`) located in the project directory.

4. **Restore Dependencies:**
   Ensure all necessary NuGet packages are restored. You can do this by right-clicking on the solution in the Solution Explorer and selecting "Restore NuGet Packages."

5. **Database Setup:**
   - Ensure you have PostgreSQL installed and running on your machine.
   - Create a new database for DortanApp.
   - Update the database connection string in the application's configuration file to match your PostgreSQL setup.

6. **Build and Run:**
   Build the solution by selecting "Build Solution" from the Build menu. Once the build is successful, run the application by pressing `F5` or selecting "Start Debugging" from the Debug menu.

## Usage

- **Managing Activities:**
  - Use the interface to add new activities or modify existing ones.
  - Each activity can have specific details such as name, description, and available slots.

- **Reservations:**
  - Select an activity and input the reservation dates.
  - The system will handle conflicts and ensure that reservations do not overlap.

---

This completes the documentation for DortanApp. If you have any further questions or need additional details, feel free to ask!
