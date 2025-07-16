# Product Service

This service manages the products in the e-commerce application. It handles creating, retrieving, updating, and deleting products. It also provides price information to other services via a gRPC interface.

## Features

- Product catalog management (CRUD operations)
- Caching of product data using Redis
- Asynchronous updates to the search service via RabbitMQ
- gRPC server for providing product prices

## Technologies

- **Framework**: FastAPI
- **Database**: MongoDB with Beanie ODM
- **Caching**: Redis
- **Message Broker**: RabbitMQ (`aio-pika`)
- **gRPC**: For exposing the price service

## API Endpoints

- `/api/v1/products`: For CRUD operations on products.

The service also exposes a gRPC server for the `PriceService`.

## Environment Variables

- `PROJECT_NAME`: The name of the project.
- `API_V1_STR`: The prefix for the API version.
- `MONGO_URI`: The connection string for the MongoDB database.
- `REDIS_URL`: The URL for the Redis cache.
- `RABBITMQ_URL`: The URL for the RabbitMQ server.
- `PRICE_SERVICE_GRPC_HOST`: Host for the gRPC price service.
- `PRICE_SERVICE_GRPC_PORT`: Port for the gRPC price service.

## Running the Service

The service is designed to be run with Docker Compose from the root of the monorepo.

```sh
docker-compose up --build product-service
```
