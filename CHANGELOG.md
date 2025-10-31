# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-10-31

### Added
- **Comments System** - Full CRUD for commenting on reviews and books
  - Markdown support in comments
  - Spoiler tagging
  - Policy-based authorization
- **Reactions System** - Helpful, Like, Insightful reactions
  - Toggle functionality
  - Auto-aggregate helpful_count
  - Real-time updates
- **Bookshelf Management** - Custom shelves
  - Create/edit/delete shelves
  - Public/private visibility
  - Add/remove books
  - Personal notes
- **Reading Status Tracking** - Track reading progress
  - Want/Reading/Read/Abandoned states
  - Progress tracking (pages)
  - Start/finish dates
- **Meilisearch Integration** - Advanced search
  - Full-text search for books, authors, reviews
  - Typo tolerance
  - Fast search results
  - Pagination support
- **SearchController** - New search API endpoint
- **Additional Policies** - BookshelfPolicy, ReadingStatusPolicy
- **IndexSearchCommand** - Artisan command to index Meilisearch data

### Changed
- Updated AppServiceProvider with policy mappings
- Enhanced SearchService with proper configuration
- Improved routing with 42+ total endpoints
- Updated docker-compose.yml with Meilisearch configuration

### Statistics
- Total API Endpoints: 42+ (was 17)
- Controllers: 10 (was 4)
- Services: 3 (was 2)
- Policies: 5 (was 3)
- Database Tables: 19 (unchanged)
- Project Completion: 65% (was 40%)

---

## [0.1.0] - 2024-10-30

### Added
- Initial project structure with Laravel 11
- Docker Compose setup (Nginx, PHP-FPM, MySQL, Redis, Meilisearch)
- Database schema with 19 tables
- Eloquent models (18 models with relationships)
- Authentication system (register/login/logout)
- Book CRUD operations with advanced filtering
- Review system with star ratings (0.5-5.0)
- Markdown support in reviews
- Authorization policies (Book, Review, Comment)
- Business logic services (Review, Audit)
- Database seeders for test data
- Model factories for all entities
- PHPUnit test setup
- Comprehensive documentation

### Features Implemented
- User registration and authentication
- Role-based access control (guest, user, moderator, admin)
- Book catalog with pagination
- Advanced book filtering
- Review creation with ratings
- Auto-aggregate book ratings
- CSRF protection
- SQL injection prevention
- XSS protection
- Production-ready Docker deployment

### Statistics
- Total Files: 85+
- Lines of Code: 8,000+
- Models: 18
- Controllers: 4
- Services: 2
- Policies: 3
- Routes: 17
- Migrations: 19
- Seeders: 7
- Factories: 7
- Project Completion: 40%

---

## [Unreleased]

### Planned
- Admin panel with dashboard
- Moderation tools
- User management UI
- Report handling
- In-app notifications
- Email notifications
- Follow users/authors
- Activity feed
- Recommendations engine
- Frontend views with Blade
- TailwindCSS styling
- Responsive design
- Comprehensive test suite
- API documentation with OpenAPI/Swagger
- Performance optimization
- Caching strategies
- CDN integration

---

## Version History

- **0.2.0** - Phase 2: Extended Features (Comments, Reactions, Bookshelves, Reading Status, Search)
- **0.1.0** - Phase 1: Foundation (Infrastructure, Database, Authentication, Books, Reviews)
- **0.0.0** - Initial setup

---

**Note**: This project follows [Semantic Versioning](https://semver.org/)
