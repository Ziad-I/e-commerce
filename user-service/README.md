# User Service

This service is responsible for managing users, including authentication and authorization.

## Features

- User registration
- User login (token-based authentication)
- User profile management
- Password recovery

## Technologies

- **Framework**: FastAPI
- **Database**: MongoDB with Beanie ODM
- **Authentication**: `fastapi-users`
- **gRPC**: For communication with the `notification-service`.

## API Endpoints

The following are the main API prefixes:

- `/api/v1/users/auth`: For authentication-related endpoints (login, logout, etc.).
- `/api/v1/users`: For user management endpoints.

For a detailed list of endpoints, you can refer to the OpenAPI documentation available at `/api/v1/openapi.json` when the service is running.

## Environment Variables

This service requires a set of environment variables to be configured. These can be placed in a `.env` file in the service's root directory. Key variables include:

- `PROJECT_NAME`: The name of the project.
- `API_V1_STR`: The prefix for the API version.
- `MONGO_URI`: The connection string for the MongoDB database.
- `SECRET_KEY`: A secret key for signing JWTs.
- `NOTIFICATION_SERVICE_GRPC_HOST`: Host for the notification gRPC service.
- `NOTIFICATION_SERVICE_GRPC_PORT`: Port for the notification gRPC service.

## Running the Service

The service is designed to be run with Docker Compose from the root of the monorepo.

```sh
docker-compose up --build user-service
```
