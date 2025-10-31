<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('comments', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->foreignId('review_id')->nullable()->constrained()->onDelete('cascade');
            $table->foreignId('book_id')->nullable()->constrained()->onDelete('cascade');
            $table->text('body_md');
            $table->text('body_html');
            $table->boolean('is_spoiler')->default(false);
            $table->enum('status', ['published', 'hidden'])->default('published');
            $table->timestamps();

            $table->index(['review_id']);
            $table->index(['book_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('comments');
    }
};

