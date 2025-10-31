<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class UserSeeder extends Seeder
{
    public function run(): void
    {
        // Admin user
        User::create([
            'name' => 'Admin',
            'email' => 'admin@bookrate.local',
            'password' => Hash::make('password'),
            'role' => 'admin',
            'is_active' => true,
            'email_verified_at' => now(),
        ]);

        // Moderator user
        User::create([
            'name' => 'Moderator',
            'email' => 'moderator@bookrate.local',
            'password' => Hash::make('password'),
            'role' => 'moderator',
            'is_active' => true,
            'email_verified_at' => now(),
        ]);

        // Regular users
        User::factory()->count(10)->create([
            'role' => 'user',
            'is_active' => true,
            'email_verified_at' => now(),
        ]);
    }
}

