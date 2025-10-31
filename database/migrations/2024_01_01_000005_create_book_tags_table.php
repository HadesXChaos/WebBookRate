<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('book_tags', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('slug')->unique()->index();
            $table->text('description')->nullable();
            $table->timestamps();
        });

        Schema::create('book_tag_pivot', function (Blueprint $table) {
            $table->foreignId('book_id')->constrained()->onDelete('cascade');
            $table->foreignId('tag_id')->constrained('book_tags')->onDelete('cascade');
            $table->primary(['book_id', 'tag_id']);
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('book_tag_pivot');
        Schema::dropIfExists('book_tags');
    }
};

