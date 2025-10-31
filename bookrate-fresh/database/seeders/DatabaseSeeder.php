<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $this->call([
            UserSeeder::class,
            AuthorSeeder::class,
            PublisherSeeder::class,
            SeriesSeeder::class,
            BookTagSeeder::class,
            BookSeeder::class,
        ]);
    }
}

