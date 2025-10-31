<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('audit_logs', function (Blueprint $table) {
            $table->id();
            $table->foreignId('actor_id')->nullable()->constrained('users')->onDelete('set null');
            $table->string('action'); // created, updated, deleted, published, hidden, etc.
            $table->string('target_type'); // App\Models\Book, App\Models\Review, etc.
            $table->unsignedBigInteger('target_id');
            $table->json('meta')->nullable();
            $table->ipAddress('ip_address')->nullable();
            $table->string('user_agent')->nullable();
            $table->timestamps();

            $table->index(['actor_id']);
            $table->index(['target_type', 'target_id']);
            $table->index('created_at');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('audit_logs');
    }
};

