<?php

namespace Database\Factories;

use App\Models\Author;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Author>
 */
class AuthorFactory extends Factory
{
    protected $model = Author::class;

    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'name' => fake()->name(),
            'bio' => fake()->optional()->paragraph(2),
            'birthday' => fake()->optional()->date('Y-m-d', '-10 years'),
            'country' => fake()->country(),
            'photo_url' => fake()->optional()->imageUrl(200, 200),
        ];
    }
}

