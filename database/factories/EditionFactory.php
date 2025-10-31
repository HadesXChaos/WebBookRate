<?php

namespace Database\Factories;

use App\Models\Book;
use App\Models\Edition;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Edition>
 */
class EditionFactory extends Factory
{
    protected $model = Edition::class;

    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'book_id' => Book::factory(),
            'format' => fake()->randomElement(['paperback', 'hardcover', 'ebook', 'audiobook']),
            'isbn10' => fake()->numerify('##########'),
            'isbn13' => fake()->numerify('##############'),
            'published_year' => fake()->numberBetween(1900, 2024),
            'pages' => fake()->numberBetween(100, 800),
            'cover_url' => fake()->imageUrl(400, 600, 'books'),
        ];
    }
}

