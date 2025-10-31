<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class ReadingStatus extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'book_id',
        'status',
        'started_at',
        'finished_at',
        'progress_pages',
    ];

    protected $casts = [
        'started_at' => 'date',
        'finished_at' => 'date',
        'progress_pages' => 'integer',
    ];

    protected $table = 'reading_statuses';

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function book(): BelongsTo
    {
        return $this->belongsTo(Book::class);
    }
}

