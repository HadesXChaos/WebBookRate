# BookRate Project Structure

## 📁 Directory Overview

```
bookrate/
├── app/
│   ├── Console/               # Artisan commands
│   ├── Exceptions/            # Exception handlers
│   ├── Http/
│   │   ├── Controllers/       # Controllers (MVC)
│   │   │   ├── Auth/         # Authentication controllers
│   │   │   ├── BookController.php
│   │   │   ├── ReviewController.php
│   │   │   └── ...           # Other controllers
│   │   ├── Middleware/        # Custom middleware
│   │   ├── Requests/          # Form request validation
│   │   └── Resources/         # API resources
│   ├── Models/                # Eloquent models
│   │   ├── User.php
│   │   ├── Book.php
│   │   ├── Author.php
│   │   ├── Review.php
│   │   └── ...               # Other models
│   ├── Policies/              # Authorization policies
│   │   ├── BookPolicy.php
│   │   ├── ReviewPolicy.php
│   │   └── CommentPolicy.php
│   ├── Services/              # Business logic services
│   │   ├── ReviewService.php
│   │   └── AuditService.php
│   └── Providers/             # Service providers
├── bootstrap/
├── config/
├── database/
│   ├── factories/             # Model factories
│   ├── migrations/            # Database migrations
│   └── seeders/              # Database seeders
├── docker/
│   ├── nginx/
│   ├── php/
│   └── mysql/
├── public/                    # Public assets
├── resources/
│   ├── views/                # Blade templates
│   ├── css/
│   └── js/
├── routes/
│   ├── web.php               # Web routes
│   ├── api.php               # API routes
│   └── channels.php
├── storage/
├── tests/
├── docker-compose.yml
├── composer.json
└── README.md
```

## 🔑 Key Files

### Models
- **User**: Users with roles (guest, user, moderator, admin)
- **Book**: Books with ratings and reviews
- **Author**: Book authors
- **Publisher**: Publishers
- **Series**: Book series
- **BookTag**: Tags/categories
- **Edition**: Different editions of books
- **Review**: User reviews
- **Comment**: Comments on reviews/books
- **Reaction**: Reactions to reviews
- **Bookshelf**: Custom user bookshelves
- **BookshelfItem**: Items in bookshelves
- **ReadingStatus**: Reading progress tracking
- **Follow**: Following users/authors/books
- **Report**: Content reports
- **AuditLog**: Admin/mod actions logs

### Controllers
- **Auth/RegisterController**: User registration
- **Auth/LoginController**: User login/logout
- **BookController**: CRUD operations for books
- **ReviewController**: Review management
- **CommentController**: Comment management (TODO)
- **AdminController**: Admin panel (TODO)

### Services
- **ReviewService**: Business logic for reviews
- **AuditService**: Audit logging
- **NotificationService**: Notifications (TODO)
- **SearchService**: Meilisearch integration (TODO)

### Policies
- **BookPolicy**: Book authorization
- **ReviewPolicy**: Review authorization
- **CommentPolicy**: Comment authorization

## 🗄️ Database Schema

See `database/migrations/` for complete schema:
- `2024_01_01_000000_update_users_table.php` - User table updates
- `2024_01_01_000001_create_authors_table.php` - Authors
- `2024_01_01_000002_create_publishers_table.php` - Publishers
- `2024_01_01_000003_create_series_table.php` - Series
- `2024_01_01_000004_create_books_table.php` - Books
- `2024_01_01_000005_create_book_tags_table.php` - Tags & pivot
- `2024_01_01_000006_create_editions_table.php` - Editions
- `2024_01_01_000007_create_reviews_table.php` - Reviews
- `2024_01_01_000008_create_comments_table.php` - Comments
- `2024_01_01_000009_create_reactions_table.php` - Reactions
- `2024_01_01_000010_create_bookshelves_table.php` - Bookshelves
- `2024_01_01_000011_create_reading_statuses_table.php` - Reading status
- `2024_01_01_000012_create_follows_table.php` - Follows
- `2024_01_01_000013_create_notifications_table.php` - Notifications
- `2024_01_01_000014_create_reports_table.php` - Reports
- `2024_01_01_000015_create_audit_logs_table.php` - Audit logs

## 🚀 Features Implemented

### ✅ Completed
- [x] Docker setup with Nginx, PHP, MySQL, Redis, Meilisearch
- [x] Database migrations for all entities
- [x] Eloquent models with relationships
- [x] Authentication system (register/login/logout)
- [x] Book CRUD operations
- [x] Review system with ratings
- [x] Policies for authorization
- [x] Services for business logic
- [x] Database seeders for test data
- [x] Model factories

### 🔨 In Progress
- [ ] Comments management
- [ ] Reactions (helpful/like)
- [ ] Bookshelf features
- [ ] Reading status tracking
- [ ] Search with Meilisearch
- [ ] Admin panel
- [ ] Moderation tools
- [ ] Notifications
- [ ] Following system
- [ ] Reports handling
- [ ] Frontend views (Blade templates)
- [ ] Tests

## 📝 Next Steps

1. **Install Composer** and run `composer install`
2. **Setup .env** file from `.env.example`
3. **Run migrations**: `php artisan migrate`
4. **Seed database**: `php artisan db:seed`
5. **Start development**: `php artisan serve`

Or use Docker:
1. `docker-compose up -d`
2. `docker-compose exec app composer install`
3. `docker-compose exec app php artisan key:generate`
4. `docker-compose exec app php artisan migrate --seed`

## 🔗 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login
- `POST /auth/logout` - Logout

### Books
- `GET /books` - List books (with filters)
- `GET /books/{id}` - Get book details
- `POST /books` - Create book (admin/moderator)
- `PUT /books/{book}` - Update book (admin/moderator)
- `DELETE /books/{book}` - Delete book (admin)

### Reviews
- `GET /reviews` - List reviews
- `GET /reviews/{review}` - Get review
- `POST /reviews` - Create review (authenticated)
- `PUT /reviews/{review}` - Update review (owner/moderator)
- `DELETE /reviews/{review}` - Delete review (owner/moderator)

## 🧪 Testing

Run tests:
```bash
php artisan test
```

## 📚 Documentation

- [README.md](README.md) - Project overview
- [INSTALL.md](INSTALL.md) - Installation guide
- [requirement.md](requirement.md) - Full requirements

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

