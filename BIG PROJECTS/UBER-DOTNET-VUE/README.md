# Uber – Full Stack Application (.NET Core & Vue.js)

## Overview

A full stack web application inspired by the Uber model, developed with **.NET Core C#** for the back-end and **Vue.js** for the front-end. The project supports order management, meal delivery (Uber Eats), ride booking, and includes secure authentication using JWT.

## Key Features

### Authentication & User Management
* JWT authentication (registration, login, account management)
* Role-based access control (Admin, Driver, Customer)
* Profile management and settings
* Password recovery and email verification

### Ride Management
* Real-time ride booking
* Trip history and tracking
* Fare calculation
* Driver matching algorithm
* Ride status updates

### Food Delivery (Uber Eats)
* Restaurant management
* Menu and product management
* Order processing
* Delivery tracking
* Payment integration

### Interactive Features
* Interactive map with Leaflet
* Real-time location tracking
* Route optimization
* Estimated time of arrival
* Price estimation

### UI/UX
* Responsive design
* Material Design components
* Dark/Light theme
* Progressive Web App (PWA) support
* Offline functionality

## Technologies Used

### Back-end
* **Framework**: .NET 8
* **ORM**: Entity Framework Core
* **API**: RESTful Web API
* **Testing**: xUnit
* **Documentation**: Swagger/OpenAPI

### Front-end
* **Framework**: Vue.js 3
* **Build Tool**: Vite
* **State Management**: Pinia
* **Routing**: Vue Router
* **HTTP Client**: Axios
* **UI Framework**: Vuetify

### Database
* **Primary**: PostgreSQL
* **Caching**: Redis
* **Search**: Elasticsearch

### DevOps
* **Containerization**: Docker
* **CI/CD**: GitHub Actions
* **Monitoring**: Application Insights

## Prerequisites

* [.NET 8 SDK](https://dotnet.microsoft.com/download)
* [Node.js (>=16.x)](https://nodejs.org/)
* [PostgreSQL](https://www.postgresql.org/)
* [Vue CLI / Vite](https://vitejs.dev/)
* [Docker](https://www.docker.com/) (optional)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/melih0132/uber-clone-dotnet-vue.git
cd uber-clone-dotnet-vue
```

### 2. Backend Setup

```bash
cd UberApi
dotnet restore
dotnet ef database update
dotnet run
```

### 3. Frontend Setup

```bash
cd ../UberVueJS
npm install
npm run dev
```

## Configuration

### Environment Variables

Create a `.env` file in the front-end project root:

```env
VITE_API_URL=http://localhost:5000/api
VITE_MAP_API_KEY=your_map_api_key
VITE_STRIPE_PUBLIC_KEY=your_stripe_key
```

### Database Configuration

Configure your PostgreSQL connection in `UberApi/appsettings.Development.json`:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Database=uber_clone;Username=your_username;Password=your_password"
  }
}
```

## Project Structure

```
uber-clone-dotnet-vue/
├── UberApi/                    → .NET Back-end API
│   ├── Controllers/           → REST Controllers
│   │   ├── AuthController.cs  → Authentication endpoints
│   │   ├── RideController.cs  → Ride management
│   │   └── OrderController.cs → Food delivery
│   ├── Models/               → Entities and DTOs
│   │   ├── Entities/        → Database models
│   │   └── DTOs/           → Data transfer objects
│   ├── Services/           → Business logic
│   │   ├── AuthService.cs  → Authentication logic
│   │   ├── RideService.cs  → Ride management
│   │   └── OrderService.cs → Order processing
│   ├── Data/               → Database context
│   ├── Migrations/         → EF Core migrations
│   └── Tests/              → Unit tests
│
└── UberVueJS/                 → Vue.js Front-end
    ├── src/
    │   ├── components/       → Reusable components
    │   │   ├── auth/        → Authentication
    │   │   ├── ride/        → Ride booking
    │   │   └── order/       → Food delivery
    │   ├── views/           → Page components
    │   ├── stores/          → Pinia stores
    │   ├── services/        → API services
    │   ├── assets/          → Static resources
    │   └── router/          → Route configuration
    ├── tests/               → Unit tests
    └── public/              → Public files
```

## Best Practices

* **Code Quality**
  * TypeScript for type safety
  * ESLint and Prettier for code formatting
  * Unit tests for critical components
  * Code documentation with XML comments

* **Security**
  * JWT token authentication
  * Role-based authorization
  * Input validation
  * XSS and CSRF protection
  * Secure password hashing

* **Performance**
  * Lazy loading of components
  * API response caching
  * Optimized database queries
  * Image optimization
  * Code splitting

* **Development Workflow**
  * Git Flow branching strategy
  * Pull request reviews
  * Automated testing
  * Continuous integration
  * Code quality checks

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## University Project

This project was developed as part of the 4th semester of the Computer Science BUT program.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
