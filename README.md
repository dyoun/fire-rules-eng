# Overview

Python API service to compute observations against rules.

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
│   │   │   └── rule_evaluation.py  # Rules evaluation entities
│   │   └── interfaces/
│   │       ├── rules_repository.py     # Rules repository contract
│   │       └── rules_service.py        # Rules service contract
│   ├── application/            # Application layer (business logic)
│   │   └── services/
│   │       └── rules_service.py        # Rules evaluation logic
│   ├── infrastructure/         # Infrastructure layer (data access)
│   │   └── repositories/
│   ├── presentation/           # Presentation layer (API controllers)
│   │   ├── controllers/
│   │   │   └── rules_controller.py     # Rules evaluation REST API endpoints
│   │   └── app.py             # Flask application factory
│   └── config/                # Configuration
│       ├── container.py       # Dependency injection container
│       └── settings.py        # Application settings
├── tests/                     # Test directory
├── fire-risk.json            # Sample rule definition
├── observations.json         # Sample input data
├── run-rules.ipynb          # Jupyter notebook example
├── requirements.txt         # Python dependencies
├── main.py                 # Application entry point
└── README.md               # This file
```

## API Endpoints

### Health Check
- **GET** `/health`
  - Returns service health status
  - Response: `{"status": "healthy", "service": "rules-engine-api"}`

### Rules Engine
- **POST** `/rules/`
  - Evaluates rules against provided observations
  - Request body: 
    ```json
    {
      "observations": {
        "risk_type": "windows",
        "window_type": "tempered",
        "vegetation_type": "tree",
        "distance": 15
      },
      "request_id": "optional-request-id"
    }
    ```
  - Response:
    ```json
    {                                                                         
      "performance": "83.7µs",                                                
      "request_id": "test-005",                                               
      "result": {                                                             
        "calc_safe_distance": 15,                                             
        "distance": 15,                                                       
        "mitigations": {
          "Bridge": [                                
            "Apply a Film to windows which decreases minimum safe distance by 20%",
            "Apply flame retardants to shrubs that decrease minimum safe distance by 25%",
            "Prune trees to a safe height decreases safe distance by 50%"
          ],
          "Full": [                     
            "Remove Vegetation",
            "Replace window with Tempered Glass"
          ]
        },
        "risk_type": "windows",
        "safe_distance": 30,
        "vegetation_type": "tree",
        "window_type": "tempered"
      },
      "timestamp": "2025-08-24T22:37:46.022937"
    }
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
5. **Flexibility**: Components can be swapped out (e.g., rule repository instead of in-memory)

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


## Sources
* Rules API Service
* [Rules UI Interface to Administer Rules](https://hub.docker.com/r/gorules/brms)
* https://gorules.io/pricing
