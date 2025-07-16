# Notification Service

This is a gRPC-based service responsible for sending notifications, such as emails, to users.

## Features

- Sends different types of emails (e.g., welcome, password reset).
- Uses Jinja2 templates for email bodies.

## Technologies

- **Framework**: gRPC (`grpcio`)
- **Templating**: Jinja2

## gRPC Service

The service implements the `NotificationService` defined in `proto/notification.proto`.

- `SendEmail`: An RPC method to send an email.

## Environment Variables

- `NOTIFICATION_SERVICE_GRPC_HOST`: The host on which the gRPC server listens.
- `NOTIFICATION_SERVICE_GRPC_PORT`: The port for the gRPC server.
- `SMTP_HOST`: The SMTP server host.
- `SMTP_PORT`: The SMTP server port.
- `SMTP_USER`: The username for the SMTP server.
- `SMTP_PASSWORD`: The password for the SMTP server.
- `SMTP_FROM`: The "from" address for outgoing emails.
- `TEMPLATES_DIR`: The directory where email templates are stored.

## Running the Service

The service is designed to be run with Docker Compose from the root of the monorepo.

```sh
docker-compose up --build notification-service
```
