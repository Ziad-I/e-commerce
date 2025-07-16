# Cart Service

This service is responsible for managing user shopping carts.

## Features

- Add items to a cart
- Remove items from a cart
- View cart contents
- Clear cart

## Technologies

- **Framework**: FastAPI
- **Database**: MongoDB with Beanie ODM
- **gRPC**: For communicating with the `product-service` to get item prices.

## API Endpoints

- `/api/v1/cart`: For all cart-related operations.

## Environment Variables

- `PROJECT_NAME`: The name of the project.
- `API_V1_STR`: The prefix for the API version.
- `MONGO_URI`: The connection string for the MongoDB database.
- `PRICE_SERVICE_GRPC_HOST`: Host for the product gRPC service.
- `PRICE_SERVICE_GRPC_PORT`: Port for the product gRPC service.

## Running the Service

The service is designed to be run with Docker Compose from the root of the monorepo.

```sh
docker-compose up --build cart-service
```
