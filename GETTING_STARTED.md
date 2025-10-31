# Getting Started with BookRate

This document provides a comprehensive guide to setting up and using the BookRate project.

## What is BookRate?

BookRate is a community-driven book review and rating platform built with Laravel 11. It allows users to:
- Discover and explore books
- Rate and review books
- Create custom bookshelves
- Track reading progress
- Follow authors and other users
- Participate in discussions

## Project Status

### ✅ Completed (Phase 1)
- Docker setup with all services
- Complete database schema with 15+ tables
- Eloquent models with relationships
- Authentication system
- Book CRUD operations
- Review system with ratings
- Authorization policies
- Business logic services
- Database seeders
- Test structure

### 🔨 In Progress
- Frontend views
- Admin panel
- Moderation tools
- Search functionality
- Notifications

### 📅 Planned
- Bookshelf features
- Reading status tracking
- Following system
- Recommendations
- OAuth integration
- Email digest

## Installation Methods

### Method 1: Docker (Recommended)

**Best for**: Quick setup, consistent environment, production-like setup

1. Ensure Docker Desktop is running
2. Clone the repository
3. Run `docker-compose up -d`
4. Follow the commands in [QUICKSTART.md](QUICKSTART.md)

**Pros**: No local PHP/Composer needed, isolated environment, easy cleanup
**Cons**: Requires Docker, slightly slower on Windows/Mac

### Method 2: Laravel Installer

**Best for**: Development with full control, local debugging

1. Install PHP 8.3+, Composer, MySQL 8.0+, Redis
2. Run: `composer create-project laravel/laravel bookrate`
3. Copy files from this project to the Laravel installation
4. Run: `composer install`
5. Configure `.env`
6. Run: `php artisan migrate --seed`

**Pros**: Native performance, easier debugging
**Cons**: Requires more setup, OS-specific configuration

### Method 3: Laravel Sail

**Best for**: Official Laravel Docker solution

```bash
curl -s "https://laravel.build/bookrate" | bash
cd bookrate
./vendor/bin/sail up -d
./vendor/bin/sail artisan migrate --seed
```

**Pros**: Official Laravel tool, good documentation
**Cons**: Different from our docker-compose setup

## Project Structure

```
bookrate/
├── app/                    # Application code
│   ├── Http/              # HTTP layer
│   ├── Models/            # Eloquent models
│   ├── Services/          # Business logic
│   └── Policies/          # Authorization
├── database/              # Database
│   ├── migrations/        # Schema
│   ├── seeders/          # Initial data
│   └── factories/        # Test data
├── routes/                # Route definitions
├── tests/                 # Automated tests
├── docker/                # Docker configuration
└── resources/             # Views, assets
```

## Key Concepts

### Models & Relationships

**Book** (central entity)
- belongsTo: Author, Publisher, Series
- hasMany: Reviews, Comments, Editions, Tags
- polymorphic: Follows

**Review** (user-generated content)
- belongsTo: User, Book, Edition
- hasMany: Comments, Reactions
- Auto-calculates book ratings

**User** (authentication & profiles)
- Roles: guest, user, moderator, admin
- Can review, comment, follow, create bookshelves

### Business Logic

**Services**: Handle complex operations
- `ReviewService`: Create/update/delete reviews, recalculate ratings
- `AuditService`: Log admin actions

**Policies**: Authorization rules
- `BookPolicy`: Who can create/edit/delete books
- `ReviewPolicy`: Who can moderate reviews
- `CommentPolicy`: Comment management rules

### Data Flow

```
User Request
    ↓
Routes (web.php/api.php)
    ↓
Middleware (auth, throttle)
    ↓
Controller
    ↓
Service (business logic)
    ↓
Model (database)
    ↓
Response (JSON/view)
```

## API Endpoints

### Authentication
- `POST /auth/register` - Create account
- `POST /auth/login` - Sign in
- `POST /auth/logout` - Sign out

### Books
- `GET /books` - List (with filters)
- `GET /books/{id}` - Details
- `POST /books` - Create (moderator+)
- `PUT /books/{id}` - Update (moderator+)
- `DELETE /books/{id}` - Delete (admin)

### Reviews
- `GET /reviews` - List
- `POST /reviews` - Create
- `PUT /reviews/{id}` - Update (owner/moderator)
- `DELETE /reviews/{id}` - Delete (owner/moderator)

## Database Schema

### Core Tables
- `users` - User accounts & profiles
- `authors` - Book authors
- `publishers` - Publishers
- `series` - Book series
- `books` - Books (central entity)
- `editions` - Book editions
- `book_tags` - Categories/tags
- `book_tag_pivot` - Many-to-many relationship

### User-Generated Content
- `reviews` - Book reviews
- `comments` - Comments on reviews
- `reactions` - Helpful/like reactions
- `bookshelves` - User bookshelves
- `bookshelf_items` - Items in shelves
- `reading_statuses` - Reading progress

### Social Features
- `follows` - Following relationships
- `notifications` - In-app notifications
- `reports` - Content reports
- `audit_logs` - Admin action logs

## Development Workflow

### 1. Create a New Feature

```bash
# Create migration
php artisan make:migration create_feature_table

# Create model
php artisan make:model Feature

# Create controller
php artisan make:controller FeatureController

# Create policy
php artisan make:policy FeaturePolicy

# Add routes
# routes/web.php
```

### 2. Database Changes

```bash
# Create migration
php artisan make:migration add_column_to_table

# Run migrations
php artisan migrate

# Rollback if needed
php artisan migrate:rollback
```

### 3. Testing

```bash
# Run all tests
php artisan test

# Specific test
php artisan test --filter=BookTest

# Coverage
php artisan test --coverage
```

### 4. Code Quality

```bash
# Format code
php artisan pint

# Static analysis (requires PHPStan)
composer phpstan

# Linting (requires ESLint)
npm run lint
```

## Configuration

### Environment Variables

Key settings in `.env`:

```env
APP_NAME=BookRate
APP_ENV=local
APP_DEBUG=true
DB_DATABASE=bookrate
DB_USERNAME=root
DB_PASSWORD=
REDIS_HOST=127.0.0.1
MEILISEARCH_HOST=http://127.0.0.1:7700
```

### Caching

```bash
# Cache config
php artisan config:cache

# Cache routes
php artisan route:cache

# Cache views
php artisan view:cache

# Clear all
php artisan optimize:clear
```

### Queue Workers

```bash
# Start queue worker
php artisan queue:work

# Failed jobs
php artisan queue:failed
php artisan queue:retry all
```

## Security Considerations

### Implemented
- Password hashing (bcrypt)
- CSRF protection
- SQL injection prevention (Eloquent)
- XSS protection
- Authorization policies
- Rate limiting

### To Implement
- 2FA authentication
- API tokens (Sanctum)
- OAuth integration
- Content security policy
- HTTPS enforcement
- Input sanitization

## Performance Tips

### Database
- Use indexes on frequently queried columns
- Eager load relationships to avoid N+1
- Use pagination for large datasets
- Optimize slow queries

### Caching
- Cache expensive queries
- Use Redis for sessions/cache
- Cache API responses
- CDN for static assets

### Code
- Avoid unnecessary loops
- Use lazy loading when appropriate
- Queue heavy tasks
- Optimize images

## Troubleshooting

### Common Issues

**Database connection error**
```bash
# Check MySQL is running
docker-compose ps db

# Check credentials in .env
# Restart containers
docker-compose restart
```

**Permission denied**
```bash
# Fix storage permissions
chmod -R 775 storage bootstrap/cache

# In Docker
docker-compose exec app chmod -R 775 storage
```

**Composer errors**
```bash
# Clear cache
composer clear-cache

# Reinstall
rm -rf vendor
composer install
```

**Migrations fail**
```bash
# Fresh migration
php artisan migrate:fresh --seed

# Reset database
php artisan db:wipe && php artisan migrate --seed
```

## Next Steps

1. **Read Documentation**
   - [README.md](README.md) - Overview
   - [INSTALL.md](INSTALL.md) - Detailed setup
   - [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Architecture

2. **Explore Code**
   - Models in `app/Models/`
   - Controllers in `app/Http/Controllers/`
   - Routes in `routes/web.php`

3. **Run the Application**
   - Access http://localhost:8080
   - Login with admin credentials
   - Create some books and reviews

4. **Contribute**
   - Check [TODO.md](TODO.md) for tasks
   - Read [CONTRIBUTING.md](CONTRIBUTING.md)
   - Submit pull requests

## Resources

- [Laravel Documentation](https://laravel.com/docs)
- [Docker Documentation](https://docs.docker.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Meilisearch Documentation](https://docs.meilisearch.com/)

## Support

- GitHub Issues: Report bugs and request features
- Discussions: Ask questions and share ideas
- Email: support@bookrate.local

Happy coding! 🎉

