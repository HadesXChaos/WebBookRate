<?php

namespace App\Policies;

use App\Models\User;
use App\Models\Book;

class BookPolicy
{
    public function viewAny(User $user): bool
    {
        return true;
    }

    public function view(?User $user, Book $book): bool
    {
        return true;
    }

    public function create(User $user): bool
    {
        return $user->isModerator();
    }

    public function update(User $user, Book $book): bool
    {
        return $user->isModerator();
    }

    public function delete(User $user, Book $book): bool
    {
        return $user->isAdmin();
    }
}

