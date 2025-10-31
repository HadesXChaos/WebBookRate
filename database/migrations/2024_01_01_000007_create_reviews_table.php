<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('reviews', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->foreignId('book_id')->constrained()->onDelete('cascade');
            $table->foreignId('edition_id')->nullable()->constrained()->onDelete('set null');
            $table->string('title')->nullable();
            $table->text('body_md')->nullable();
            $table->text('body_html')->nullable();
            $table->decimal('rating', 2, 1); // 0.5 to 5.0
            $table->boolean('is_spoiler')->default(false);
            $table->enum('status', ['pending', 'published', 'hidden'])->default('published')->index();
            $table->unsignedInteger('helpful_count')->default(0);
            $table->timestamps();

            $table->unique(['user_id', 'book_id', 'edition_id'], 'unique_user_book_edition_review');
            $table->index(['book_id', 'status']);
            $table->index(['user_id']);
            $table->fullText(['title', 'body_html']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('reviews');
    }
};

