# Hello World RESTful API Service

A Hello World RESTful Python Flask API service built using SOLID principles and enterprise design patterns.

## Architecture Overview

This application demonstrates clean architecture principles with clear separation of concerns across multiple layers.

### SOLID Principles Applied

- **Single Responsibility Principle (SRP)**: Each class has one reason to change
  - `Greeting` model only handles greeting data
  - `GreetingService` only handles business logic
  - `GreetingRepository` only handles data access

- **Open/Closed Principle (OCP)**: Open for extension, closed for modification
  - New repository implementations can be added without changing existing code
  - New greeting types can be added by extending the service

- **Liskov Substitution Principle (LSP)**: Objects should be replaceable with instances of their subtypes
  - `InMemoryGreetingRepository` can be replaced with any `IGreetingRepository` implementation

- **Interface Segregation Principle (ISP)**: Many client-specific interfaces are better than one general-purpose interface
  - `IGreetingRepository` and `IGreetingService` are focused, single-purpose interfaces

- **Dependency Inversion Principle (DIP)**: Depend on abstractions, not concretions
  - Services depend on repository interfaces, not concrete implementations
  - Controllers depend on service interfaces, not concrete services

### Enterprise Design Patterns

- **Repository Pattern**: Abstracts data access logic (`IGreetingRepository`)
- **Service Layer Pattern**: Encapsulates business logic (`GreetingService`)
- **Dependency Injection**: Manages object dependencies via DI container
- **Layered Architecture**: Clear separation between domain, application, infrastructure, and presentation layers

## Project Structure

```
app/
├── src/
│   ├── domain/                 # Domain layer (entities, interfaces)
│   │   ├── models/
│   │   │   └── greeting.py     # Greeting entity
│   │   └── interfaces/
│   │       ├── greeting_repository.py  # Repository contract
│   │       └── greeting_service.py     # Service contract
│   ├── application/            # Application layer (business logic)
│   │   └── services/
│   │       └── greeting_service.py     # Business logic implementation
│   ├── infrastructure/         # Infrastructure layer (data access)
│   │   └── repositories/
│   │       └── in_memory_greeting_repository.py  # Data access implementation
│   ├── presentation/           # Presentation layer (API controllers)
│   │   ├── controllers/
│   │   │   └── greeting_controller.py  # REST API endpoints
│   │   └── app.py             # Flask application factory
│   └── config/                # Configuration
│       ├── container.py       # Dependency injection container
│       └── settings.py        # Application settings
├── tests/                     # Test directory
├── requirements.txt           # Python dependencies
├── main.py                   # Application entry point
└── README.md                 # This file
```

## API Endpoints

### Health Check
- **GET** `/health`
  - Returns service health status
  - Response: `{"status": "healthy", "service": "hello-world-api"}`

### Greetings
- **GET** `/api/v1/hello`
  - Creates and returns a "Hello World!" greeting
  - Response: `{"id": "uuid", "message": "Hello World!", "timestamp": "ISO-8601"}`

- **GET** `/api/v1/greetings`
  - Returns all stored greetings
  - Response: Array of greeting objects

- **POST** `/api/v1/greetings`
  - Creates a custom greeting
  - Request body: `{"message": "Your custom message"}`
  - Response: `{"id": "uuid", "message": "Your custom message", "timestamp": "ISO-8601"}`

## Installation and Setup

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone or navigate to the project directory:
   ```bash
   cd app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the development server:
```bash
python main.py
```

The API will be available at `http://localhost:5000`

### Configuration

The application can be configured using environment variables:

- `HOST`: Server host (default: `0.0.0.0`)
- `PORT`: Server port (default: `5000`)
- `DEBUG`: Enable debug mode (default: `False`)
- `API_VERSION`: API version (default: `v1`)

Example:
```bash
export HOST=127.0.0.1
export PORT=8080
export DEBUG=true
python main.py
```

## Usage Examples

### Get Hello World greeting
```bash
curl http://localhost:5000/api/v1/hello
```

### Create a custom greeting
```bash
curl -X POST http://localhost:5000/api/v1/greetings \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from REST API!"}'
```

### Get all greetings
```bash
curl http://localhost:5000/api/v1/greetings
```

### Health check
```bash
curl http://localhost:5000/health
```

## Dependencies

- **Flask 3.0.0**: Web framework
- **dependency-injector 4.41.0**: Dependency injection container
- **Werkzeug 3.0.1**: WSGI utilities (Flask dependency)

## Design Benefits

1. **Maintainability**: Clear separation of concerns makes code easier to modify
2. **Testability**: Dependencies can be easily mocked for unit testing
3. **Extensibility**: New features can be added without modifying existing code
4. **Scalability**: Architecture supports growth and complexity
5. **Flexibility**: Components can be swapped out (e.g., database repository instead of in-memory)

## Future Enhancements

- Database integration (PostgreSQL, MongoDB)
- Authentication and authorization
- Input validation and error handling middleware
- Logging and monitoring
- API documentation with OpenAPI/Swagger
- Unit and integration tests
- Docker containerization
- CI/CD pipeline

Total cost:            $0.4066
Total duration (API):  2m 51.0s
Total duration (wall): 12m 5.6s
Total code changes:    452 lines added, 0 lines removed
Usage by model:
    claude-3-5-haiku:  2.2k input, 143 output, 0 cache read, 0 cache write
       claude-sonnet:  51 input, 8.5k output, 737.2k cache read, 14.7k cache write
