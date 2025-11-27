#!/bin/bash
set -e

echo "Đang chờ PostgreSQL..."
while ! nc -z db 5432; do sleep 1; done
echo "PostgreSQL sẵn sàng!"

# Chỉ chạy migrate và seed data ở container WEB
if [ "$1" != "celery" ] && [[ "$1" != *"beat"* ]]; then

    echo ">>> Đang chạy Migration..."
    python manage.py migrate --noinput

    # 1. CHẠY SEED DATA TRƯỚC
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
    admin_user.profile.bio = "Quản trị viên hệ thống"; 
    admin_user.profile.location = "Hệ thống";
    admin_user.profile.save()
    create_default_shelves(admin_user)
    print(">>> TẠO ADMIN: admin / 123")

# --- 2. Tạo Users ---
users_to_create = [
    {'username': 'reviewer1', 'role': 'reviewer', 'email': 'reviewer1@gmail.com', 'name': 'Reviewer Một'},
    {'username': 'reviewer2', 'role': 'reviewer', 'email': 'reviewer2@gmail.com', 'name': 'Reviewer Hai'},
    {'username': 'reader1',   'role': 'reader',   'email': 'reader1@gmail.com',   'name': 'Reader Một'},
    {'username': 'reader2',   'role': 'reader',   'email': 'reader2@gmail.com',   'name': 'Reader Hai'},
    {'username': 'reader3',   'role': 'reader',   'email': 'reader3@gmail.com',   'name': 'Reader Ba (Sắp thăng hạng)'},
    {'username': 'bang', 'role': 'reviewer', 'email': 'bang@gmail.com', 'name': 'Le Duy Bang'},
    {'username': 'hoang', 'role': 'reviewer', 'email': 'hoang@gmail.com', 'name': 'Nguyen Huy Hoang'},
    {'username': 'phi', 'role': 'reviewer', 'email': 'phi@gmail.com', 'name': 'Nguyen Hoang Phi'},
    {'username': 'toai', 'role': 'reviewer', 'email': 'toai@gmail.com', 'name': 'Nguyen Anh Toai'},
    {'username': 'tho', 'role': 'reviewer', 'email': 'tho@gmail.com', 'name': 'Truong Le Bao Tho'},
]

for u_data in users_to_create:
    if not User.objects.filter(username=u_data['username']).exists():
        user = User.objects.create_user(
            username=u_data['username'], 
            email=u_data['email'], 
            password='123',
            first_name=u_data['name'].split()[0], 
            last_name=" ".join(u_data['name'].split()[1:]),
            role=u_data['role'], 
            is_active=True, 
            is_verified=True
        )
        if not hasattr(user, 'profile'): Profile.objects.create(user=user)
        user.profile.bio = f"Xin chào, tôi là {u_data['username']}."; user.profile.location = "Việt Nam"; user.profile.save()
        create_default_shelves(user)
        print(f">>> TẠO USER: {u_data['username']}")

def create_reviews_for_user(username, target_count, specific_book_slugs=None):
    try:
        user = User.objects.get(username=username)
        if specific_book_slugs is None:
            specific_book_slugs = []

        if specific_book_slugs:
            print(f"--- Đang tạo review cho {username}... ---")
            for slug in specific_book_slugs:
                try:
                    book = Book.objects.get(slug=slug)
                    
                    # Cắt ngắn title nếu quá dài
                    short_title = (book.title[:100] + '...') if len(book.title) > 100 else book.title
                    
                    Review.objects.get_or_create(
                        user=user,
                        book=book,
                        defaults={
                            'title': f"Review về {short_title}",
                            'body_md': f"Review cho sách '{book.title}'. Nội dung review mẫu tự động.",
                            'rating': 5,
                            'status': 'public',
                            'is_active': True
                        }
                    )
                except Book.DoesNotExist:
                    print(f"!!! Warning: Sách có slug '{slug}' không tồn tại.")

        current_count = Review.objects.filter(user=user).count()
        needed = target_count - current_count
        
        if needed <= 0:
            print(f"--- {username} đã đủ {current_count} reviews. ---")
            return

        print(f"--- {username} vẫn thiếu {needed} bài. Đang tạo thêm ngẫu nhiên... ---")
        
        available_books = list(Book.objects.exclude(reviews__user=user))
        random.shuffle(available_books)
        
        for i in range(min(len(available_books), needed)):
            book = available_books[i]
            short_title = (book.title[:100] + '...') if len(book.title) > 100 else book.title
            
            Review.objects.create(
                user=user,
                book=book,
                title=f"Review ngẫu nhiên về {short_title}",
                body_md=f"Review tự động.",
                rating=random.choice([3, 4, 5]),
                status='public',
                is_active=True
            )
            needed -= 1

        if needed > 0:
            print(f"!!! Thiếu sách. Tạo thêm {needed} sách ảo cho {username}...")
            dummy_author, _ = Author.objects.get_or_create(name="Tác giả AI")
            for k in range(needed):
                rand_id = random.randint(10000, 99999)
                new_book = Book.objects.create(
                    title=f"Sách Ảo {k+1}-{rand_id} cho {username}", description="Sách ảo.", pages=100, year=2024
                )
                new_book.authors.add(dummy_author)
                Review.objects.create(
                    user=user, book=new_book, title=f"Review bổ sung {k+1}", body_md="Review bổ sung.",
                    rating=5, status='public', is_active=True
                )

    except User.DoesNotExist:
        print(f"User {username} không tồn tại.")

# --- THỰC HIỆN ---

reader3_slugs = [
    'truyen-kieu', 
    'sach-nhan-gian-ang-gia',
    'sach-giai-phong-bo-nao-khoi-tu-duy-oc-hai',
    'sach-hanh-trinh-cua-linh-hon',
    'hieu-sach-nho-o-paris',
    'sach-cuoc-oi-va-so-phan',
    'sach-nguyen-ngoc-tu-troi',
    'sach-luoc-su-am-nhac',
    'chainsaw-man-tap-8',
    'sach-loi-nguyen-chan-ai',
    'sach-lu-tre-uong-tau',
    'sach-ung-thu-khong-phai-la-benh',
    'sach-ai-cong-cu-nang-cao-hieu-suat-cong-viec',
    'sach-quyen-luc-ich-thuc',
    'sach-thu-cho-em',
    'sach-rung-nauy-tai-ban',
    'tim-hieu-van-hoa-thai-lan',
    'luat-to-chuc-chinh-quyen-ia-phuong-nam-2025-ban-in-2025',
    'kinh-te-quoc-te-kt'
]
create_reviews_for_user('reader3', 19, specific_book_slugs=reader3_slugs)

reviewer1_slugs = ['truyen-kieu', 'phat-giao-thai-lan']
create_reviews_for_user('reviewer1', 2, specific_book_slugs=reviewer1_slugs)

reviewer2_slugs = ['truyen-kieu', 'kingdom-63']
create_reviews_for_user('reviewer2', 2, specific_book_slugs=reviewer2_slugs)

print(">>> HOÀN TẤT <<<")
END

fi 

exec "$@"