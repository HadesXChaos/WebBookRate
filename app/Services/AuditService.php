<?php

namespace App\Services;

use App\Models\AuditLog;
use App\Models\User;

class AuditService
{
    public function log(
        ?User $actor,
        string $action,
        string $targetType,
        int $targetId,
        ?array $meta = null
    ): AuditLog {
        return AuditLog::create([
            'actor_id' => $actor?->id,
            'action' => $action,
            'target_type' => $targetType,
            'target_id' => $targetId,
            'meta' => $meta,
            'ip_address' => request()->ip(),
            'user_agent' => request()->userAgent(),
        ]);
    }
}

