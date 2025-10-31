<?php

namespace Database\Seeders;

use App\Models\Author;
use App\Models\Book;
use App\Models\BookTag;
use App\Models\Publisher;
use App\Models\Series;
use Illuminate\Database\Seeder;

class BookSeeder extends Seeder
{
    public function run(): void
    {
        $authors = Author::all();
        $publishers = Publisher::all();
        $series = Series::all();
        $tags = BookTag::all();

        $books = [
            [
                'author' => 'Nguyễn Du',
                'title' => 'Truyện Kiều',
                'slug' => 'truyen-kieu',
                'description' => 'Tác phẩm kinh điển của văn học Việt Nam',
                'published_year' => 1820,
                'pages' => 800,
                'tags' => ['classic-literature', 'poetry'],
            ],
            [
                'author' => 'Nam Cao',
                'title' => 'Chí Phèo',
                'slug' => 'chi-pheo',
                'description' => 'Truyện ngắn nổi tiếng về số phận con người',
                'published_year' => 1941,
                'pages' => 150,
                'tags' => ['classic-literature', 'fiction'],
            ],
            [
                'author' => 'J.K. Rowling',
                'title' => 'Harry Potter and the Philosopher\'s Stone',
                'slug' => 'harry-potter-philosophers-stone',
                'description' => 'The first book in the Harry Potter series',
                'published_year' => 1997,
                'pages' => 320,
                'series' => 'Harry Potter',
                'tags' => ['fantasy', 'fiction'],
            ],
            [
                'author' => 'George Orwell',
                'title' => '1984',
                'slug' => '1984',
                'description' => 'Dystopian novel about surveillance and oppression',
                'published_year' => 1949,
                'pages' => 328,
                'tags' => ['science-fiction', 'fiction'],
            ],
            [
                'author' => 'Haruki Murakami',
                'title' => 'Norwegian Wood',
                'slug' => 'norwegian-wood',
                'description' => 'A nostalgic story of love and loss',
                'published_year' => 1987,
                'pages' => 296,
                'tags' => ['romance', 'fiction'],
            ],
            [
                'author' => 'Tolkien',
                'title' => 'The Hobbit',
                'slug' => 'the-hobbit',
                'description' => 'Epic fantasy adventure',
                'published_year' => 1937,
                'pages' => 310,
                'series' => 'The Lord of the Rings',
                'tags' => ['fantasy', 'fiction'],
            ],
        ];

        foreach ($books as $bookData) {
            $author = $authors->where('name', $bookData['author'])->first();
            if (!$author) {
                continue;
            }

            $book = Book::create([
                'author_id' => $author->id,
                'publisher_id' => $publishers->random()->id,
                'series_id' => isset($bookData['series']) 
                    ? $series->where('name', $bookData['series'])->first()?->id 
                    : null,
                'title' => $bookData['title'],
                'slug' => $bookData['slug'],
                'description' => $bookData['description'],
                'published_year' => $bookData['published_year'],
                'pages' => $bookData['pages'] ?? null,
                'language' => 'vi',
            ]);

            // Attach tags
            foreach ($bookData['tags'] as $tagSlug) {
                $tag = $tags->where('slug', $tagSlug)->first();
                if ($tag) {
                    $book->tags()->attach($tag->id);
                }
            }
        }
    }
}

