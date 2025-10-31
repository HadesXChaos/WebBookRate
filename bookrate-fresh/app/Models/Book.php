<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Spatie\Sluggable\HasSlug;
use Spatie\Sluggable\SlugOptions;

class Book extends Model
{
    use HasFactory, HasSlug;

    protected $fillable = [
        'author_id',
        'publisher_id',
        'series_id',
        'title',
        'slug',
        'language',
        'published_year',
        'pages',
        'isbn10',
        'isbn13',
        'cover_url',
        'description',
        'avg_rating',
        'ratings_count',
        'reviews_count',
    ];

    protected $casts = [
        'avg_rating' => 'decimal:2',
        'published_year' => 'integer',
        'pages' => 'integer',
        'ratings_count' => 'integer',
        'reviews_count' => 'integer',
    ];

    public function getSlugOptions(): SlugOptions
    {
        return SlugOptions::create()
            ->generateSlugsFrom('title')
            ->saveSlugsTo('slug');
    }

    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }

    public function publisher(): BelongsTo
    {
        return $this->belongsTo(Publisher::class);
    }

    public function series(): BelongsTo
    {
        return $this->belongsTo(Series::class);
    }

    public function editions(): HasMany
    {
        return $this->hasMany(Edition::class);
    }

    public function tags(): BelongsToMany
    {
        return $this->belongsToMany(BookTag::class, 'book_tag_pivot', 'book_id', 'tag_id');
    }

    public function reviews(): HasMany
    {
        return $this->hasMany(Review::class);
    }

    public function publishedReviews(): HasMany
    {
        return $this->hasMany(Review::class)->where('status', 'published');
    }

    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }

    public function readingStatuses(): HasMany
    {
        return $this->hasMany(ReadingStatus::class);
    }

    public function bookshelfItems(): HasMany
    {
        return $this->hasMany(BookshelfItem::class);
    }

    public function follows(): HasMany
    {
        return $this->hasMany(Follow::class);
    }

    public function scopePopular($query)
    {
        return $query->orderBy('reviews_count', 'desc')
            ->orderBy('avg_rating', 'desc');
    }

    public function scopeTrending($query)
    {
        return $query->whereHas('reviews', function ($q) {
            $q->where('created_at', '>=', now()->subDays(30));
        })->orderBy('reviews_count', 'desc');
    }

    public function scopeHighRated($query)
    {
        return $query->where('avg_rating', '>=', 4.0)
            ->where('ratings_count', '>=', 10)
            ->orderBy('avg_rating', 'desc');
    }
}

