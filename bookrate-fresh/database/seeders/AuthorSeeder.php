<?php

namespace Database\Seeders;

use App\Models\Author;
use Illuminate\Database\Seeder;

class AuthorSeeder extends Seeder
{
    public function run(): void
    {
        $authors = [
            [
                'name' => 'Nguyễn Du',
                'slug' => 'nguyen-du',
                'bio' => 'Nhà thơ nổi tiếng của Việt Nam, tác giả Truyện Kiều',
                'country' => 'Việt Nam',
            ],
            [
                'name' => 'Nam Cao',
                'slug' => 'nam-cao',
                'bio' => 'Nhà văn hiện thực Việt Nam',
                'country' => 'Việt Nam',
            ],
            [
                'name' => 'J.K. Rowling',
                'slug' => 'j-k-rowling',
                'bio' => 'Tác giả nổi tiếng thế giới với series Harry Potter',
                'country' => 'UK',
            ],
            [
                'name' => 'George Orwell',
                'slug' => 'george-orwell',
                'bio' => 'Nhà văn, nhà báo, nhà phê bình người Anh',
                'country' => 'UK',
            ],
            [
                'name' => 'Haruki Murakami',
                'slug' => 'haruki-murakami',
                'bio' => 'Tiểu thuyết gia người Nhật Bản nổi tiếng thế giới',
                'country' => 'Japan',
            ],
            [
                'name' => 'Tolkien',
                'slug' => 'j-r-r-tolkien',
                'bio' => 'Nhà văn, nhà ngôn ngữ học, giáo sư người Anh',
                'country' => 'UK',
            ],
        ];

        foreach ($authors as $author) {
            Author::create($author);
        }
    }
}

