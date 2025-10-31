# Quick Start Guide

Get BookRate up and running in 5 minutes!

## Prerequisites

- Docker Desktop installed
- Git installed

## Setup Steps

### 1. Clone the Repository

```bash
git clone <repository-url> bookrate
cd bookrate
```

### 2. Start Docker

```bash
docker-compose up -d
```

Wait for all services to start (usually 30-60 seconds).

### 3. Install Dependencies

```bash
docker-compose exec app composer install
```

### 4. Configure Environment

```bash
docker-compose exec app cp .env.example .env
docker-compose exec app php artisan key:generate
```

### 5. Setup Database

```bash
docker-compose exec app php artisan migrate --seed
```

### 6. Access the Application

- **Web App**: http://localhost:8080
- **Meilisearch**: http://localhost:7700
- **MySQL**: localhost:33060

### 7. Login Credentials

After seeding, use these credentials:

**Admin:**
- Email: `admin@bookrate.local`
- Password: `password`

**Regular User:**
- Email: `user@bookrate.local`
- Password: `password`

⚠️ **Change passwords in production!**

## Testing the API

### Register a New User

```bash
curl -X POST http://localhost:8080/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password",
    "password_confirmation": "password"
  }'
```

### Login

```bash
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@bookrate.local",
    "password": "password"
  }'
```

### List Books

```bash
curl http://localhost:8080/books
```

### Get Book Details

```bash
curl http://localhost:8080/books/1
```

### Create a Review (Requires Login)

```bash
curl -X POST http://localhost:8080/reviews \
  -H "Content-Type: application/json" \
  -H "Cookie: laravel_session=YOUR_SESSION_TOKEN" \
  -d '{
    "book_id": 1,
    "rating": 4.5,
    "body_md": "Great book with wonderful storytelling and engaging characters!",
    "is_spoiler": false
  }'
```

## Common Commands

### View Logs

```bash
docker-compose logs -f app
```

### Access Container Shell

```bash
docker-compose exec app bash
```

### Run Artisan Commands

```bash
docker-compose exec app php artisan <command>
```

### Restart Services

```bash
docker-compose restart
```

### Stop Services

```bash
docker-compose down
```

### Fresh Database

```bash
docker-compose exec app php artisan migrate:fresh --seed
```

## Troubleshooting

### Port Already in Use

If port 8080 is in use, edit `docker-compose.yml`:

```yaml
ports:
  - "8081:80"  # Change 8080 to 8081
```

### Database Connection Error

Check if MySQL is running:

```bash
docker-compose ps
```

Restart if needed:

```bash
docker-compose restart db
```

### Permission Errors

Fix storage permissions:

```bash
docker-compose exec app chmod -R 775 storage bootstrap/cache
```

### Clear Cache

```bash
docker-compose exec app php artisan cache:clear
docker-compose exec app php artisan config:clear
docker-compose exec app php artisan route:clear
```

## Next Steps

1. Read [INSTALL.md](INSTALL.md) for detailed setup
2. Check [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for architecture
3. Review [TODO.md](TODO.md) for planned features
4. See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Need Help?

- Check existing issues on GitHub
- Read the documentation
- Ask in discussions
- Contact maintainers

Happy coding! 🚀

