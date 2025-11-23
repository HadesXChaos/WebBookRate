#!/bin/bash
set -e

export DJANGO_SETTINGS_MODULE=bookreview.settings

echo "Đang chờ PostgreSQL..."
for i in {1..30}; do
    pg_isready -h db -p 5432 >/dev/null 2>&1 && break
    echo "Đang chờ DB... ($i/30)"
    sleep 1
done

if [ $i -eq 31 ]; then
    echo "DB timeout!"
    exit 1
fi

echo "DB đã sẵn sàng!"

python manage.py migrate --no-input

# Kiểm tra và seed sách
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookreview.settings')
import django
django.setup()
from books.models import Book
if not Book.objects.exists():
    print('Đang import sách...')
    os.system('python seed_data.py')
else:
    print(f'ĐÃ CÓ {Book.objects.count()} cuốn sách → Bỏ qua')
"

# Tạo admin
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookreview.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@book.com', '123')
    print('Tạo admin: admin /Pass: 123')
" || true

echo "Khởi động ứng dụng..."
exec "$@"