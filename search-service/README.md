# Search Service

This service provides search capabilities for the e-commerce platform, primarily for products. It uses Elasticsearch as its search engine.

## Features

- Full-text search for products
- Filtering and sorting of search results
- Consumes messages from RabbitMQ to keep its index updated with product changes.

## Technologies

- **Framework**: FastAPI
- **Search Engine**: Elasticsearch
- **Message Broker**: RabbitMQ (`aio-pika`)

## API Endpoints

- `/api/v1/search`: To perform search queries.

## Environment Variables

- `PROJECT_NAME`: The name of the project.
- `API_V1_STR`: The prefix for the API version.
- `ELASTICSEARCH_URL`: The URL for the Elasticsearch cluster.
- `RABBITMQ_URL`: The URL for the RabbitMQ server.

## Running the Service

The service is designed to be run with Docker Compose from the root of the monorepo.

```sh
docker-compose up --build search-service
```
