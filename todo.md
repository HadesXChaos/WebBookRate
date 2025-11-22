# TODO - Tiến độ thực hiện BookReview.vn

## Tổng quan
Dự án BookReview.vn - Web đánh giá sách giúp người dùng khám phá, đọc nhận xét, chấm điểm, theo dõi tiến độ đọc và tương tác cộng đồng.

**Ngày cập nhật:** $(date)

---

## 1. Cấu trúc dự án - ✅ Đã hoàn thành

### 1.1 Module Structure
- ✅ **bookreview/** - Django project settings
- ✅ **users/** - User authentication & profiles
- ✅ **books/** - Books, authors, genres, publishers
- ✅ **reviews/** - Reviews, comments, likes
- ✅ **shelves/** - Shelves & reading progress
- ✅ **social/** - Follow, notifications, collections
- ✅ **moderation/** - Reports & moderator actions
- ✅ **search/** - Search functionality

### 1.2 Templates & Static Files
- ✅ Templates structure (`templates/`)
- ✅ Static files (`static/`)
- ✅ Base template (`base.html`)
- ✅ Auth templates (login, register, logout)
- ✅ Book detail template
- ✅ Review detail template
- ✅ User profile template
- ✅ Search template
- ✅ Shelves template
- ✅ Notifications template

### 1.3 Infrastructure
- ✅ Docker setup (`Dockerfile`, `docker-compose.yml`)
- ✅ Requirements (`requirements.txt`)
- ✅ Environment example (`.env.example`)
- ✅ Django migrations structure
- ✅ Settings configuration

---

## 2. Authentication & User Management - ✅ Đã hoàn thành cơ bản

### 2.1 Models
- ✅ User model (Django auth)
- ✅ User Profile model
- ✅ User migrations

### 2.2 API Endpoints
- ✅ `POST /api/auth/register/` - Đăng ký
- ✅ `POST /api/auth/login/` - Đăng nhập
- ✅ `POST /api/auth/logout/` - Đăng xuất (API)
- ✅ `GET /api/auth/profile/` - Xem/chỉnh sửa profile

### 2.3 Frontend Views
- ✅ `GET /login/` - Trang đăng nhập
- ✅ `GET /register/` - Trang đăng ký
- ✅ `GET /logout/` - Trang đăng xuất (frontend view)

### 2.4 User Stories
- ✅ **US-REG-01**: Đăng ký/đăng nhập (email) - ✅ Đã hoàn thành cơ bản
  - ⚠️ OAuth (Google/Facebook/Apple) - 🔄 Chưa triển khai
  - ✅ Email verification - ✅ Đã triển khai
  - ✅ Password reset - ✅ Đã triển khai
  - ✅ Rate-limit - ✅ Đã triển khai

### 2.5 Bug Fixes
- ✅ **Fix 2025-01-XX**: Fix lỗi 405 Method Not Allowed cho `/api/auth/logout/`
  - Đã tạo `logout_view_frontend` để xử lý GET request từ frontend
  - Tự động submit POST form khi truy cập `/logout/`

---

## 3. Books & Metadata Management - ✅ Đã hoàn thành cơ bản

### 3.1 Models
- ✅ Book model
- ✅ Author model
- ✅ Genre model
- ✅ Publisher model
- ✅ Tag model
- ✅ BookEdition model
- ✅ BookAuthor relationship
- ✅ BookTag relationship

### 3.2 API Endpoints
- ✅ `GET /api/books/` - Danh sách sách
- ✅ `GET /api/books/{slug}/` - Chi tiết sách
- ✅ `GET /api/books/authors/` - Danh sách tác giả
- ✅ `GET /api/books/genres/` - Danh sách thể loại
- ✅ `GET /api/books/publishers/` - Danh sách nhà xuất bản
- ✅ `GET /api/books/tags/` - Danh sách thẻ

### 3.3 Frontend Views
- ✅ `GET /books/{slug}/` - Trang chi tiết sách

### 3.4 Features
- ✅ Slug duy nhất cho books, authors, genres
- ✅ Tính toán điểm trung bình và số lượng review (signals)

### 3.5 Bug Fixes
- ✅ **Fix 2025-01-XX**: Fix lỗi 404 cho `/api/books/genres/`
  - Sắp xếp lại URL patterns trong `books/urls.py`
  - Đặt các pattern cụ thể (`genres/`, `authors/`, `publishers/`, `tags/`) trước pattern catch-all `<str:slug>/`

### 3.6 User Stories
- ✅ **US-BOOK-01**: Tìm sách theo tên, tác giả, ISBN - ✅ Đã triển khai
  - ⚠️ Cache optimization - 🔄 Chưa triển khai
  - ⚠️ Autocomplete - 🔄 Chưa triển khai đầy đủ

---

## 4. Reviews & Ratings - ✅ Đã hoàn thành cơ bản

### 4.1 Models
- ✅ Review model (với markdown support)
- ✅ Rating model
- ✅ ReviewImage model
- ✅ Comment model (thread support)
- ✅ Like model (generic foreign key)

### 4.2 API Endpoints
- ✅ `GET /api/reviews/` - Danh sách review
- ✅ `POST /api/reviews/` - Tạo review
- ✅ `GET /api/reviews/{id}/` - Chi tiết review
- ✅ `PATCH /api/reviews/{id}/` - Chỉnh sửa review
- ✅ `DELETE /api/reviews/{id}/` - Xóa review
- ✅ `POST /api/reviews/{id}/like/` - Like review
- ✅ `DELETE /api/reviews/{id}/like/` - Unlike review

### 4.3 Frontend Views
- ✅ `GET /reviews/{id}/` - Trang chi tiết review

### 4.4 Features
- ✅ Markdown support cho review body
- ✅ HTML sanitization (bleach)
- ✅ Rating 1-5
- ✅ Like/unlike functionality
- ✅ Comment threading

### 4.5 User Stories
- ✅ **US-REV-01**: Viết review với rating 1-5 - ✅ Đã hoàn thành cơ bản
  - ✅ Validation tối thiểu 100 ký tự - ✅ Đã triển khai (REVIEW_MIN_LENGTH setting)
  - ⚠️ Anti-spam - 🔄 Chưa triển khai
- ✅ **US-REV-02**: Chỉnh sửa/xoá review - ✅ Đã triển khai
  - ⚠️ Lưu lịch sử sửa - 🔄 Chưa triển khai
- ✅ **US-CMT-01**: Bình luận dưới review - ✅ Đã triển khai
  - ⚠️ Mention @username - 🔄 Chưa triển khai
  - ✅ Rate-limit - ✅ Đã triển khai (20 comments/hour)
- ✅ **US-LIKE-01**: Like review/bình luận - ✅ Đã triển khai

---

## 5. Shelves & Reading Progress - ✅ Đã hoàn thành cơ bản

### 5.1 Models
- ✅ Shelf model (hệ thống + tùy chỉnh)
- ✅ ShelfItem model
- ✅ ReadingProgress model

### 5.2 API Endpoints
- ✅ `GET /api/shelves/` - Danh sách kệ sách
- ✅ `POST /api/shelves/` - Tạo kệ sách
- ✅ `GET /api/shelves/{id}/` - Chi tiết kệ sách
- ✅ `POST /api/shelves/{id}/books/{book_id}/` - Thêm sách vào kệ

### 5.3 Frontend Views
- ✅ `GET /shelves/` - Trang quản lý kệ sách

### 5.4 User Stories
- ✅ **US-SHL-01**: Thêm sách vào kệ Want-to-Read/Reading/Read - ✅ Đã triển khai
- ⚠️ **US-PROG-01**: Cập nhật tiến độ đọc - 🔄 Chưa triển khai đầy đủ
  - ⚠️ Biểu đồ tuần - 🔄 Chưa triển khai

---

## 6. Social Features - ✅ Đã hoàn thành cơ bản

### 6.1 Models
- ✅ Follow model (generic foreign key)
- ✅ Notification model
- ✅ Collection model (tùy chọn)

### 6.2 API Endpoints
- ✅ `GET /api/social/notifications/` - Danh sách thông báo
- ✅ `PATCH /api/social/notifications/{id}/` - Đánh dấu đã đọc

### 6.3 Frontend Views
- ✅ `GET /notifications/` - Trang thông báo

### 6.4 User Stories
- ⚠️ **US-FLW-01**: Follow user/author/book - 🔄 Chưa triển khai đầy đủ
- ⚠️ **US-COLL-01**: Tạo collection - 🔄 Chưa triển khai

---

## 7. Search & Discovery - ✅ Đã hoàn thành cơ bản

### 7.1 API Endpoints
- ✅ `GET /api/search/?q=query` - Tìm kiếm
- ✅ `GET /api/search/autocomplete/?q=query` - Autocomplete

### 7.2 Frontend Views
- ✅ `GET /search/` - Trang tìm kiếm
- ✅ `GET /explore/` - Trang khám phá

### 7.3 Features
- ✅ Full-text search cơ bản
- ✅ Advanced filtering - ✅ Đã triển khai (genre, rating, year, author, publisher, language, sorting)
- ⚠️ Trending algorithm - 🔄 Chưa triển khai

---

## 8. Moderation - ✅ Đã hoàn thành cơ bản

### 8.1 Models
- ✅ Report model
- ✅ ModeratorAction model

### 8.2 API Endpoints
- ✅ `POST /api/moderation/reports/` - Báo cáo vi phạm
- ✅ `GET /api/moderation/reports/` - Danh sách báo cáo (moderator)

### 8.3 User Stories
- ⚠️ **US-RPT-01**: Báo cáo nội dung vi phạm - 🔄 Chưa triển khai đầy đủ
  - ⚠️ Moderator dashboard - 🔄 Chưa triển khai
  - ⚠️ SLA xử lý 48h - 🔄 Chưa triển khai

---

## 9. SEO & Analytics - ✅ Đã hoàn thành cơ bản

### 9.1 Features
- ✅ Sitemap (books, authors, reviews) - `sitemaps.py`
- ✅ Robots.txt
- ✅ Slug URLs cho SEO-friendly
- ✅ Schema.org markup - ✅ Đã triển khai (Book, Review với AggregateRating)
- ✅ OpenGraph tags - ✅ Đã triển khai (title, description, image, url)
- ✅ Canonical URLs - ✅ Đã triển khai cho tất cả các trang

### 9.2 User Stories
- ✅ **US-SEO-01**: Google index trang chi tiết sách - ✅ Đã hoàn thành
  - ✅ Sitemap.xml, robots.txt
  - ✅ Schema.org Book/Review - ✅ Đã triển khai

---

## 10. Admin & Management - ✅ Đã hoàn thành cơ bản

### 10.1 Features
- ✅ Django Admin interface
- ✅ Admin cho các models chính
- ⚠️ Custom admin dashboard - 🔄 Chưa triển khai
- ⚠️ Banner management - 🔄 Chưa triển khai
- ⚠️ Banned words configuration - 🔄 Chưa triển khai

---

## 11. Performance & Cache - ✅ Đã triển khai cơ bản

### 11.1 Requirements
- ✅ Cache layer (Redis) - ✅ Đã cấu hình
- ✅ Cache trang sách (60s) - ✅ Đã triển khai
- ✅ Cache danh mục (5 phút) - ✅ Đã triển khai
- ⚠️ Precompute top books (Celery job) - 🔄 Chưa triển khai
- ✅ Optimize queries (select_related/prefetch_related) - ✅ Đã triển khai

---

## 12. Security & Privacy - ✅ Đã triển khai cơ bản

### 12.1 Features
- ✅ CSRF protection (Django default)
- ✅ HTML sanitization (bleach cho markdown)
- ✅ Rate limiting - ✅ Đã triển khai (register, login, password reset, email verification, comments)
- ✅ Password strength validation - ✅ Đã triển khai (uppercase, lowercase, digit, special char, min 8 chars)
- ⚠️ 2FA - 🔄 Chưa triển khai
- ⚠️ reCAPTCHA/Turnstile - 🔄 Chưa triển khai
- ⚠️ GDPR data export - 🔄 Chưa triển khai

---

## 13. Testing - ✅ Đã triển khai cơ bản

### 13.1 Requirements
- ✅ Unit tests - ✅ Đã triển khai (models: User, Book, Review, Comment, Author, Genre)
- ✅ Integration tests - ✅ Đã triển khai (API endpoints: auth, books, reviews)
- ✅ Test validators - ✅ Đã triển khai (password strength validation)
- ⚠️ Test coverage 90% - 🔄 Chưa đạt (cần bổ sung thêm tests)

---

## 14. Documentation - ✅ Đã hoàn thành cơ bản

### 14.1 Files
- ✅ README.md - Hướng dẫn cài đặt và sử dụng
- ✅ requirement.md - Tài liệu yêu cầu phần mềm (SRS)
- ✅ todo.md - File này

---

## 15. Deployment & DevOps - ✅ Đã hoàn thành cơ bản

### 15.1 Infrastructure
- ✅ Docker configuration
- ✅ Docker Compose setup
- ✅ Environment variables setup
- ✅ Production deployment guide - ✅ Đã hoàn thiện (DEPLOYMENT.md)
- ⚠️ CI/CD pipeline - 🔄 Chưa triển khai
- ⚠️ Monitoring (Sentry, Prometheus) - 🔄 Chưa triển khai

---

## 16. Bug Fixes Log

### 2025-01-XX
1. ✅ **Fix URL ordering trong books/urls.py**
   - **Vấn đề:** `/api/books/genres/` trả về 404
   - **Nguyên nhân:** Pattern catch-all `<str:slug>/` được đặt trước các pattern cụ thể
   - **Giải pháp:** Sắp xếp lại URL patterns, đặt các pattern cụ thể trước pattern catch-all
   - **File thay đổi:** `books/urls.py`

2. ✅ **Fix logout view cho frontend**
   - **Vấn đề:** `/api/auth/logout/` trả về 405 Method Not Allowed khi truy cập từ frontend
   - **Nguyên nhân:** API endpoint chỉ chấp nhận POST, nhưng frontend redirect sử dụng GET
   - **Giải pháp:** Tạo `logout_view_frontend` xử lý cả GET và POST, tự động submit POST form
   - **Files thay đổi:** 
     - `bookreview/views.py` - Thêm `logout_view_frontend`
     - `bookreview/urls.py` - Cập nhật logout URL
     - `templates/auth/logout.html` - Template mới

### 2025-01-XX (Triển khai MVP Features)
3. ✅ **Triển khai Email Verification**
   - **Tính năng:** Gửi email xác nhận khi đăng ký, xác nhận email qua link
   - **Files thay đổi:**
     - `users/utils.py` - Thêm `send_verification_email()`
     - `users/views.py` - Cập nhật `RegisterView` và `verify_email()`
     - `templates/emails/verification_email.html` - Email template
     - `templates/auth/email_verified.html` - Frontend verification page
     - `bookreview/settings.py` - Thêm `BASE_URL` setting

4. ✅ **Triển khai Password Reset**
   - **Tính năng:** Yêu cầu đặt lại mật khẩu qua email, đặt lại mật khẩu với token
   - **Files thay đổi:**
     - `users/models.py` - Thêm `PasswordResetToken` model
     - `users/serializers.py` - Thêm `PasswordResetRequestSerializer`, `PasswordResetConfirmSerializer`
     - `users/views.py` - Thêm `password_reset_request()`, `password_reset_confirm()`
     - `users/utils.py` - Thêm `send_password_reset_email()`
     - `templates/emails/password_reset_email.html` - Email template
     - `templates/auth/password_reset.html` - Frontend request page
     - `templates/auth/password_reset_confirm.html` - Frontend confirm page
     - `bookreview/views.py` - Thêm `password_reset_view()`

5. ✅ **Triển khai Rate Limiting**
   - **Tính năng:** Giới hạn số lượng request cho các endpoints quan trọng
   - **Files thay đổi:**
     - `users/throttles.py` - Custom throttle classes (Register, Login, PasswordReset, EmailVerification)
     - `users/views.py` - Áp dụng throttles cho các views
     - `bookreview/settings.py` - Cấu hình throttle rates

6. ✅ **Cải thiện Cache Optimization**
   - **Tính năng:** Cache cho books, reviews, và danh mục
   - **Files thay đổi:**
     - `books/views.py` - Thêm cache cho `BookDetailView` (60s), danh sách genres/authors/publishers/tags (5 phút)
     - `reviews/views.py` - Thêm cache cho `ReviewDetailView` (60s), invalidate cache khi update

### 2025-01-XX (Hoàn thiện MVP Features)
7. ✅ **Triển khai Password Strength Validation**
   - **Tính năng:** Validation mật khẩu nâng cao (uppercase, lowercase, digit, special char, min 8 chars)
   - **Files thay đổi:**
     - `users/validators.py` - Thêm `validate_password_strength()` function
     - `users/serializers.py` - Áp dụng validator cho RegisterSerializer và PasswordResetConfirmSerializer

8. ✅ **Thêm Rate Limiting cho Comments**
   - **Tính năng:** Giới hạn số lượng comment (20 comments/hour per user)
   - **Files thay đổi:**
     - `users/throttles.py` - Thêm `CommentThrottle` class
     - `reviews/views.py` - Áp dụng throttle cho `CommentListView`
     - `bookreview/settings.py` - Thêm `comment` throttle rate

9. ✅ **Triển khai Advanced Search & Filtering**
   - **Tính năng:** Tìm kiếm nâng cao với filters (genre, rating, year, author, publisher, language, sorting)
   - **Files thay đổi:**
     - `search/views.py` - Cải thiện `search_view()` với advanced filtering và sorting

10. ✅ **Thêm Schema.org Markup**
    - **Tính năng:** Structured data cho Book và Review để cải thiện SEO
    - **Files thay đổi:**
      - `templates/books/book_detail.html` - Thêm Book schema với AggregateRating
      - `templates/reviews/review_detail.html` - Thêm Review schema với Rating

11. ✅ **Thêm Canonical URLs và OpenGraph Tags**
    - **Tính năng:** Canonical URLs và OpenGraph tags đầy đủ cho SEO và social sharing
    - **Files thay đổi:**
      - `templates/base.html` - Thêm canonical URL và og:url
      - `templates/books/book_detail.html` - Thêm canonical và og tags
      - `templates/reviews/review_detail.html` - Thêm canonical và og tags

### 2025-01-XX (Testing & Deployment)
12. ✅ **Triển khai Testing Infrastructure**
    - **Tính năng:** Unit tests và integration tests cho các modules chính
    - **Files thay đổi:**
      - `users/tests.py` - Tests cho User model, API endpoints, validators, email verification, password reset
      - `books/tests.py` - Tests cho Book, Author, Genre models và API endpoints
      - `reviews/tests.py` - Tests cho Review, Comment, Like models và API endpoints

13. ✅ **Tạo Production Deployment Guide**
    - **Tính năng:** Hướng dẫn chi tiết triển khai lên production
    - **Files thay đổi:**
      - `DEPLOYMENT.md` - Hướng dẫn đầy đủ về deployment, cấu hình Nginx, Gunicorn, Celery, SSL, backup, monitoring

---

## Tổng kết

### Đã hoàn thành (✅)
- Cấu trúc dự án và module structure
- Authentication & User Management cơ bản
- Books & Metadata Management
- Reviews & Ratings cơ bản
- Shelves & Reading Progress cơ bản
- Social Features cơ bản
- Search & Discovery cơ bản
- Moderation models
- SEO cơ bản (sitemap, robots.txt)
- Admin interface cơ bản
- Docker setup
- Documentation cơ bản

### Đang triển khai / Cần bổ sung (🔄)
- OAuth (Google/Facebook/Apple)
- Trending algorithm
- Precompute top books (Celery job)
- Security enhancements (2FA, reCAPTCHA)
- Test coverage 90% (cần bổ sung thêm tests)
- CI/CD pipeline
- Monitoring & logging (Sentry, Prometheus)
- i18n (đa ngôn ngữ)
- Advanced features (collections, reading progress charts)
- GDPR data export
- Anti-spam cho reviews
- Mention @username trong comments
- Lưu lịch sử sửa review

### Chưa bắt đầu (❌)
- Import CSV/ISBN functionality
- OpenLibrary API integration
- Advanced analytics
- CDN setup
- Advanced moderation dashboard

---

## Lộ trình tiếp theo (Ưu tiên)

### MVP (Minimum Viable Product) - Ưu tiên cao
1. ✅ Core features (đã hoàn thành)
2. ✅ Email verification
3. ✅ Rate limiting
4. ✅ Cache optimization
5. ✅ Testing cơ bản (unit tests, integration tests)
6. ✅ Production deployment guide

### V1 - Tính năng nâng cao
1. OAuth integration
2. Advanced search & filtering
3. Trending algorithm
4. Collections feature
5. Reading progress charts
6. Advanced moderation dashboard
7. i18n support

---

**Ghi chú:** File này sẽ được cập nhật thường xuyên khi có tiến độ mới.

