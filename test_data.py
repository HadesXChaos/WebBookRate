import os
import django
import random
import uuid

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookreview.settings')
django.setup()

from books.models import Book, BookView
from reviews.models import Review
from django.contrib.auth import get_user_model

User = get_user_model()

def make_book_trending():
    try:
        # 1. Chọn sách mục tiêu (Random)
        count = Book.objects.count()
        if count == 0:
            print("Chưa có sách nào trong database!")
            return

        random_index = random.randint(0, count - 1)
        target_book = Book.objects.all()[random_index]
        
        print(f"🎯 MỤC TIÊU: '{target_book.title}'")
        
        # 2. Bơm 100 VIEWs (An toàn nhất, không bao giờ lỗi)
        # Lấy đại 1 user thật để gán view (hoặc để user=None cũng được)
        real_user = User.objects.first()
        
        print(f"... Đang bơm 100 views (100 điểm)")
        views = []
        for _ in range(100):
            views.append(BookView(
                book=target_book, 
                ip_address=f'192.168.1.{random.randint(1, 255)}', # Fake IP khác nhau
                user=real_user
            ))
        BookView.objects.bulk_create(views)

        # 3. Bơm 5 REVIEWs (Tạo User ảo để tránh lỗi trùng lặp)
        print(f"... Đang tạo 5 user ảo để viết 5 reviews (25 điểm)")
        
        for i in range(5):
            # Tạo tên user ngẫu nhiên để không trùng
            fake_username = f"bot_reviewer_{uuid.uuid4().hex[:8]}"
            
            # Tạo user mới
            fake_user = User.objects.create_user(
                username=fake_username, 
                password='password123',
                email=f"{fake_username}@example.com"
            )
            
            # Viết review
            Review.objects.create(
                book=target_book,
                user=fake_user,
                title=f"Sách quá hay {i+1}",
                body_md="Nội dung xuất sắc, mọi người nên đọc ngay!",
                rating=5,
                status='public'
            )
            print(f"   -> Bot '{fake_username}' đã review.")

        print("-" * 30)
        print(f"✅ XONG! Tổng điểm bơm thêm: 125 điểm.")
        print(f"Sách '{target_book.title}' chắc chắn đã lên TOP 1.")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == '__main__':
    make_book_trending()