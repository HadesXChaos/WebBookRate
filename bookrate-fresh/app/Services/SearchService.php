<?php

namespace App\Services;

use App\Models\Book;
use App\Models\Author;
use App\Models\Review;
use MeiliSearch\Client;

class SearchService
{
    protected Client $client;

    public function __construct()
    {
        // In Docker, use meilisearch hostname, otherwise use localhost
        $host = env('MEILISEARCH_HOST', 'http://meilisearch:7700');
        
        // If host doesn't have http://, add it
        if (!str_starts_with($host, 'http://') && !str_starts_with($host, 'https://')) {
            $host = 'http://' . $host;
        }
        
        // Add port if not specified
        if (!str_contains($host, ':7700')) {
            $host .= ':7700';
        }
        
        $key = env('MEILISEARCH_KEY', '');

        $this->client = new Client($host, $key);
    }

    public function indexBooks(): void
    {
        $index = $this->client->index('books');

        // Get all books with relationships
        $books = Book::with(['author', 'publisher', 'tags'])->get();

        $documents = $books->map(function ($book) {
            return [
                'id' => $book->id,
                'title' => $book->title,
                'slug' => $book->slug,
                'author_name' => $book->author->name,
                'author_id' => $book->author_id,
                'publisher_name' => $book->publisher->name ?? null,
                'description' => $book->description,
                'published_year' => $book->published_year,
                'pages' => $book->pages,
                'language' => $book->language,
                'avg_rating' => $book->avg_rating,
                'ratings_count' => $book->ratings_count,
                'reviews_count' => $book->reviews_count,
                'tags' => $book->tags->pluck('name')->toArray(),
                'created_at' => $book->created_at->toIso8601String(),
            ];
        })->toArray();

        $index->addDocuments($documents);

        // Configure searchable attributes
        $index->updateSearchableAttributes([
            'title',
            'author_name',
            'description',
            'tags',
        ]);

        // Configure filterable attributes
        $index->updateFilterableAttributes([
            'author_id',
            'published_year',
            'language',
            'avg_rating',
            'tags',
        ]);

        // Configure sortable attributes
        $index->updateSortableAttributes([
            'published_year',
            'avg_rating',
            'reviews_count',
            'created_at',
        ]);
    }

    public function indexAuthors(): void
    {
        $index = $this->client->index('authors');

        $authors = Author::all();

        $documents = $authors->map(function ($author) {
            return [
                'id' => $author->id,
                'name' => $author->name,
                'slug' => $author->slug,
                'bio' => $author->bio,
                'country' => $author->country,
                'birthday' => $author->birthday?->format('Y-m-d'),
            ];
        })->toArray();

        $index->addDocuments($documents);

        $index->updateSearchableAttributes(['name', 'bio']);
        $index->updateFilterableAttributes(['country']);
        $index->updateSortableAttributes(['name']);
    }

    public function indexReviews(): void
    {
        $index = $this->client->index('reviews');

        $reviews = Review::with(['user', 'book.author'])
            ->where('status', 'published')
            ->get();

        $documents = $reviews->map(function ($review) {
            return [
                'id' => $review->id,
                'book_id' => $review->book_id,
                'book_title' => $review->book->title,
                'author_name' => $review->book->author->name,
                'user_id' => $review->user_id,
                'user_name' => $review->user->name,
                'title' => $review->title,
                'body_html' => $review->body_html,
                'rating' => $review->rating,
                'helpful_count' => $review->helpful_count,
                'created_at' => $review->created_at->toIso8601String(),
            ];
        })->toArray();

        $index->addDocuments($documents);

        $index->updateSearchableAttributes(['title', 'body_html', 'book_title', 'author_name']);
        $index->updateFilterableAttributes(['book_id', 'user_id', 'rating']);
        $index->updateSortableAttributes(['helpful_count', 'rating', 'created_at']);
    }

    public function searchBooks(array $filters = [], string $query = '', array $sort = []): array
    {
        $index = $this->client->index('books');

        $options = [
            'limit' => $filters['per_page'] ?? 20,
            'offset' => ($filters['page'] ?? 1) - 1,
        ];

        if (!empty($sort)) {
            $options['sort'] = $sort;
        }

        if (!empty($query)) {
            $response = $index->search($query, $options);
        } else {
            $response = $index->getDocuments($options);
        }

        // Convert SearchResult to array
        if (is_object($response)) {
            return [
                'data' => $response->getHits(),
                'total' => $response->getEstimatedTotalHits() ?? count($response->getHits()),
                'per_page' => $options['limit'],
                'current_page' => ($options['offset'] / $options['limit']) + 1,
            ];
        }

        return $response;
    }

    public function searchAuthors(string $query = ''): array
    {
        $index = $this->client->index('authors');

        if (empty($query)) {
            return $index->getDocuments();
        }

        $response = $index->search($query);

        if (is_object($response)) {
            return $response->getHits();
        }

        return $response;
    }

    public function searchReviews(array $filters = [], string $query = ''): array
    {
        $index = $this->client->index('reviews');

        $options = [
            'limit' => $filters['per_page'] ?? 20,
        ];

        if (!empty($query)) {
            $response = $index->search($query, $options);
        } else {
            $response = $index->getDocuments($options);
        }

        if (is_object($response)) {
            return [
                'data' => $response->getHits(),
                'total' => $response->getEstimatedTotalHits() ?? count($response->getHits()),
                'per_page' => $options['limit'],
            ];
        }

        return $response;
    }
}

