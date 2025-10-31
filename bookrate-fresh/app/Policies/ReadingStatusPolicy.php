<?php

namespace App\Policies;

use App\Models\User;
use App\Models\ReadingStatus;

class ReadingStatusPolicy
{
    public function viewAny(?User $user): bool
    {
        return true;
    }

    public function view(?User $user, ReadingStatus $readingStatus): bool
    {
        return true; // Can be made private in future
    }

    public function create(User $user): bool
    {
        return true;
    }

    public function update(User $user, ReadingStatus $readingStatus): bool
    {
        return $user->id === $readingStatus->user_id;
    }

    public function delete(User $user, ReadingStatus $readingStatus): bool
    {
        return $user->id === $readingStatus->user_id;
    }
}

