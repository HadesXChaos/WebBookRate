#!/bin/bash
set -e

echo "Đang chờ PostgreSQL..."
while ! nc -z db 5432; do sleep 1; done
echo "PostgreSQL sẵn sàng!"

# Chỉ chạy migrate và seed data ở container WEB
if [ "$1" != "celery" ] && [[ "$1" != *"beat"* ]]; then

    echo ">>> Đang chạy Migration..."
    python manage.py migrate --noinput

    # 1. CHẠY SEED DATA TRƯỚC (Để có sách)
    if [ -f seed_data.py ]; then
        echo ">>> CHẠY SEED DATA (Sách & Tác giả)..."
        python seed_data.py
    fi

    # 2. TẠO USERS VÀ REVIEWS
    echo ">>> Đang tạo Users và Reviews mẫu..."
    python <<END
import os, django
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookreview.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import Profile
from shelves.models import Shelf
from reviews.models import Review
from books.models import Book, Author

User = get_user_model()

def create_default_shelves(user):
    default_shelves = [
        {'name': 'Want to Read', 'system_type': 'WTR'},
        {'name': 'Currently Reading', 'system_type': 'READING'},
        {'name': 'Read', 'system_type': 'READ'},
    ]
    for shelf_data in default_shelves:
        Shelf.objects.get_or_create(
            user=user,
            system_type=shelf_data['system_type'],
            defaults={'name': shelf_data['name'], 'visibility': 'public'}
        )

# --- 1. Tạo Superuser ---
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser(
        username='admin', email='admin@example.com', password='123', 
        role='admin', first_name='Super', last_name='Admin', is_verified=True
    )
    if not hasattr(admin_user, 'profile'): Profile.objects.create(user=admin_user)
    admin_user.profile.bio = "Quản trị viên"; admin_user.profile.save()
    create_default_shelves(admin_user)
    print(">>> TẠO ADMIN: admin / 123")

# --- 2. Tạo Users ---
users_to_create = [
    {'username': 'reviewer1', 'role': 'reviewer', 'email': 'reviewer1@gmail.com', 'name': 'Reviewer Một'},
    {'username': 'reviewer2', 'role': 'reviewer', 'email': 'reviewer2@gmail.com', 'name': 'Reviewer Hai'},
    {'username': 'reader1',   'role': 'reader',   'email': 'reader1@gmail.com',   'name': 'Reader Một'},
    {'username': 'reader2',   'role': 'reader',   'email': 'reader2@gmail.com',   'name': 'Reader Hai'},
    {'username': 'reader3',   'role': 'reader',   'email': 'reader3@gmail.com',   'name': 'Reader Ba (Sắp thăng hạng)'},
]

for u_data in users_to_create:
    if not User.objects.filter(username=u_data['username']).exists():
        user = User.objects.create_user(
            username=u_data['username'], email=u_data['email'], password='123',
            first_name=u_data['name'].split()[0], last_name=" ".join(u_data['name'].split()[1:]),
            role=u_data['role'], is_active=True, is_verified=True
        )
        if not hasattr(user, 'profile'): Profile.objects.create(user=user)
        user.profile.bio = f"Thành viên {u_data['username']}"; user.profile.location = "VN"; user.profile.save()
        create_default_shelves(user)
        print(f">>> TẠO USER: {u_data['username']}")

# --- 3. Logic Tạo Review (Dùng sách có sẵn) ---
def create_reviews_for_user(username, count):
    try:
        user = User.objects.get(username=username)
        
        available_books = list(Book.objects.exclude(reviews__user=user))
        random.shuffle(available_books)
        
        needed = count
        
        if needed > 0:
            print(f"--- {username} cần tạo {count} reviews. Sách khả dụng: {len(available_books)} ---")

            for i in range(min(len(available_books), count)):
                book = available_books[i]
                Review.objects.get_or_create(
                    user=user,
                    book=book,
                    defaults={
                        'title': f"Review về {book.title}",
                        'body_md': f"Sách '{book.title}' rất hay. Đây là bài review số {i+1} của tôi.",
                        'rating': random.choice([3, 4, 5]),
                        'status': 'public',
                        'is_active': True # <--- ĐÃ SỬA LỖI CHÍNH TẢ Ở ĐÂY
                    }
                )
                needed -= 1

            if needed > 0:
                print(f"!!! Thiếu {needed} sách. Đang tạo thêm sách bổ sung cho {username}...")
                dummy_author, _ = Author.objects.get_or_create(name="Tác giả Bổ Sung")
                
                for k in range(needed):
                    rand_suffix = random.randint(1000, 9999)
                    new_book = Book.objects.create(
                        title=f"Sách Bổ Sung {k+1}-{rand_suffix} cho {username}",
                        description="Sách được tạo tự động để đủ KPI review.",
                        pages=100
                    )
                    new_book.authors.add(dummy_author)
                    
                    Review.objects.create(
                        user=user,
                        book=new_book,
                        title=f"Review bổ sung {k+1}",
                        body_md="Bài viết để đủ số lượng thăng hạng.",
                        rating=5,
                        status='public',
                        is_active=True
                    )

    except User.DoesNotExist:
        print(f"User {username} không tồn tại.")

# Thực hiện
create_reviews_for_user('reader3', 19)
create_reviews_for_user('reviewer1', 2)
create_reviews_for_user('reviewer2', 2)

print(">>> HOÀN TẤT <<<")
END

fi 

exec "$@"