<?php

use App\Http\Controllers\Auth\LoginController;
use App\Http\Controllers\Auth\RegisterController;
use App\Http\Controllers\BookController;
use App\Http\Controllers\ReviewController;
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
});

