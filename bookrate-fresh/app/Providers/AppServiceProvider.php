<?php

namespace App\Providers;

use App\Models\Book;
use App\Models\Bookshelf;
use App\Models\Comment;
use App\Models\ReadingStatus;
use App\Models\Review;
use App\Policies\BookPolicy;
use App\Policies\BookshelfPolicy;
use App\Policies\CommentPolicy;
use App\Policies\ReadingStatusPolicy;
use App\Policies\ReviewPolicy;
use Illuminate\Support\Facades\Gate;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * The policy mappings for the application.
     *
     * @var array<class-string, class-string>
     */
    protected $policies = [
        Book::class => BookPolicy::class,
        Review::class => ReviewPolicy::class,
        Comment::class => CommentPolicy::class,
        Bookshelf::class => BookshelfPolicy::class,
        ReadingStatus::class => ReadingStatusPolicy::class,
    ];

    /**
     * Register any application services.
     */
    public function register(): void
    {
        //
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        //
    }
}
