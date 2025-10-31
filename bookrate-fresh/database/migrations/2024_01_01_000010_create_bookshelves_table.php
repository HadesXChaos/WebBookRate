<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('bookshelves', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->string('name');
            $table->text('description')->nullable();
            $table->boolean('is_public')->default(true);
            $table->timestamps();

            $table->index(['user_id', 'is_public']);
        });

        Schema::create('bookshelf_items', function (Blueprint $table) {
            $table->id();
            $table->foreignId('bookshelf_id')->constrained()->onDelete('cascade');
            $table->foreignId('book_id')->constrained()->onDelete('cascade');
            $table->text('note')->nullable();
            $table->timestamp('added_at')->useCurrent();
            $table->timestamps();

            $table->unique(['bookshelf_id', 'book_id']);
            $table->index(['bookshelf_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('bookshelf_items');
        Schema::dropIfExists('bookshelves');
    }
};

