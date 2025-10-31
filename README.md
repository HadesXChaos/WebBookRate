# BookRate - Community Book Review Platform

A comprehensive book review and rating platform built with Laravel 11, featuring reviews, ratings, bookshelves, and social features.

## 🚀 Technology Stack

- **Backend:** Laravel 11 (PHP 8.3+)
- **Database:** MySQL 8.0
- **Cache/Search:** Redis + Meilisearch
- **Frontend:** Blade + TailwindCSS + Alpine.js
- **Container:** Docker Compose

## 📋 Requirements

- Docker Desktop
- Docker Compose v3.8+
- 4GB+ RAM recommended

## 🛠️ Installation

### Option 1: With Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd bookrate
```

2. Start Docker containers:
```bash
docker-compose up -d
```

3. Install dependencies:
```bash
docker-compose exec app composer install
```

4. Generate application key:
```bash
docker-compose exec app php artisan key:generate
```

5. Run migrations:
```bash
docker-compose exec app php artisan migrate
```

6. Seed database:
```bash
docker-compose exec app php artisan db:seed
```

7. Access the application:
- Web: http://localhost:8080
- Meilisearch: http://localhost:7700
- MySQL: localhost:33060

### Option 2: Local Development

1. Install PHP 8.3+, Composer, MySQL 8.0, Redis

2. Install dependencies:
```bash
composer install
```

3. Copy environment file:
```bash
cp .env.example .env
```

4. Configure `.env` with your database credentials

5. Generate key and run migrations:
```bash
php artisan key:generate
php artisan migrate
php artisan db:seed
```

6. Start development server:
```bash
php artisan serve
```

## 📁 Project Structure

```
bookrate/
├── app/
│   ├── Models/           # Eloquent models
│   ├── Http/
│   │   ├── Controllers/  # Controllers
│   │   ├── Middleware/   # Custom middleware
│   │   ├── Requests/     # Form requests
│   │   └── Resources/    # API resources
│   ├── Services/         # Business logic
│   ├── Policies/         # Authorization policies
│   ├── Providers/        # Service providers
│   └── Observers/        # Model observers
├── database/
│   ├── migrations/       # Database migrations
│   ├── seeders/         # Database seeders
│   └── factories/       # Model factories
├── resources/
│   ├── views/           # Blade templates
│   ├── css/             # CSS files
│   ├── js/              # JavaScript files
│   └── lang/            # Language files
├── routes/
│   ├── web.php          # Web routes
│   ├── api.php          # API routes
│   └── channels.php     # Broadcast channels
├── tests/               # Tests
├── docker/              # Docker configuration
└── docker-compose.yml   # Docker Compose setup
```

## 🎯 Key Features

### For Users
- ✨ Discover books with advanced search
- ⭐ Rate and review books
- 📚 Create custom bookshelves
- 📖 Track reading progress
- 💬 Comment on reviews
- 🔔 Get notifications
- 👥 Follow users and authors

### For Moderators/Admins
- 🔍 Moderation queue
- 📊 Dashboard analytics
- 👥 User management
- 📝 Content management
- 🚨 Handle reports
- 🔒 Audit logging

## 🧪 Testing

Run PHPUnit tests:
```bash
php artisan test
```

Run with coverage:
```bash
php artisan test --coverage
```

## 📝 Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Submit a pull request

## 📄 License

This project is open-sourced software licensed under the MIT license.

## 🤝 Support

For issues and questions, please open an issue on GitHub.

