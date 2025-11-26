#!/bin/bash
set -e

echo "Đang chờ PostgreSQL..."
while ! nc -z db 5432; do sleep 1; done
echo "PostgreSQL sẵn sàng!"

python manage.py migrate --noinput

# Tạo admin
python <<END
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookreview.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', '123')
    print("TẠO ADMIN: admin / 123")
else:
    print("Admin đã tồn tại")
END

if [ "$1" != "celery" ] && [[ "$1" != *"beat"* ]]; then
    if [ -f seed_data.py ]; then
        echo "CHẠY SEED DATA..."
        python seed_data.py
    fi
fi

exec "$@"