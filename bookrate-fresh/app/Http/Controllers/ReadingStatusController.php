<?php

namespace App\Http\Controllers;

use App\Models\ReadingStatus;
use App\Models\Book;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class ReadingStatusController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $query = ReadingStatus::where('user_id', auth()->id())
            ->with(['book.author']);

        if ($request->has('status')) {
            $query->where('status', $request->status);
        }

        $readingStatuses = $query->orderBy('updated_at', 'desc')
            ->paginate($request->get('per_page', 20));

        return response()->json($readingStatuses);
    }

    public function show(ReadingStatus $readingStatus): JsonResponse
    {
        $this->authorize('view', $readingStatus);

        $readingStatus->load(['book.author', 'user']);

        return response()->json($readingStatus);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'book_id' => ['required', 'exists:books,id'],
            'status' => ['required', 'in:want,reading,read,abandoned'],
            'started_at' => ['nullable', 'date'],
            'finished_at' => ['nullable', 'date'],
            'progress_pages' => ['nullable', 'integer', 'min:0'],
        ]);

        // Check if status already exists
        $existing = ReadingStatus::where('user_id', auth()->id())
            ->where('book_id', $validated['book_id'])
            ->first();

        if ($existing) {
            $existing->update($validated);
            $readingStatus = $existing;
        } else {
            $readingStatus = ReadingStatus::create([
                'user_id' => auth()->id(),
                'book_id' => $validated['book_id'],
                'status' => $validated['status'],
                'started_at' => $validated['started_at'] ?? null,
                'finished_at' => $validated['finished_at'] ?? null,
                'progress_pages' => $validated['progress_pages'] ?? null,
            ]);
        }

        $readingStatus->load(['book.author']);

        return response()->json($readingStatus, 201);
    }

    public function update(Request $request, ReadingStatus $readingStatus): JsonResponse
    {
        $this->authorize('update', $readingStatus);

        $validated = $request->validate([
            'status' => ['sometimes', 'in:want,reading,read,abandoned'],
            'started_at' => ['nullable', 'date'],
            'finished_at' => ['nullable', 'date'],
            'progress_pages' => ['nullable', 'integer', 'min:0'],
        ]);

        $readingStatus->update($validated);
        $readingStatus->load(['book.author']);

        return response()->json($readingStatus);
    }

    public function destroy(ReadingStatus $readingStatus): JsonResponse
    {
        $this->authorize('delete', $readingStatus);

        $readingStatus->delete();

        return response()->json(['message' => 'Reading status deleted successfully']);
    }
}

