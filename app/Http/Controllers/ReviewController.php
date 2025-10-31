<?php

namespace App\Http\Controllers;

use App\Models\Review;
use App\Models\Book;
use App\Services\ReviewService;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class ReviewController extends Controller
{
    public function __construct(
        private ReviewService $reviewService
    ) {}

    public function index(Request $request): JsonResponse
    {
        $query = Review::with(['user', 'book.author', 'edition']);

        if ($request->has('book_id')) {
            $query->where('book_id', $request->book_id);
        }

        if ($request->has('user_id')) {
            $query->where('user_id', $request->user_id);
        }

        if ($request->get('status')) {
            $query->where('status', $request->status);
        } else {
            $query->where('status', 'published');
        }

        // Hide spoilers by default unless requested
        if (!$request->boolean('include_spoilers')) {
            $query->where('is_spoiler', false);
        }

        $reviews = $query->orderBy('created_at', 'desc')
            ->paginate($request->get('per_page', 20));

        return response()->json($reviews);
    }

    public function show(Review $review): JsonResponse
    {
        $review->load(['user', 'book.author', 'edition', 'comments.user', 'reactions.user']);

        return response()->json($review);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'book_id' => ['required', 'exists:books,id'],
            'edition_id' => ['nullable', 'exists:editions,id'],
            'title' => ['nullable', 'string', 'max:255'],
            'body_md' => ['required', 'string', 'min:50'],
            'rating' => ['required', 'numeric', 'min:0.5', 'max:5.0'],
            'is_spoiler' => ['boolean'],
        ]);

        $book = Book::findOrFail($validated['book_id']);

        // Check if user already has a review for this book/edition
        $existingReview = Review::where('user_id', auth()->id())
            ->where('book_id', $book->id)
            ->where('edition_id', $validated['edition_id'] ?? null)
            ->first();

        if ($existingReview) {
            return response()->json([
                'message' => 'You already have a review for this book edition',
                'review' => $existingReview,
            ], 422);
        }

        $review = $this->reviewService->createReview(auth()->user(), $book, $validated);

        return response()->json($review, 201);
    }

    public function update(Request $request, Review $review): JsonResponse
    {
        $validated = $request->validate([
            'title' => ['sometimes', 'string', 'max:255'],
            'body_md' => ['sometimes', 'string', 'min:50'],
            'rating' => ['sometimes', 'numeric', 'min:0.5', 'max:5.0'],
            'is_spoiler' => ['boolean'],
        ]);

        $review = $this->reviewService->updateReview($review, $validated);

        return response()->json($review);
    }

    public function destroy(Review $review): JsonResponse
    {
        $this->reviewService->deleteReview($review);

        return response()->json(['message' => 'Review deleted successfully']);
    }
}

