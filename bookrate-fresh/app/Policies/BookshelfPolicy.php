<?php

namespace App\Policies;

use App\Models\User;
use App\Models\Bookshelf;

class BookshelfPolicy
{
    public function viewAny(?User $user): bool
    {
        return true;
    }

    public function view(?User $user, Bookshelf $bookshelf): bool
    {
        return $bookshelf->is_public || $user?->id === $bookshelf->user_id;
    }

    public function create(User $user): bool
    {
        return true;
    }

    public function update(User $user, Bookshelf $bookshelf): bool
    {
        return $user->id === $bookshelf->user_id;
    }

    public function delete(User $user, Bookshelf $bookshelf): bool
    {
        return $user->id === $bookshelf->user_id;
    }
}

