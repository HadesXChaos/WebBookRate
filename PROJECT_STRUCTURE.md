# BookRate Project Structure

## 📁 Directory Overview

```
bookrate-fresh/                    # Main application directory
├── app/
│   ├── Console/
│   │   └── Commands/
│   │       └── IndexSearchCommand.php  # Meilisearch indexing
│   ├── Http/
│   │   └── Controllers/
│   │       ├── Auth/
│   │       │   ├── LoginController.php
│   │       │   └── RegisterController.php
│   │       ├── BookController.php
│   │       ├── BookshelfController.php
│   │       ├── CommentController.php
│   │       ├── ReadingStatusController.php
│   │       ├── ReactionController.php
│   │       ├── ReviewController.php
│   │       └── SearchController.php
│   ├── Models/                     # Eloquent models
│   │   ├── Author.php
│   │   ├── AuditLog.php
│   │   ├── Book.php
│   │   ├── Bookshelf.php
│   │   ├── BookshelfItem.php
│   │   ├── BookTag.php
│   │   ├── Comment.php
│   │   ├── Edition.php
│   │   ├── Follow.php
│   │   ├── Publisher.php
│   │   ├── ReadingStatus.php
│   │   ├── Reaction.php
│   │   ├── Report.php
│   │   ├── Review.php
│   │   ├── Series.php
│   │   └── User.php
│   ├── Policies/                   # Authorization policies
│   │   ├── BookPolicy.php
│   │   ├── BookshelfPolicy.php
│   │   ├── CommentPolicy.php
│   │   ├── ReadingStatusPolicy.php
│   │   └── ReviewPolicy.php
│   ├── Providers/
│   │   └── AppServiceProvider.php
│   └── Services/                   # Business logic
│       ├── AuditService.php
│       ├── ReviewService.php
│       └── SearchService.php
├── bootstrap/
│   ├── app.php
│   └── providers.php
├── config/                         # Laravel configuration
│   ├── app.php
│   ├── auth.php
│   ├── cache.php
│   ├── database.php
│   ├── filesystems.php
│   ├── logging.php
│   ├── mail.php
│   ├── queue.php
│   ├── services.php
│   └── session.php
├── database/
│   ├── factories/                  # Model factories
│   │   ├── AuthorFactory.php
│   │   ├── BookFactory.php
│   │   ├── EditionFactory.php
│   │   ├── PublisherFactory.php
│   │   ├── ReviewFactory.php
│   │   ├── SeriesFactory.php
│   │   └── UserFactory.php
│   ├── migrations/                 # Database migrations
│   │   ├── 0001_01_01_000000_create_users_table.php
│   │   ├── 0001_01_01_000001_create_cache_table.php
│   │   ├── 0001_01_01_000002_create_jobs_table.php
│   │   ├── 2024_01_01_000000_update_users_table.php
│   │   ├── 2024_01_01_000001_create_authors_table.php
│   │   ├── 2024_01_01_000002_create_publishers_table.php
│   │   ├── 2024_01_01_000003_create_series_table.php
│   │   ├── 2024_01_01_000004_create_books_table.php
│   │   ├── 2024_01_01_000005_create_book_tags_table.php
│   │   ├── 2024_01_01_000006_create_editions_table.php
│   │   ├── 2024_01_01_000007_create_reviews_table.php
│   │   ├── 2024_01_01_000008_create_comments_table.php
│   │   ├── 2024_01_01_000009_create_reactions_table.php
│   │   ├── 2024_01_01_000010_create_bookshelves_table.php
│   │   ├── 2024_01_01_000011_create_reading_statuses_table.php
│   │   ├── 2024_01_01_000012_create_follows_table.php
│   │   ├── 2024_01_01_000013_create_notifications_table.php
│   │   ├── 2024_01_01_000014_create_reports_table.php
│   │   └── 2024_01_01_000015_create_audit_logs_table.php
│   └── seeders/                    # Database seeders
│       ├── AuthorSeeder.php
│       ├── BookSeeder.php
│       ├── BookTagSeeder.php
│       ├── DatabaseSeeder.php
│       ├── PublisherSeeder.php
│       ├── SeriesSeeder.php
│       └── UserSeeder.php
├── docker/                         # Docker configuration
│   ├── mysql/
│   │   └── my.cnf
│   ├── nginx/
│   │   └── default.conf
│   └── php/
│       ├── Dockerfile
│       └── php.ini
├── public/                         # Public assets
│   ├── index.php
│   ├── favicon.ico
│   └── robots.txt
├── resources/
│   ├── css/
│   │   └── app.css
│   ├── js/
│   │   ├── app.js
│   │   └── bootstrap.js
│   └── views/
│       └── welcome.blade.php
├── routes/
│   ├── api.php                    # API routes
│   ├── console.php                # Console routes
│   └── web.php                    # Web routes (42+ endpoints)
├── storage/                        # Storage files
│   ├── app/
│   ├── framework/
│   └── logs/
├── tests/                          # PHPUnit tests
│   ├── Feature/
│   │   └── ExampleTest.php
│   ├── Unit/
│   │   └── ExampleTest.php
│   └── TestCase.php
├── vendor/                         # Composer dependencies
├── .gitignore
├── artisan                         # Laravel CLI
├── composer.json
├── composer.lock
├── docker-compose.yml              # Docker Compose config
├── package.json
├── phpunit.xml
├── README.md                       # Full documentation
├── SUCCESS.md                      # Verification guide
├── FINAL_STATUS.md                 # Current status
├── UPDATED_STATUS.md               # Feature list
├── API_EXAMPLES.md                 # API usage examples
├── SETUP_NOTES.md                  # Configuration guide
├── COMPLETE_SUMMARY.md             # Quick overview
├── PHASE2_COMPLETE.md              # New features
└── vite.config.js
```

---

## 📊 Key Components

### Models (18)
- User management: User
- Content: Book, Author, Publisher, Series, Edition, BookTag
- UGC: Review, Comment, Reaction
- Social: Bookshelf, BookshelfItem, ReadingStatus, Follow
- Management: Report, AuditLog, Notification

### Controllers (10)
- Auth: LoginController, RegisterController
- Content: BookController, ReviewController, CommentController
- Social: BookshelfController, ReadingStatusController, ReactionController
- Search: SearchController

### Services (3)
- ReviewService: Review business logic
- AuditService: Logging and auditing
- SearchService: Meilisearch integration

### Policies (5)
- BookPolicy, ReviewPolicy, CommentPolicy
- BookshelfPolicy, ReadingStatusPolicy

---

## 🎯 API Routes

### Public (3)
- GET / - API info
- GET /books - List books
- GET /books/{id} - Book details
- GET /search - Search endpoint

### Auth (3)
- POST /auth/register
- POST /auth/login
- POST /auth/logout

### Protected (38)
- Books: 3 endpoints
- Reviews: 5 endpoints
- Comments: 5 endpoints
- Reactions: 3 endpoints
- Bookshelves: 7 endpoints
- Reading Status: 5 endpoints

**Total: 44 routes configured**

---

## 🗄️ Database Schema

### Tables (19)
1. users - Extended with role
2. authors - Book authors
3. publishers - Publishers
4. series - Book series
5. books - Main book catalog
6. book_tags - Categories
7. book_tag_pivot - Book-tag relationship
8. editions - Book editions
9. reviews - User reviews
10. comments - Comments on reviews/books
11. reactions - Helpful/like reactions
12. bookshelves - Custom shelves
13. bookshelf_items - Books in shelves
14. reading_statuses - Reading progress
15. follows - User follows
16. notifications - In-app alerts
17. reports - Content reports
18. audit_logs - Activity logging
19. Laravel internal tables (cache, jobs, etc.)

---

## 🐳 Docker Services

### Running Containers
1. **nginx** - Web server (port 8080)
2. **app** - PHP-FPM application
3. **db** - MySQL 8.0 (port 33060)
4. **redis** - Cache (port 63790)
5. **meilisearch** - Search engine (port 7700)

---

## 📦 Dependencies

### Backend
- Laravel 11
- PHP 8.3
- MySQL 8.0
- Redis 7
- Meilisearch 1.5

### Laravel Packages
- spatie/laravel-sluggable
- spatie/laravel-permission
- spatie/laravel-data
- intervention/image
- league/commonmark
- predis/predis
- meilisearch/meilisearch-php

---

## 🚀 Quick Commands

```bash
# Start application
cd bookrate-fresh
docker-compose up -d

# Run migrations
docker-compose exec app php artisan migrate:fresh --seed

# Index search
docker-compose exec app php artisan meilisearch:index

# View logs
docker-compose logs -f app
```

---

This is your complete BookRate project structure! 🎉

