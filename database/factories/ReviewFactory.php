<?php

namespace Database\Factories;

use App\Models\Book;
use App\Models\Edition;
use App\Models\Review;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Review>
 */
class ReviewFactory extends Factory
{
    protected $model = Review::class;

    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'user_id' => User::factory(),
            'book_id' => Book::factory(),
            'edition_id' => Edition::factory(),
            'title' => fake()->optional()->sentence(),
            'body_md' => fake()->paragraphs(3, true),
            'rating' => fake()->randomElement([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]),
            'is_spoiler' => fake()->boolean(20),
            'status' => 'published',
            'helpful_count' => fake()->numberBetween(0, 100),
        ];
    }
}

