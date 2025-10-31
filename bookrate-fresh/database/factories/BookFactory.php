<?php

namespace Database\Factories;

use App\Models\Author;
use App\Models\Book;
use App\Models\Publisher;
use App\Models\Series;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Book>
 */
class BookFactory extends Factory
{
    protected $model = Book::class;

    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'author_id' => Author::factory(),
            'publisher_id' => Publisher::factory(),
            'series_id' => Series::factory(),
            'title' => fake()->sentence(3),
            'language' => 'vi',
            'published_year' => fake()->numberBetween(1900, 2024),
            'pages' => fake()->numberBetween(100, 800),
            'isbn10' => fake()->numerify('##########'),
            'isbn13' => fake()->numerify('##############'),
            'cover_url' => fake()->imageUrl(400, 600, 'books'),
            'description' => fake()->paragraph(5),
            'avg_rating' => 0,
            'ratings_count' => 0,
            'reviews_count' => 0,
        ];
    }
}

