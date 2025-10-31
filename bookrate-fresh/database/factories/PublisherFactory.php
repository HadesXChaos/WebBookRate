<?php

namespace Database\Factories;

use App\Models\Publisher;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Publisher>
 */
class PublisherFactory extends Factory
{
    protected $model = Publisher::class;

    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'name' => 'NXB ' . fake()->company(),
            'website' => fake()->url(),
            'description' => fake()->optional()->sentence(),
            'logo_url' => fake()->optional()->imageUrl(150, 150),
        ];
    }
}

