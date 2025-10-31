<?php

namespace App\Http\Controllers;

use App\Models\Reaction;
use App\Models\Review;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\DB;

class ReactionController extends Controller
{
    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'review_id' => ['required', 'exists:reviews,id'],
            'type' => ['required', 'in:helpful,like,insightful'],
        ]);

        $review = Review::findOrFail($validated['review_id']);

        // Check if user already reacted
        $existingReaction = Reaction::where('user_id', auth()->id())
            ->where('review_id', $review->id)
            ->first();

        if ($existingReaction) {
            // Update existing reaction
            $existingReaction->update(['type' => $validated['type']]);
        } else {
            // Create new reaction
            $reaction = Reaction::create([
                'user_id' => auth()->id(),
                'review_id' => $review->id,
                'type' => $validated['type'],
            ]);
        }

        // Update helpful_count on review
        $helpfulCount = Reaction::where('review_id', $review->id)
            ->where('type', 'helpful')
            ->count();

        $review->update(['helpful_count' => $helpfulCount]);

        return response()->json([
            'message' => 'Reaction added successfully',
            'helpful_count' => $helpfulCount,
        ]);
    }

    public function destroy(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'review_id' => ['required', 'exists:reviews,id'],
        ]);

        $reaction = Reaction::where('user_id', auth()->id())
            ->where('review_id', $validated['review_id'])
            ->first();

        if ($reaction) {
            $reaction->delete();

            // Update helpful_count
            $review = Review::findOrFail($validated['review_id']);
            $helpfulCount = Reaction::where('review_id', $review->id)
                ->where('type', 'helpful')
                ->count();

            $review->update(['helpful_count' => $helpfulCount]);

            return response()->json([
                'message' => 'Reaction removed successfully',
                'helpful_count' => $helpfulCount,
            ]);
        }

        return response()->json(['message' => 'Reaction not found'], 404);
    }

    public function toggle(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'review_id' => ['required', 'exists:reviews,id'],
            'type' => ['required', 'in:helpful,like,insightful'],
        ]);

        $existingReaction = Reaction::where('user_id', auth()->id())
            ->where('review_id', $validated['review_id'])
            ->first();

        if ($existingReaction) {
            // Remove existing reaction
            $existingReaction->delete();
            $action = 'removed';
        } else {
            // Add new reaction
            Reaction::create([
                'user_id' => auth()->id(),
                'review_id' => $validated['review_id'],
                'type' => $validated['type'],
            ]);
            $action = 'added';
        }

        // Update helpful_count
        $review = Review::findOrFail($validated['review_id']);
        $helpfulCount = Reaction::where('review_id', $review->id)
            ->where('type', 'helpful')
            ->count();

        $review->update(['helpful_count' => $helpfulCount]);

        return response()->json([
            'message' => "Reaction {$action} successfully",
            'helpful_count' => $helpfulCount,
        ]);
    }
}

