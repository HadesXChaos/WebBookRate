<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('books', function (Blueprint $table) {
            $table->id();
            $table->foreignId('author_id')->constrained()->onDelete('restrict');
            $table->foreignId('publisher_id')->nullable()->constrained()->onDelete('set null');
            $table->foreignId('series_id')->nullable()->constrained()->onDelete('set null');
            $table->string('title');
            $table->string('slug')->unique()->index();
            $table->string('language')->default('vi');
            $table->integer('published_year')->nullable();
            $table->integer('pages')->nullable();
            $table->string('isbn10')->nullable();
            $table->string('isbn13')->nullable();
            $table->string('cover_url')->nullable();
            $table->text('description')->nullable();
            $table->decimal('avg_rating', 3, 2)->default(0)->index();
            $table->unsignedInteger('ratings_count')->default(0);
            $table->unsignedInteger('reviews_count')->default(0);
            $table->timestamps();

            $table->index('published_year');
            $table->fullText(['title', 'description']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('books');
    }
};

