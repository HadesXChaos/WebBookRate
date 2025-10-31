<?php

namespace App\Http\Controllers;

use App\Models\Bookshelf;
use App\Models\BookshelfItem;
use App\Models\Book;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class BookshelfController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $query = Bookshelf::where('user_id', auth()->id());

        if ($request->boolean('public')) {
            $query->where('is_public', true);
        }

        $bookshelves = $query->with(['items.book.author'])
            ->orderBy('created_at', 'desc')
            ->get();

        return response()->json($bookshelves);
    }

    public function show(Bookshelf $bookshelf): JsonResponse
    {
        // Only show if public or owned by user
        if (!$bookshelf->is_public && $bookshelf->user_id !== auth()->id()) {
            abort(403);
        }

        $bookshelf->load(['user', 'items.book.author', 'items.book.tags']);

        return response()->json($bookshelf);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'name' => ['required', 'string', 'max:255'],
            'description' => ['nullable', 'string'],
            'is_public' => ['boolean'],
        ]);

        $bookshelf = Bookshelf::create([
            'user_id' => auth()->id(),
            'name' => $validated['name'],
            'description' => $validated['description'] ?? null,
            'is_public' => $validated['is_public'] ?? true,
        ]);

        return response()->json($bookshelf, 201);
    }

    public function update(Request $request, Bookshelf $bookshelf): JsonResponse
    {
        $this->authorize('update', $bookshelf);

        $validated = $request->validate([
            'name' => ['sometimes', 'string', 'max:255'],
            'description' => ['nullable', 'string'],
            'is_public' => ['boolean'],
        ]);

        $bookshelf->update($validated);

        return response()->json($bookshelf);
    }

    public function destroy(Bookshelf $bookshelf): JsonResponse
    {
        $this->authorize('delete', $bookshelf);

        $bookshelf->delete();

        return response()->json(['message' => 'Bookshelf deleted successfully']);
    }

    public function addBook(Request $request, Bookshelf $bookshelf): JsonResponse
    {
        $this->authorize('update', $bookshelf);

        $validated = $request->validate([
            'book_id' => ['required', 'exists:books,id'],
            'note' => ['nullable', 'string'],
        ]);

        // Check if book already in bookshelf
        $existing = BookshelfItem::where('bookshelf_id', $bookshelf->id)
            ->where('book_id', $validated['book_id'])
            ->first();

        if ($existing) {
            return response()->json([
                'message' => 'Book already in this bookshelf',
                'item' => $existing,
            ], 422);
        }

        $item = BookshelfItem::create([
            'bookshelf_id' => $bookshelf->id,
            'book_id' => $validated['book_id'],
            'note' => $validated['note'] ?? null,
        ]);

        $item->load('book.author');

        return response()->json($item, 201);
    }

    public function removeBook(Request $request, Bookshelf $bookshelf, Book $book): JsonResponse
    {
        $this->authorize('update', $bookshelf);

        $item = BookshelfItem::where('bookshelf_id', $bookshelf->id)
            ->where('book_id', $book->id)
            ->first();

        if ($item) {
            $item->delete();
        }

        return response()->json(['message' => 'Book removed from bookshelf']);
    }
}

