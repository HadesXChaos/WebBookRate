<?php

use App\Http\Controllers\Auth\LoginController;
use App\Http\Controllers\Auth\RegisterController;
use App\Http\Controllers\BookController;
use App\Http\Controllers\BookshelfController;
use App\Http\Controllers\CommentController;
use App\Http\Controllers\ReactionController;
use App\Http\Controllers\ReadingStatusController;
use App\Http\Controllers\ReviewController;
use App\Http\Controllers\SearchController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return response()->json([
        'message' => 'BookRate API',
        'version' => '1.0.0',
    ]);
});

// Authentication routes
Route::post('/auth/register', [RegisterController::class, 'store'])->name('register');
Route::post('/auth/login', [LoginController::class, 'store'])->name('login');
Route::post('/auth/logout', [LoginController::class, 'destroy'])->name('logout')->middleware('auth');

// Public book routes
Route::get('/books', [BookController::class, 'index'])->name('books.index');
Route::get('/books/{id}', [BookController::class, 'show'])->name('books.show');

// Public search route
Route::get('/search', [SearchController::class, 'search'])->name('search');

// Protected routes
Route::middleware(['auth'])->group(function () {
    // Books
    Route::post('/books', [BookController::class, 'store'])->name('books.store');
    Route::put('/books/{book}', [BookController::class, 'update'])->name('books.update');
    Route::delete('/books/{book}', [BookController::class, 'destroy'])->name('books.destroy');

    // Reviews
    Route::get('/reviews', [ReviewController::class, 'index'])->name('reviews.index');
    Route::post('/reviews', [ReviewController::class, 'store'])->name('reviews.store');
    Route::get('/reviews/{review}', [ReviewController::class, 'show'])->name('reviews.show');
    Route::put('/reviews/{review}', [ReviewController::class, 'update'])->name('reviews.update');
    Route::delete('/reviews/{review}', [ReviewController::class, 'destroy'])->name('reviews.destroy');

    // Comments
    Route::get('/comments', [CommentController::class, 'index'])->name('comments.index');
    Route::post('/comments', [CommentController::class, 'store'])->name('comments.store');
    Route::get('/comments/{comment}', [CommentController::class, 'show'])->name('comments.show');
    Route::put('/comments/{comment}', [CommentController::class, 'update'])->name('comments.update');
    Route::delete('/comments/{comment}', [CommentController::class, 'destroy'])->name('comments.destroy');

    // Reactions
    Route::post('/reactions', [ReactionController::class, 'store'])->name('reactions.store');
    Route::delete('/reactions', [ReactionController::class, 'destroy'])->name('reactions.destroy');
    Route::post('/reactions/toggle', [ReactionController::class, 'toggle'])->name('reactions.toggle');

    // Bookshelves
    Route::get('/bookshelves', [BookshelfController::class, 'index'])->name('bookshelves.index');
    Route::post('/bookshelves', [BookshelfController::class, 'store'])->name('bookshelves.store');
    Route::get('/bookshelves/{bookshelf}', [BookshelfController::class, 'show'])->name('bookshelves.show');
    Route::put('/bookshelves/{bookshelf}', [BookshelfController::class, 'update'])->name('bookshelves.update');
    Route::delete('/bookshelves/{bookshelf}', [BookshelfController::class, 'destroy'])->name('bookshelves.destroy');
    
    // Bookshelf items
    Route::post('/bookshelves/{bookshelf}/books', [BookshelfController::class, 'addBook'])->name('bookshelves.add-book');
    Route::delete('/bookshelves/{bookshelf}/books/{book}', [BookshelfController::class, 'removeBook'])->name('bookshelves.remove-book');

    // Reading Status
    Route::get('/reading-statuses', [ReadingStatusController::class, 'index'])->name('reading-statuses.index');
    Route::post('/reading-statuses', [ReadingStatusController::class, 'store'])->name('reading-statuses.store');
    Route::get('/reading-statuses/{readingStatus}', [ReadingStatusController::class, 'show'])->name('reading-statuses.show');
    Route::put('/reading-statuses/{readingStatus}', [ReadingStatusController::class, 'update'])->name('reading-statuses.update');
    Route::delete('/reading-statuses/{readingStatus}', [ReadingStatusController::class, 'destroy'])->name('reading-statuses.destroy');
});

