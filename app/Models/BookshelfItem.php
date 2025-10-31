<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class BookshelfItem extends Model
{
    use HasFactory;

    protected $fillable = [
        'bookshelf_id',
        'book_id',
        'note',
        'added_at',
    ];

    protected $casts = [
        'added_at' => 'datetime',
    ];

    protected $table = 'bookshelf_items';

    public function bookshelf(): BelongsTo
    {
        return $this->belongsTo(Bookshelf::class, 'bookshelf_id');
    }

    public function book(): BelongsTo
    {
        return $this->belongsTo(Book::class);
    }
}

