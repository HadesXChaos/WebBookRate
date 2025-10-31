<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Bookshelf extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'name',
        'description',
        'is_public',
    ];

    protected $casts = [
        'is_public' => 'boolean',
    ];

    protected $table = 'bookshelves';

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function items(): HasMany
    {
        return $this->hasMany(BookshelfItem::class, 'bookshelf_id');
    }

    public function publicItems(): HasMany
    {
        if ($this->is_public) {
            return $this->items();
        }
        return $this->items()->whereRaw('1=0'); // Empty result for private bookshelves
    }
}

