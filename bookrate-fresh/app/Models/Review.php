<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use League\CommonMark\CommonMarkConverter;

class Review extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'book_id',
        'edition_id',
        'title',
        'body_md',
        'body_html',
        'rating',
        'is_spoiler',
        'status',
        'helpful_count',
    ];

    protected $casts = [
        'rating' => 'decimal:1',
        'is_spoiler' => 'boolean',
        'helpful_count' => 'integer',
    ];

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function book(): BelongsTo
    {
        return $this->belongsTo(Book::class);
    }

    public function edition(): BelongsTo
    {
        return $this->belongsTo(Edition::class);
    }

    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }

    public function reactions(): HasMany
    {
        return $this->hasMany(Reaction::class);
    }

    public function scopePublished($query)
    {
        return $query->where('status', 'published');
    }

    public function scopeWithSpoiler($query, bool $include = true)
    {
        return $query->where('is_spoiler', $include);
    }

    protected static function boot()
    {
        parent::boot();

        static::creating(function ($review) {
            if ($review->body_md) {
                $converter = new CommonMarkConverter([
                    'html_input' => 'strip',
                    'allow_unsafe_links' => false,
                ]);
                $review->body_html = $converter->convert($review->body_md)->getContent();
            }
        });

        static::updating(function ($review) {
            if ($review->isDirty('body_md')) {
                $converter = new CommonMarkConverter([
                    'html_input' => 'strip',
                    'allow_unsafe_links' => false,
                ]);
                $review->body_html = $converter->convert($review->body_md)->getContent();
            }
        });
    }
}

