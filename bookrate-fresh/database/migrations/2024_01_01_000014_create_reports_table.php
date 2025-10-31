<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('reports', function (Blueprint $table) {
            $table->id();
            $table->foreignId('reporter_id')->constrained('users')->onDelete('cascade');
            $table->string('target_type'); // App\Models\Review, App\Models\Comment, etc.
            $table->unsignedBigInteger('target_id');
            $table->string('reason'); // spam, harassment, inappropriate, etc.
            $table->text('note')->nullable();
            $table->enum('status', ['open', 'reviewing', 'resolved'])->default('open')->index();
            $table->timestamps();

            $table->index(['target_type', 'target_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('reports');
    }
};

