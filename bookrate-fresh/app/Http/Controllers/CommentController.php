<?php

namespace App\Http\Controllers;

use App\Models\Comment;
use App\Models\Review;
use App\Models\Book;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class CommentController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $query = Comment::with(['user']);

        if ($request->has('review_id')) {
            $query->where('review_id', $request->review_id);
        }

        if ($request->has('book_id')) {
            $query->where('book_id', $request->book_id);
        }

        $comments = $query->where('status', 'published')
            ->orderBy('created_at', 'desc')
            ->paginate($request->get('per_page', 20));

        return response()->json($comments);
    }

    public function show(Comment $comment): JsonResponse
    {
        $comment->load(['user', 'review', 'book']);

        return response()->json($comment);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'review_id' => ['nullable', 'exists:reviews,id'],
            'book_id' => ['nullable', 'exists:books,id'],
            'body_md' => ['required', 'string', 'min:5'],
            'is_spoiler' => ['boolean'],
        ]);

        // Must specify either review_id or book_id
        if (!$request->has('review_id') && !$request->has('book_id')) {
            return response()->json([
                'message' => 'Either review_id or book_id must be provided',
            ], 422);
        }

        $comment = Comment::create([
            'user_id' => auth()->id(),
            'review_id' => $validated['review_id'] ?? null,
            'book_id' => $validated['book_id'] ?? null,
            'body_md' => $validated['body_md'],
            'is_spoiler' => $validated['is_spoiler'] ?? false,
            'status' => 'published',
        ]);

        $comment->load('user');

        return response()->json($comment, 201);
    }

    public function update(Request $request, Comment $comment): JsonResponse
    {
        $validated = $request->validate([
            'body_md' => ['sometimes', 'string', 'min:5'],
            'is_spoiler' => ['boolean'],
        ]);

        $comment->update($validated);

        return response()->json($comment);
    }

    public function destroy(Comment $comment): JsonResponse
    {
        $comment->delete();

        return response()->json(['message' => 'Comment deleted successfully']);
    }
}

