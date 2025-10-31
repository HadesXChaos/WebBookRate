<?php

namespace App\Http\Controllers;

use App\Models\Book;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class BookController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $query = Book::with(['author', 'publisher', 'tags']);

        // Search
        if ($request->has('q')) {
            $query->where('title', 'like', '%' . $request->q . '%')
                ->orWhereHas('author', function ($q) use ($request) {
                    $q->where('name', 'like', '%' . $request->q . '%');
                });
        }

        // Filters
        if ($request->has('author_id')) {
            $query->where('author_id', $request->author_id);
        }

        if ($request->has('tag_id')) {
            $query->whereHas('tags', function ($q) use ($request) {
                $q->where('book_tags.id', $request->tag_id);
            });
        }

        if ($request->has('published_year')) {
            $query->where('published_year', $request->published_year);
        }

        // Sorting
        $sortBy = $request->get('sort_by', 'created_at');
        $sortOrder = $request->get('sort_order', 'desc');

        $allowedSorts = ['created_at', 'avg_rating', 'reviews_count', 'title', 'published_year'];
        if (in_array($sortBy, $allowedSorts)) {
            $query->orderBy($sortBy, $sortOrder);
        }

        // Pagination
        $perPage = min($request->get('per_page', 20), 100);
        $books = $query->paginate($perPage);

        return response()->json($books);
    }

    public function show(string $id): JsonResponse
    {
        $book = Book::with([
            'author',
            'publisher',
            'series',
            'editions',
            'tags',
            'publishedReviews' => function ($query) {
                $query->with('user')
                    ->orderBy('helpful_count', 'desc')
                    ->limit(10);
            },
        ])->findOrFail($id);

        // Add user's reading status if authenticated
        if (auth()->check()) {
            $book->user_reading_status = $book->readingStatuses()
                ->where('user_id', auth()->id())
                ->first();
            $book->user_review = $book->reviews()
                ->where('user_id', auth()->id())
                ->first();
        }

        return response()->json($book);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'author_id' => ['required', 'exists:authors,id'],
            'publisher_id' => ['nullable', 'exists:publishers,id'],
            'series_id' => ['nullable', 'exists:series,id'],
            'title' => ['required', 'string', 'max:255'],
            'language' => ['nullable', 'string'],
            'published_year' => ['nullable', 'integer'],
            'pages' => ['nullable', 'integer'],
            'isbn10' => ['nullable', 'string'],
            'isbn13' => ['nullable', 'string'],
            'cover_url' => ['nullable', 'url'],
            'description' => ['nullable', 'string'],
            'tags' => ['nullable', 'array'],
            'tags.*' => ['exists:book_tags,id'],
        ]);

        $book = Book::create($validated);

        if (isset($validated['tags'])) {
            $book->tags()->attach($validated['tags']);
        }

        return response()->json($book, 201);
    }

    public function update(Request $request, Book $book): JsonResponse
    {
        $validated = $request->validate([
            'author_id' => ['sometimes', 'exists:authors,id'],
            'publisher_id' => ['nullable', 'exists:publishers,id'],
            'series_id' => ['nullable', 'exists:series,id'],
            'title' => ['sometimes', 'string', 'max:255'],
            'language' => ['nullable', 'string'],
            'published_year' => ['nullable', 'integer'],
            'pages' => ['nullable', 'integer'],
            'isbn10' => ['nullable', 'string'],
            'isbn13' => ['nullable', 'string'],
            'cover_url' => ['nullable', 'url'],
            'description' => ['nullable', 'string'],
            'tags' => ['nullable', 'array'],
            'tags.*' => ['exists:book_tags,id'],
        ]);

        $book->update($validated);

        if (isset($validated['tags'])) {
            $book->tags()->sync($validated['tags']);
        }

        return response()->json($book);
    }

    public function destroy(Book $book): JsonResponse
    {
        $book->delete();

        return response()->json(['message' => 'Book deleted successfully']);
    }
}

