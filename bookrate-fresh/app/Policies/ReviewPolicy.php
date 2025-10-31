<?php

namespace App\Policies;

use App\Models\User;
use App\Models\Review;

class ReviewPolicy
{
    public function viewAny(?User $user): bool
    {
        return true;
    }

    public function view(?User $user, Review $review): bool
    {
        return true;
    }

    public function create(User $user): bool
    {
        return $user->canReview();
    }

    public function update(User $user, Review $review): bool
    {
        return $user->id === $review->user_id || $user->isModerator();
    }

    public function delete(User $user, Review $review): bool
    {
        return $user->id === $review->user_id || $user->isModerator();
    }

    public function restore(User $user, Review $review): bool
    {
        return $user->isModerator();
    }

    public function forceDelete(User $user, Review $review): bool
    {
        return $user->isAdmin();
    }
}

