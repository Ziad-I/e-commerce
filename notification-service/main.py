import logging
import os
import smtplib
from concurrent import futures
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import grpc
from google.protobuf.json_format import MessageToDict
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from core.config import settings
from proto import notification_pb2, notification_pb2_grpc
from core.logger import configure_logging

from loguru import logger


jinja_env = Environment(
    loader=FileSystemLoader(settings.TEMPLATES_DIR),
    autoescape=True,
)

TEMPLATE_MAP = {
    notification_pb2.EMAIL_TYPE_WELCOME: "welcome.html",
    notification_pb2.EMAIL_TYPE_PASSWORD_RESET: "password_reset.html",
    notification_pb2.EMAIL_TYPE_VERIFY: "verify.html",
    notification_pb2.EMAIL_TYPE_NOTIFICATION: "notification.html",
}


class NotificationService(notification_pb2_grpc.NotificationServiceServicer):
    def SendEmail(self, request, context):
        data = dict(request.metadata)
        template_file = TEMPLATE_MAP.get(request.type)

        if not template_file:
            error_msg = f"Unknown email type: {request.type}"
            logger.warning(error_msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(error_msg)
            return notification_pb2.SendEmailResponse(success=False, error=error_msg)

        try:
            template = jinja_env.get_template(template_file)
            body_html = template.render(**data)
        except TemplateNotFound:
            error_msg = f"Template not found: {template_file}"
            logger.error(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error while preparing email.")
            return notification_pb2.SendEmailResponse(success=False, error=error_msg)

        msg = MIMEText(body_html, "html", "utf-8")
        msg["Subject"] = data.get("subject", "Notification")
        msg["From"] = settings.SMTP_FROM
        msg["To"] = request.to

        try:
            with smtplib.SMTP(
                settings.SMTP_HOST, settings.SMTP_PORT, timeout=10
            ) as smtp:
                if settings.SMTP_TLS:
                    smtp.starttls()
                if settings.SMTP_USER and settings.SMTP_PASSWORD:
                    smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                smtp.sendmail(settings.SMTP_FROM, request.to, msg.as_string())
            logger.info(f"Email sent successfully to {request.to}")
            return notification_pb2.SendEmailResponse(success=True, error="")
        except smtplib.SMTPException as e:
            error_msg = "Failed to send email via SMTP"
            logger.error(f"{error_msg}: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("An internal error occurred while sending the email.")
            return notification_pb2.SendEmailResponse(success=False, error=error_msg)


def serve():
    configure_logging()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    notification_pb2_grpc.add_NotificationServiceServicer_to_server(
        NotificationService(), server
    )
    port = settings.GRPC_PORT
    host = settings.GRPC_HOST
    server.add_insecure_port(f"{host}:{port}")
    logger.info(f"gRPC email service listening on {host}:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
