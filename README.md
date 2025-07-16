# E-commerce Microservices

This is a sample e-commerce application built with a microservices architecture. The project demonstrates a variety of technologies and patterns for building a scalable and maintainable backend system.

## Architecture

The application is composed of several independent services that communicate with each other via REST APIs and gRPC. It uses a message broker for asynchronous communication and various databases for data storage.

The main components are:
- **User Service**: Manages user accounts, authentication, and authorization.
- **Product Service**: Manages products, categories, and pricing. It also acts as a gRPC server for price information.
- **Cart Service**: Manages user shopping carts.
- **Search Service**: Provides product search and filtering capabilities, powered by Elasticsearch.
- **Notification Service**: Handles sending notifications (e.g., emails) to users. It's a gRPC service.
- **MongoDB**: Primary database for most services.
- **Redis**: Used for caching.
- **RabbitMQ**: Message broker for asynchronous tasks.
- **Elasticsearch**: Powers the search service.

## Services

| Service                | Language/Framework | Port (Host) | Description                                      |
| ---------------------- | ------------------ | ----------- | ------------------------------------------------ |
| `user-service`         | Python/FastAPI     | 8000        | Handles user authentication and management.      |
| `product-service`      | Python/FastAPI     | 8001        | Manages products and provides price via gRPC.    |
| `cart-service`         | Python/FastAPI     | 8002        | Manages shopping carts.                          |
| `search-service`       | Python/FastAPI     | 8003        | Provides search functionality over products.     |
| `notification-service` | Python/gRPC        | 50051       | Sends notifications (e.g., email).               |
| `mongo`                | MongoDB            | 27017       | Primary database.                                |
| `redis`                | Redis              | 6379        | Caching layer for products.                                   |
| `rabbitmq`             | RabbitMQ           | 15672       | Message broker.                  |
| `elasticsearch`        | Elasticsearch      | 9200, 9300  | Search and analytics engine.                     |

*Note: The `product-service` also exposes a gRPC server on port `50052` inside the docker network.*

## Technologies Used

- **Backend**: Python, FastAPI, gRPC
- **Databases**: MongoDB, Redis, Elasticsearch
- **Message Broker**: RabbitMQ
- **Containerization**: Docker, Docker Compose
- **Dependency Management**: `uv`

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1.  **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd e-commerce-microservices
    ```

2.  **Environment Variables:**
    Each service has its own `.env` file for configuration. You'll need to create them based on the example files or the configuration settings in `app/core/config.py` for each service.

3.  **Build and run the application:**
    ```sh
    docker-compose up --build
    ```
    This command will build the Docker images for each service and start all the containers.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
