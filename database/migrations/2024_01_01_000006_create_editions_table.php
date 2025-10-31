<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('editions', function (Blueprint $table) {
            $table->id();
            $table->foreignId('book_id')->constrained()->onDelete('cascade');
            $table->string('format')->default('paperback'); // paperback, hardcover, ebook, audiobook
            $table->string('isbn10')->nullable();
            $table->string('isbn13')->nullable();
            $table->integer('published_year')->nullable();
            $table->integer('pages')->nullable();
            $table->string('cover_url')->nullable();
            $table->timestamps();

            $table->index(['book_id', 'format']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('editions');
    }
};

