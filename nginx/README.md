# API Gateway with NGINX 

A minimal NGINX-based API gateway that:
- Routes API requests to the correct microservice based on the URL path.
- Validates JWTs via an internal /validate sub‑request to the user service.
- Caches validation results to improve performance.
- Forwards user info headers (X-User-Id, X-User-Email, X-Is-Verified) to services.

## How auth works

1. Client sends request with Authorization header
2. Nginx checks if the route requires authentication
3. If yes, it validates the token with the user service at /api/v1/users/auth/validate
4. Valid tokens are cached for 5 minutes
5. User info is forwarded to the microservice in headers:
   - X-User-Id
   - X-User-Email
   - X-User-Verified