# Django Auth Products

A full-featured Django REST API project with user authentication, product management, and async email processing using Celery.

## Features

- **User Authentication**: Custom user model with JWT authentication via `djangorestframework-simplejwt`
- **Email Verification**: Email verification system with async Celery tasks
- **Password Reset**: Forgot password and reset functionality
- **Product Management**: CRUD operations for products with category relationships
- **Category Management**: CRUD operations for categories
- **Role-Based Access**: Admin and User roles with permission-based access control
- **Async Tasks**: Celery workers for background email processing
- **Docker Setup**: Complete Docker Compose setup with PostgreSQL, Redis, Celery, and Flower
- **API Documentation**: RESTful API with pagination support
- **Logging**: Comprehensive logging system for error tracking and monitoring
- **Health Check**: Health check endpoint for monitoring and load balancers
- **Error Handling**: Standardized error responses with custom exception handler

## Tech Stack

- **Django** 5.1
- **Django REST Framework** 3.15.2
- **djangorestframework-simplejwt** 5.3.1
- **PostgreSQL** 16
- **Redis** 7
- **Celery** 5.4.0
- **Flower** (Celery monitoring)
- **Gunicorn** 21.2.0
- **Docker** & **Docker Compose**

## Project Structure

```
django-auth-products/
├── core/                 # Main Django project settings
│   ├── settings.py      # Project configuration
│   ├── urls.py          # Main URL configuration
│   ├── celery.py        # Celery configuration
│   └── wsgi.py          # WSGI configuration
├── users/               # User authentication app
│   ├── models.py        # Custom User model
│   ├── views.py         # Authentication views
│   ├── serializers.py   # User serializers
│   ├── tasks.py         # Celery tasks for emails
│   └── signals.py       # User signals
├── products/            # Products app
│   ├── models.py        # Product model
│   ├── views.py         # Product views
│   ├── serializers.py   # Product serializers
│   └── permissions.py   # Custom permissions
├── categories/          # Categories app
│   ├── models.py        # Category model
│   ├── views.py         # Category views
│   └── serializers.py   # Category serializers
├── docker-compose.yml   # Docker Compose configuration
├── Dockerfile           # Docker image configuration
└── requirements.txt     # Python dependencies
```

## Database Models

### User Model
- Custom user model extending `AbstractUser`
- Fields: `role` (ADMIN/USER), `is_verified` (Boolean)
- JWT authentication support

### Category Model
- Fields: `name`, `description`, `created_at`

### Product Model
- Fields: `name`, `description`, `price`, `created_at`
- Relationships: `category` (ForeignKey), `created_by` (ForeignKey to User)

## Installation & Setup

### Prerequisites
- Docker and Docker Compose installed
- (Optional) Python 3.12+ if running locally

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd django-auth-products
   ```

2. **Create `.env` file**
   Create a `.env` file in the project root with the following variables:
   ```env
   # Django Settings
   DJANGO_SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=True
   
   # Database Settings
   POSTGRES_DB=django_auth
   POSTGRES_USER=django_user
   POSTGRES_PASSWORD=django_pass
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   
   # Redis Settings
   REDIS_URL=redis://redis:6379/0
   
   # Email Settings (Console backend by default)
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@example.com
   EMAIL_HOST_PASSWORD=your-email-password
   ```

3. **Build and run containers**
   ```bash
   docker compose up --build
   ```

4. **Run migrations**
   ```bash
   docker compose exec web python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

6. **Access the application**
   - API: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin
   - Health Check: http://localhost:8000/health
   - Flower (Celery Monitor): http://localhost:5555

### Running Locally (Without Docker)

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install flower  # For Celery monitoring
   ```

2. **Set up PostgreSQL and Redis**
   - Install and run PostgreSQL
   - Install and run Redis

3. **Configure environment variables**
   Update the `.env` file or set environment variables directly.

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start Celery worker**
   ```bash
   celery -A core worker -l info
   ```

7. **Start Flower (optional)**
   ```bash
   celery -A core flower --broker=redis://localhost:6379/0 --port=5555
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - API: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin
   - Health Check: http://localhost:8000/health
   - Flower (Celery Monitor): http://localhost:5555

## API Endpoints

### Health Check

- `GET /health` - Health check endpoint (checks Database and Redis)

### Authentication (`/api/auth`)

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT tokens
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/verify-email` - Verify user email
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password with token

### Categories (`/api/categories`)

- `GET /api/categories` - List all categories (public)
- `POST /api/categories` - Create category (Admin only)
- `GET /api/categories/{id}` - Get category details (public)
- `PUT /api/categories/{id}` - Update category (Admin only)
- `PATCH /api/categories/{id}` - Partial update category (Admin only)
- `DELETE /api/categories/{id}` - Delete category (Admin only)

### Products (`/api/products`)

- `GET /api/products` - List all products (public)
- `POST /api/products` - Create product (Authenticated users)
- `GET /api/products/{id}` - Get product details (public)
- `PUT /api/products/{id}` - Update product (Owner or Admin)
- `PATCH /api/products/{id}` - Partial update product (Owner or Admin)
- `DELETE /api/products/{id}` - Delete product (Owner or Admin)

## API Usage Examples

### Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### Create a Category (Admin only)
```bash
curl -X POST http://localhost:8000/api/categories \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Electronics",
    "description": "Electronic products"
  }'
```

### Create a Product
```bash
curl -X POST http://localhost:8000/api/products \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "category": 1,
    "price": "999.99"
  }'
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | `insecure-secret` |
| `DJANGO_DEBUG` | Debug mode | `True` |
| `POSTGRES_DB` | PostgreSQL database name | `django_auth` |
| `POSTGRES_USER` | PostgreSQL username | `django_user` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `django_pass` |
| `POSTGRES_HOST` | PostgreSQL host | `db` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |
| `REDIS_URL` | Redis connection URL | `redis://redis:6379/0` |
| `EMAIL_BACKEND` | Email backend | `django.core.mail.backends.console.EmailBackend` |
| `EMAIL_HOST` | SMTP host | `smtp.example.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_USE_TLS` | Use TLS for email | `True` |
| `EMAIL_HOST_USER` | Email username | - |
| `EMAIL_HOST_PASSWORD` | Email password | - |
| `DJANGO_LOG_LEVEL` | Django log level | `INFO` |


## Auth flow 
[User signs up] 
       |
       v
[Django saves User model]
       |
       | post_save signal triggers
       v
[send_verification_email() in signals.py]
       |
       | 1️⃣ توليد JWT للتحقق
       | 2️⃣ بناء verify_url
       v
[Call Celery task]
send_welcome_email.delay(email, username, verify_url)
       |
       v
[Celery Worker picks up task]
       |
       v
[send_mail() sends email to user]
       |
       v
[User receives email with verify_url]
       |
       v
[User clicks verify_url in browser]
       |
       v
[Backend verifies token, activates account]

## Permissions

- **Categories**: Read-only for all users, write operations require Admin role
- **Products**: 
  - Read: Public access
  - Create: Authenticated users
  - Update/Delete: Product owner or Admin

## JWT Token Configuration

- **Access Token Lifetime**: 30 minutes
- **Refresh Token Lifetime**: 1 day
- **Authentication**: Bearer token in `Authorization` header

## Celery Tasks

- **Email Verification**: Sends verification email when user registers
- **Welcome Email**: Sends welcome email to new users
- **Password Reset**: Sends password reset email

All email tasks are processed asynchronously via Celery workers.

## Docker Services

- **web**: Django application (Gunicorn)
- **db**: PostgreSQL database
- **redis**: Redis message broker for Celery
- **celery**: Celery worker for async tasks
- **flower**: Celery monitoring dashboard

## Non-Functional Improvements

### Logging
- **File Logging**: Logs saved to `logs/django.log`
- **Console Logging**: Logs also output to console
- **Log Levels**: Configurable via `DJANGO_LOG_LEVEL` environment variable
- **Error Tracking**: Comprehensive error logging with context
- **Loggers**: Separate loggers for Django, Django requests, and core application

### Health Check
- **Endpoint**: `GET /health`
- **Checks**: Database connection and Redis (Celery broker) connectivity
- **Response**: JSON with service status and individual check results
- **Use Case**: Monitoring, load balancers, Kubernetes liveness/readiness probes
- **Status Codes**: Returns 200 if healthy, 503 if unhealthy

### Error Handling
- **Standardized Responses**: Consistent error response format across all endpoints
- **Custom Exception Handler**: Custom exception handler for better error messages
- **Error Logging**: All errors logged with context (request path, method, user)
- **Debug Mode**: Detailed errors in debug mode, generic messages in production
- **Error Types**: Handles 400, 401, 403, 404, 429, 500 status codes

## Development

### Running Tests
```bash
docker compose exec web python manage.py test
```

### Creating Migrations
```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

### Accessing Django Shell
```bash
docker compose exec web python manage.py shell
```

### Viewing Logs
```bash
docker compose logs -f web
docker compose logs -f celery
```

