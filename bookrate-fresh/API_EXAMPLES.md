# API Usage Examples

## Authentication

```bash
# Register
curl -X POST http://localhost:8080/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password",
    "password_confirmation": "password"
  }'

# Login (returns cookie)
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "admin@bookrate.local",
    "password": "password"
  }'
```

## Books

```bash
# List all books
curl http://localhost:8080/books

# Get book by ID
curl http://localhost:8080/books/1

# Create book (requires auth + moderator role)
curl -X POST http://localhost:8080/books \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "author_id": 1,
    "publisher_id": 1,
    "title": "New Book Title",
    "published_year": 2024,
    "pages": 300,
    "description": "A great book description"
  }'
```

## Reviews

```bash
# Create review (requires auth)
curl -X POST http://localhost:8080/reviews \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "book_id": 1,
    "rating": 4.5,
    "body_md": "This was an excellent book with great storytelling and engaging characters. The plot kept me hooked from start to finish!",
    "is_spoiler": false
  }'

# Get reviews for a book
curl "http://localhost:8080/reviews?book_id=1"
```

## Comments

```bash
# Comment on a review
curl -X POST http://localhost:8080/comments \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "review_id": 1,
    "body_md": "Great review! I totally agree with your points.",
    "is_spoiler": false
  }'

# Get comments for a review
curl "http://localhost:8080/comments?review_id=1"
```

## Reactions

```bash
# React to review (helpful/like/insightful)
curl -X POST http://localhost:8080/reactions \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "review_id": 1,
    "type": "helpful"
  }'

# Toggle reaction
curl -X POST http://localhost:8080/reactions/toggle \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "review_id": 1,
    "type": "helpful"
  }'
```

## Bookshelves

```bash
# Create bookshelf
curl -X POST http://localhost:8080/bookshelves \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "My Reading List",
    "description": "Books I want to read",
    "is_public": true
  }'

# Add book to shelf
curl -X POST http://localhost:8080/bookshelves/1/books \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "book_id": 1,
    "note": "Can'\''t wait to read this!"
  }'

# Get my bookshelves
curl http://localhost:8080/bookshelves -b cookies.txt
```

## Reading Status

```bash
# Mark book as reading
curl -X POST http://localhost:8080/reading-statuses \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "book_id": 1,
    "status": "reading",
    "started_at": "2024-01-01",
    "progress_pages": 50
  }'

# Update progress
curl -X PUT http://localhost:8080/reading-statuses/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "progress_pages": 100
  }'

# Mark as read
curl -X POST http://localhost:8080/reading-statuses \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "book_id": 1,
    "status": "read",
    "finished_at": "2024-01-31"
  }'
```

## Search

```bash
# Search books
curl "http://localhost:8080/search?q=kiều&type=books"

# Search authors
curl "http://localhost:8080/search?q=nguyễn&type=authors"

# Search reviews
curl "http://localhost:8080/search?q=excellent&type=reviews"

# Search all
curl "http://localhost:8080/search?q=book"
```

## Complete Workflow Example

```bash
# 1. Register and login
curl -X POST http://localhost:8080/auth/register \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "name": "Test User",
    "email": "test@test.com",
    "password": "password",
    "password_confirmation": "password"
  }'

# 2. Search for a book
curl "http://localhost:8080/search?q=truyen&type=books" -b cookies.txt

# 3. Mark as want to read
curl -X POST http://localhost:8080/reading-statuses \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"book_id":1,"status":"want"}'

# 4. Update to reading
curl -X POST http://localhost:8080/reading-statuses \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"book_id":1,"status":"reading","started_at":"2024-01-01","progress_pages":0}'

# 5. Mark as read and review
curl -X POST http://localhost:8080/reading-statuses \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"book_id":1,"status":"read","finished_at":"2024-01-31"}'

curl -X POST http://localhost:8080/reviews \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "book_id":1,
    "rating":5.0,
    "body_md":"Absolutely loved this book! The storytelling was amazing.",
    "is_spoiler":false
  }'

# 6. Create shelf and add book
curl -X POST http://localhost:8080/bookshelves \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name":"5-Star Books",
    "description":"My favorite books",
    "is_public":true
  }'

curl -X POST http://localhost:8080/bookshelves/1/books \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"book_id":1}'

# 7. View my profile stats
curl http://localhost:8080/reading-statuses?status=read -b cookies.txt
```

## Using Postman or Insomnia

Import this as a collection:

```json
{
  "info": {
    "name": "BookRate API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "Register",
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "body": {
              "mode": "raw",
              "raw": "{\"name\":\"John Doe\",\"email\":\"john@example.com\",\"password\":\"password\",\"password_confirmation\":\"password\"}"
            },
            "url": "http://localhost:8080/auth/register"
          }
        }
      ]
    }
  ]
}
```

