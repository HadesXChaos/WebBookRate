<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('authors', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('slug')->unique()->index();
            $table->text('bio')->nullable();
            $table->date('birthday')->nullable();
            $table->string('country')->nullable();
            $table->string('photo_url')->nullable();
            $table->timestamps();

            $table->fullText(['name']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('authors');
    }
};

