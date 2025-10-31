<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('follows', function (Blueprint $table) {
            $table->id();
            $table->foreignId('follower_id')->constrained('users')->onDelete('cascade');
            $table->foreignId('target_user_id')->nullable()->constrained('users')->onDelete('cascade');
            $table->foreignId('author_id')->nullable()->constrained()->onDelete('cascade');
            $table->foreignId('book_id')->nullable()->constrained()->onDelete('cascade');
            $table->timestamps();

            $table->unique(['follower_id', 'target_user_id'], 'unique_follow_user');
            $table->unique(['follower_id', 'author_id'], 'unique_follow_author');
            $table->unique(['follower_id', 'book_id'], 'unique_follow_book');
            $table->index(['follower_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('follows');
    }
};

