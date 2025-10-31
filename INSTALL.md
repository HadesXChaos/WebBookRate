# Installation Guide for BookRate

## Prerequisites

Before installing BookRate, ensure you have the following installed:

- **PHP 8.3 or higher**
- **Composer** (PHP package manager)
- **MySQL 8.0 or higher** (or MariaDB 10.6+)
- **Redis 7.0+**
- **Node.js 18+ and npm**
- **Git**

## Installation Steps

### 1. Clone or Download the Project

```bash
git clone <repository-url> bookrate
cd bookrate
```

### 2. Install PHP Dependencies

```bash
composer install
```

### 3. Setup Environment File

Copy the example environment file:

```bash
copy .env.example .env  # Windows
# or
cp .env.example .env    # Linux/Mac
```

Edit `.env` file and configure:

- Database credentials
- APP_KEY (generate after next step)
- Redis connection
- Meilisearch settings
- Mail settings

### 4. Generate Application Key

```bash
php artisan key:generate
```

### 5. Create Database

Create a MySQL database named `bookrate`:

```sql
CREATE DATABASE bookrate CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Run Migrations

```bash
php artisan migrate
```

### 7. Seed Database (Optional but Recommended)

```bash
php artisan db:seed
```

This will create:
- Sample users (admin, moderators, regular users)
- Sample authors
- Sample books
- Sample categories

### 8. Install Frontend Dependencies

```bash
npm install
```

### 9. Build Frontend Assets

```bash
npm run build
```

For development:

```bash
npm run dev
```

### 10. Setup Storage Link

```bash
php artisan storage:link
```

### 11. Setup Meilisearch (Optional but Recommended)

Install Meilisearch:

**Windows (using Scoop):**
```bash
scoop install meilisearch
```

**Linux/Mac:**
```bash
curl -L https://install.meilisearch.com | sh
```

Start Meilisearch:
```bash
meilisearch
```

Configure Meilisearch in `.env`:
```
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=
```

Run Meilisearch indexing:
```bash
php artisan meilisearch:setup
```

### 12. Start Development Server

```bash
php artisan serve
```

Visit: http://localhost:8000

## Docker Installation (Alternative)

If you prefer using Docker:

### 1. Start Docker Containers

```bash
docker-compose up -d
```

### 2. Install Dependencies

```bash
docker-compose exec app composer install
```

### 3. Setup Environment

```bash
docker-compose exec app cp .env.example .env
docker-compose exec app php artisan key:generate
```

### 4. Run Migrations

```bash
docker-compose exec app php artisan migrate
docker-compose exec app php artisan db:seed
```

### 5. Access Application

- Web: http://localhost:8080
- Meilisearch: http://localhost:7700
- MySQL: localhost:33060

## Default Login Credentials

After seeding, you can login with:

**Admin:**
- Email: admin@bookrate.local
- Password: password

**Moderator:**
- Email: moderator@bookrate.local
- Password: password

**Regular User:**
- Email: user@bookrate.local
- Password: password

**⚠️ Important:** Change these passwords in production!

## Troubleshooting

### Permission Issues

If you encounter permission issues with storage:

```bash
# Linux/Mac
chmod -R 775 storage bootstrap/cache
chown -R www-data:www-data storage bootstrap/cache

# Windows
# Usually not needed, but ensure IIS_IUSRS has write permissions
```

### Cache Issues

Clear all caches:

```bash
php artisan config:clear
php artisan cache:clear
php artisan route:clear
php artisan view:clear
```

### Database Connection Issues

Check your `.env` database settings and ensure MySQL is running:

```bash
# Check MySQL status
# Windows: Services panel
# Linux: systemctl status mysql
# Mac: brew services list
```

### Meilisearch Connection Issues

Ensure Meilisearch is running:

```bash
curl http://localhost:7700/health
```

## Production Deployment

### 1. Optimize Application

```bash
php artisan config:cache
php artisan route:cache
php artisan view:cache
php artisan optimize
```

### 2. Update Environment

Set `APP_ENV=production` and `APP_DEBUG=false` in `.env`

### 3. Setup Queue Worker

```bash
php artisan queue:work --daemon
```

### 4. Setup Cron Jobs

Add to crontab:

```bash
* * * * * cd /path-to-project && php artisan schedule:run >> /dev/null 2>&1
```

### 5. Setup Web Server

Configure Nginx or Apache to point to `public/` directory

## Next Steps

- Configure email settings for notifications
- Setup SSL certificate
- Configure backup strategy
- Setup monitoring and logging
- Review security settings

## Support

For issues and questions:
- Check GitHub Issues
- Read documentation
- Contact support team

