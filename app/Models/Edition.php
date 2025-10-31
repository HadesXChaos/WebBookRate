<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Edition extends Model
{
    use HasFactory;

    protected $fillable = [
        'book_id',
        'format',
        'isbn10',
        'isbn13',
        'published_year',
        'pages',
        'cover_url',
    ];

    protected $casts = [
        'published_year' => 'integer',
        'pages' => 'integer',
    ];

    public function book(): BelongsTo
    {
        return $this->belongsTo(Book::class);
    }

    public function reviews(): HasMany
    {
        return $this->hasMany(Review::class);
    }
}

