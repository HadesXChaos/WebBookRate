# Setup Notes

## Meilisearch Configuration

Meilisearch is configured in the Docker setup but may need a master key in production. For development, we disabled it by removing `MEILI_MASTER_KEY` from docker-compose.yml.

To use Meilisearch with authentication:

```bash
# Option 1: Set master key in docker-compose.yml
environment:
  - MEILI_MASTER_KEY=masterKey

# Option 2: Run indexing with key
docker-compose exec -e MEILISEARCH_KEY=masterKey app php artisan meilisearch:index
```

## Commands Added

- `php artisan meilisearch:index` - Index all books, authors, and reviews

## New API Endpoints

### Comments
- `GET /comments` - List comments
- `POST /comments` - Create comment
- `GET /comments/{comment}` - Get comment
- `PUT /comments/{comment}` - Update comment
- `DELETE /comments/{comment}` - Delete comment

### Reactions
- `POST /reactions` - Add reaction
- `DELETE /reactions` - Remove reaction
- `POST /reactions/toggle` - Toggle reaction

### Bookshelves
- `GET /bookshelves` - List bookshelves
- `POST /bookshelves` - Create bookshelf
- `GET /bookshelves/{bookshelf}` - Get bookshelf
- `PUT /bookshelves/{bookshelf}` - Update bookshelf
- `DELETE /bookshelves/{bookshelf}` - Delete bookshelf
- `POST /bookshelves/{bookshelf}/books` - Add book
- `DELETE /bookshelves/{bookshelf}/books/{book}` - Remove book

### Reading Status
- `GET /reading-statuses` - List reading statuses
- `POST /reading-statuses` - Create/update reading status
- `GET /reading-statuses/{readingStatus}` - Get reading status
- `PUT /reading-statuses/{readingStatus}` - Update reading status
- `DELETE /reading-statuses/{readingStatus}` - Delete reading status

### Search
- `GET /search?q=keyword&type=books` - Search (books, authors, reviews, or all)

## Testing the API

```bash
# Get all books (test basic API)
curl http://localhost:8080/books

# Login first (will set cookie)
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@bookrate.local","password":"password"}' \
  -c cookies.txt

# Create a bookshelf (requires login)
curl -X POST http://localhost:8080/bookshelves \
  -H "Content-Type: application/json" \
  -H "Cookie: $(cat cookies.txt | grep laravel_session | awk '{print $7}')" \
  -d '{"name":"My Favorite Books","is_public":true}'

# Add book to shelf (requires login and shelf ID)
curl -X POST http://localhost:8080/bookshelves/1/books \
  -H "Content-Type: application/json" \
  -H "Cookie: $(cat cookies.txt | grep laravel_session | awk '{print $7}')" \
  -d '{"book_id":1,"note":"One of my favorites!"}'

# Search for books
curl http://localhost:8080/search?q=kiều&type=books

# Create reading status
curl -X POST http://localhost:8080/reading-statuses \
  -H "Content-Type: application/json" \
  -H "Cookie: $(cat cookies.txt | grep laravel_session | awk '{print $7}')" \
  -d '{"book_id":1,"status":"reading","progress_pages":50}'
```

## Troubleshooting

### Meilisearch Indexing
```bash
# Index data (without auth)
docker-compose exec app php artisan meilisearch:index

# Or with auth key
docker-compose exec -e MEILISEARCH_KEY=masterKey app php artisan meilisearch:index
```

### Clear Cache
```bash
docker-compose exec app php artisan config:clear
docker-compose exec app php artisan cache:clear
docker-compose exec app php artisan route:clear
```

### View Logs
```bash
docker-compose logs -f app
```

