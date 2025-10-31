<?php

namespace Database\Seeders;

use App\Models\BookTag;
use Illuminate\Database\Seeder;

class BookTagSeeder extends Seeder
{
    public function run(): void
    {
        $tags = [
            ['name' => 'Fiction', 'slug' => 'fiction', 'description' => 'Thể loại tiểu thuyết'],
            ['name' => 'Non-Fiction', 'slug' => 'non-fiction', 'description' => 'Phi hư cấu'],
            ['name' => 'Fantasy', 'slug' => 'fantasy', 'description' => 'Giả tưởng'],
            ['name' => 'Science Fiction', 'slug' => 'science-fiction', 'description' => 'Khoa học viễn tưởng'],
            ['name' => 'Mystery', 'slug' => 'mystery', 'description' => 'Trinh thám'],
            ['name' => 'Romance', 'slug' => 'romance', 'description' => 'Lãng mạn'],
            ['name' => 'Horror', 'slug' => 'horror', 'description' => 'Kinh dị'],
            ['name' => 'Historical Fiction', 'slug' => 'historical-fiction', 'description' => 'Lịch sử'],
            ['name' => 'Biography', 'slug' => 'biography', 'description' => 'Tiểu sử'],
            ['name' => 'Self-Help', 'slug' => 'self-help', 'description' => 'Tự lực'],
            ['name' => 'Philosophy', 'slug' => 'philosophy', 'description' => 'Triết học'],
            ['name' => 'Classic Literature', 'slug' => 'classic-literature', 'description' => 'Văn học kinh điển'],
        ];

        foreach ($tags as $tag) {
            BookTag::create($tag);
        }
    }
}

