<?php

namespace App\Services;

use App\Models\Book;
use App\Models\Review;
use App\Models\User;
use Illuminate\Support\Facades\DB;

class ReviewService
{
    public function createReview(User $user, Book $book, array $data): Review
    {
        return DB::transaction(function () use ($user, $book, $data) {
            $review = Review::create([
                'user_id' => $user->id,
                'book_id' => $book->id,
                'edition_id' => $data['edition_id'] ?? null,
                'title' => $data['title'] ?? null,
                'body_md' => $data['body_md'] ?? null,
                'rating' => $data['rating'],
                'is_spoiler' => $data['is_spoiler'] ?? false,
                'status' => $data['status'] ?? 'published',
            ]);

            $this->updateBookRatings($book);

            return $review;
        });
    }

    public function updateReview(Review $review, array $data): Review
    {
        return DB::transaction(function () use ($review, $data) {
            $review->update($data);

            if (isset($data['rating'])) {
                $this->updateBookRatings($review->book);
            }

            return $review->fresh();
        });
    }

    public function deleteReview(Review $review): bool
    {
        return DB::transaction(function () use ($review) {
            $book = $review->book;
            $deleted = $review->delete();

            if ($deleted) {
                $this->updateBookRatings($book);
            }

            return $deleted;
        });
    }

    protected function updateBookRatings(Book $book): void
    {
        $stats = Review::where('book_id', $book->id)
            ->where('status', 'published')
            ->selectRaw('COUNT(*) as reviews_count, AVG(rating) as avg_rating')
            ->first();

        $book->update([
            'reviews_count' => $stats->reviews_count ?? 0,
            'avg_rating' => $stats->avg_rating ?? 0,
        ]);
    }
}

