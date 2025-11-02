# BookReview.vn

Web đánh giá sách giúp người dùng khám phá, đọc nhận xét, chấm điểm, theo dõi tiến độ đọc và tương tác cộng đồng.

## Công nghệ

- **Backend:** Django 4.2 + Django REST Framework
- **Database:** PostgreSQL
- **Cache:** Redis
- **Task Queue:** Celery
- **Storage:** S3-compatible (MinIO cho development)
- **Containerization:** Docker + Docker Compose

## Yêu cầu

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (khuyến nghị)

## Cài đặt

### 1. Clone repository

```bash
git clone <repository-url>
cd "Web Feedback Book"
```

### 2. Tạo môi trường ảo

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu hình môi trường

Sao chép file `.env.example` thành `.env` và chỉnh sửa:

```bash
cp .env.example .env
```

### 5. Chạy migrations

```bash
python manage.py migrate
```

### 6. Tạo superuser

```bash
python manage.py createsuperuser
```

### 7. Chạy development server

```bash
python manage.py runserver
```

## Sử dụng Docker

### Chạy với Docker Compose

```bash
docker-compose up -d
```

Dịch vụ sẽ chạy tại:
- **Web:** http://localhost:8000
- **MinIO Console:** http://localhost:9001
- **PostgreSQL:** localhost:5432
- **Redis:** localhost:6379

### Tạo superuser trong Docker

```bash
docker-compose exec web python manage.py createsuperuser
```

### Chạy migrations trong Docker

```bash
docker-compose exec web python manage.py migrate
```

## Cấu trúc dự án

```
.
├── bookreview/          # Django project settings
├── users/              # User authentication & profiles
├── books/              # Books, authors, genres, publishers
├── reviews/            # Reviews, comments, likes
├── shelves/            # Shelves & reading progress
├── social/             # Follow, notifications, collections
├── moderation/         # Reports & moderator actions
├── search/             # Search functionality
├── templates/          # Templates
├── static/             # Static files
├── media/              # Media files
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # Docker Compose configuration
└── README.md          # This file
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Đăng ký
- `POST /api/auth/login/` - Đăng nhập
- `POST /api/auth/logout/` - Đăng xuất
- `GET /api/auth/profile/` - Xem/chỉnh sửa profile

### Books
- `GET /api/books/` - Danh sách sách
- `GET /api/books/{slug}/` - Chi tiết sách
- `GET /api/books/authors/` - Danh sách tác giả
- `GET /api/books/genres/` - Danh sách thể loại

### Reviews
- `GET /api/reviews/` - Danh sách review
- `POST /api/reviews/` - Tạo review
- `GET /api/reviews/{id}/` - Chi tiết review
- `PATCH /api/reviews/{id}/` - Chỉnh sửa review
- `DELETE /api/reviews/{id}/` - Xóa review
- `POST /api/reviews/{id}/like/` - Like review
- `DELETE /api/reviews/{id}/like/` - Unlike review

### Shelves
- `GET /api/shelves/` - Danh sách kệ sách
- `POST /api/shelves/` - Tạo kệ sách
- `GET /api/shelves/{id}/` - Chi tiết kệ sách
- `POST /api/shelves/{id}/books/{book_id}/` - Thêm sách vào kệ

### Search
- `GET /api/search/?q=query` - Tìm kiếm
- `GET /api/search/autocomplete/?q=query` - Autocomplete

## Tính năng

- ✅ Đăng ký/đăng nhập
- ✅ Quản lý sách (tác giả, thể loại, nhà xuất bản)
- ✅ Review & Rating
- ✅ Comment & Like
- ✅ Shelves (Want to Read, Reading, Read)
- ✅ Reading Progress
- ✅ Follow Users/Authors/Books
- ✅ Notifications
- ✅ Collections
- ✅ Search
- ✅ Reports & Moderation
- ✅ SEO (sitemap, robots.txt)

## Development

### Chạy tests

```bash
python manage.py test
```

### Tạo migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Chạy Celery worker

```bash
celery -A bookreview worker -l info
```

### Chạy Celery beat

```bash
celery -A bookreview beat -l info
```

## Production Deployment

1. Cập nhật `DEBUG=False` trong `.env`
2. Cấu hình `ALLOWED_HOSTS`
3. Cấu hình database production
4. Cấu hình S3 storage
5. Cấu hình email
6. Setup SSL/TLS
7. Setup CDN cho static files

## License

MIT License

## Contributors

- Development Team
