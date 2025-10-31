# Contributing to BookRate

Thank you for your interest in contributing to BookRate! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Show empathy towards others

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/bookrate.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Commit: `git commit -m "Add your feature"`
6. Push: `git push origin feature/your-feature-name`
7. Open a Pull Request

## Development Setup

### Using Docker (Recommended)

```bash
# Start services
docker-compose up -d

# Install dependencies
docker-compose exec app composer install
docker-compose exec app npm install

# Setup environment
docker-compose exec app cp .env.example .env
docker-compose exec app php artisan key:generate

# Run migrations
docker-compose exec app php artisan migrate --seed

# Run tests
docker-compose exec app php artisan test
```

### Local Development

1. Install PHP 8.3+, Composer, MySQL, Redis
2. `composer install`
3. `cp .env.example .env`
4. Configure `.env`
5. `php artisan key:generate`
6. `php artisan migrate --seed`
7. `php artisan serve`

## Code Standards

### PHP

- Follow PSR-12 coding standard
- Use type hints everywhere
- Write meaningful comments
- Keep methods small and focused
- Use dependency injection

```bash
# Format code with Pint
php artisan pint
```

### JavaScript

- Use ES6+ syntax
- Follow ESLint rules
- Use meaningful variable names
- Keep functions pure when possible

## Testing

Write tests for all new features:

```bash
# Run all tests
php artisan test

# Run specific test
php artisan test --filter=BookTest

# With coverage
php artisan test --coverage
```

### Test Categories

- **Unit Tests**: Test individual components
- **Feature Tests**: Test complete workflows
- **Browser Tests**: Test user interactions

## Pull Request Process

1. **Update Documentation**: Update README or docs if needed
2. **Add Tests**: Ensure tests pass for new features
3. **Update Changelog**: Document your changes
4. **Check CI**: Ensure all checks pass
5. **Request Review**: Ask for feedback

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No linter errors
- [ ] Backward compatible (if applicable)

## Commit Messages

Use clear, descriptive commit messages:

```
feat: add book search functionality
fix: resolve rating calculation bug
docs: update installation guide
test: add book controller tests
refactor: improve review service
```

Prefixes: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `style`, `chore`

## Architecture Guidelines

### Service Layer

Put business logic in services, not controllers:

```php
// ❌ Bad
public function store(Request $request) {
    $book = Book::create($request->all());
    $book->tags()->attach($request->tags);
    // complex logic...
}

// ✅ Good
public function store(CreateBookRequest $request) {
    return $this->bookService->create($request->validated());
}
```

### Policy Usage

Always check permissions with policies:

```php
$this->authorize('create', Book::class);
$this->authorize('update', $book);
```

### Resource Controllers

Use resource controllers for CRUD operations:

```php
Route::resource('books', BookController::class);
```

## Database Changes

### Migrations

- Always create new migrations, never modify existing ones
- Use meaningful migration names
- Add indexes for frequently queried columns
- Consider rollback impact

### Seeders

- Update seeders if adding new models
- Keep seeders idempotent
- Use factories when possible

## Frontend Guidelines

### Blade Templates

- Keep templates DRY
- Use components when reusable
- Follow semantic HTML

### Styling

- Use TailwindCSS utility classes
- Keep custom CSS minimal
- Responsive-first approach

### JavaScript

- Prefer Alpine.js for simple interactions
- Use vanilla JS when possible
- Consider Vue.js for complex components

## Security

- Never commit sensitive data
- Validate all user input
- Use parameterized queries
- Check permissions on every action
- Follow OWASP guidelines

## Performance

- Use eager loading to avoid N+1 queries
- Implement caching where appropriate
- Optimize images
- Minimize queries
- Use Redis for sessions/cache

## Documentation

### Code Comments

```php
/**
 * Create a new review for a book.
 *
 * @param User $user
 * @param Book $book
 * @param array $data
 * @return Review
 */
```

### API Documentation

Update API docs when changing endpoints.

## Getting Help

- Check existing issues
- Read the documentation
- Ask in discussions
- Contact maintainers

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Acknowledged in documentation

Thank you for contributing to BookRate! 🎉

