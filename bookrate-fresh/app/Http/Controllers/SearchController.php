<?php

namespace App\Http\Controllers;

use App\Services\SearchService;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class SearchController extends Controller
{
    public function __construct(
        private SearchService $searchService
    ) {}

    public function search(Request $request): JsonResponse
    {
        $request->validate([
            'q' => ['required', 'string', 'min:1'],
            'type' => ['nullable', 'in:books,authors,reviews,all'],
            'page' => ['nullable', 'integer', 'min:1'],
            'per_page' => ['nullable', 'integer', 'min:1', 'max:100'],
        ]);

        $type = $request->get('type', 'all');
        $query = $request->get('q');

        if ($type === 'books' || $type === 'all') {
            $books = $this->searchService->searchBooks(
                ['page' => $request->get('page', 1), 'per_page' => $request->get('per_page', 20)],
                $query
            );

            if ($type === 'books') {
                return response()->json([
                    'type' => 'books',
                    'query' => $query,
                    'results' => $books,
                ]);
            }
        }

        if ($type === 'authors' || $type === 'all') {
            $authors = $this->searchService->searchAuthors($query);

            if ($type === 'authors') {
                return response()->json([
                    'type' => 'authors',
                    'query' => $query,
                    'results' => $authors,
                ]);
            }
        }

        if ($type === 'reviews' || $type === 'all') {
            $reviews = $this->searchService->searchReviews(
                ['per_page' => $request->get('per_page', 20)],
                $query
            );

            if ($type === 'reviews') {
                return response()->json([
                    'type' => 'reviews',
                    'query' => $query,
                    'results' => $reviews,
                ]);
            }
        }

        // Return combined results for 'all'
        return response()->json([
            'type' => 'all',
            'query' => $query,
            'results' => [
                'books' => $books ?? [],
                'authors' => $authors ?? [],
                'reviews' => $reviews ?? [],
            ],
        ]);
    }
}

