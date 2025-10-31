<?php

namespace Database\Seeders;

use App\Models\Series;
use Illuminate\Database\Seeder;

class SeriesSeeder extends Seeder
{
    public function run(): void
    {
        $series = [
            [
                'name' => 'Harry Potter',
                'slug' => 'harry-potter',
                'description' => 'Series phép thuật nổi tiếng của J.K. Rowling',
            ],
            [
                'name' => 'The Lord of the Rings',
                'slug' => 'the-lord-of-the-rings',
                'description' => 'Epic fantasy trilogy by J.R.R. Tolkien',
            ],
            [
                'name' => 'Chronicles of Narnia',
                'slug' => 'chronicles-of-narnia',
                'description' => 'Fantasy series by C.S. Lewis',
            ],
        ];

        foreach ($series as $serie) {
            Series::create($serie);
        }
    }
}

