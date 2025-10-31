<?php

namespace Database\Seeders;

use App\Models\Publisher;
use Illuminate\Database\Seeder;

class PublisherSeeder extends Seeder
{
    public function run(): void
    {
        $publishers = [
            [
                'name' => 'NXB Văn Học',
                'slug' => 'nxb-van-hoc',
                'website' => 'https://nxbvanhoc.com.vn',
                'description' => 'Nhà xuất bản chuyên về văn học Việt Nam',
            ],
            [
                'name' => 'NXB Trẻ',
                'slug' => 'nxb-tre',
                'website' => 'https://nxbtre.com.vn',
                'description' => 'Nhà xuất bản dành cho thanh thiếu niên',
            ],
            [
                'name' => 'Bloomsbury',
                'slug' => 'bloomsbury',
                'website' => 'https://www.bloomsbury.com',
                'description' => 'British publishing house',
            ],
            [
                'name' => 'Penguin Random House',
                'slug' => 'penguin-random-house',
                'website' => 'https://www.penguinrandomhouse.com',
                'description' => 'Major publishing house',
            ],
        ];

        foreach ($publishers as $publisher) {
            Publisher::create($publisher);
        }
    }
}

