# Tài liệu Yêu cầu Phần mềm (SRS)

## 1. Tổng quan
- **Tên sản phẩm:** BookReview.vn (tạm đặt)
- **Mục tiêu:** Xây dựng web đánh giá sách giúp người dùng khám phá, đọc nhận xét, chấm điểm, theo dõi tiến độ đọc và tương tác cộng đồng.
- **Phạm vi:** Ứng dụng web (desktop + mobile web) dùng **Django** (Python) làm backend, Django templating hoặc SPA nhẹ cho frontend; triển khai Postgres; Redis cho cache/queue; Celery cho tác vụ nền; S3-compatible cho lưu trữ.
- **Stakeholders:** Chủ sản phẩm, Dev, QA, Content Moderator, Người dùng cuối, Đối tác NXB.

## 2. Vai trò & Quyền hạn
- **Anonymous**: duyệt sách, xem đánh giá công khai, tìm kiếm, đăng ký.
- **User**: tất cả của Anonymous + tạo/sửa/xoá review của chính mình, chấm điểm, bình luận, theo dõi người dùng/sách, tạo kệ sách (shelf), danh sách (collection), cập nhật tiến độ đọc, báo cáo vi phạm.
- **Moderator**: duyệt/ẩn review, xoá bình luận vi phạm, xử lý báo cáo, cảnh cáo khoá tài khoản.
- **Admin**: CRUD toàn hệ thống (qua Django Admin), cấu hình banner, SEO, đề xuất nổi bật, quản trị thẻ/genre.

## 3. Phân rã chức năng (high-level)
1) **Quản lý Sách & Metadata**: Tác giả, thể loại, NXB, ấn bản, thẻ, ISBN.
2) **Đánh giá & Xếp hạng**: Review (markdown), rating 1–5, like, bình luận, đính kèm hình ảnh trích dẫn.
3) **Tìm kiếm & Khám phá**: full-text, lọc theo thể loại, năm, điểm trung bình, xu hướng.
4) **Kệ sách cá nhân (Shelves)**: Want-to-Read, Reading, Read; kệ tuỳ chỉnh.
5) **Tiến độ đọc**: cập nhật %/trang, mốc thời gian, biểu đồ cá nhân.
6) **Theo dõi & Thông báo**: follow user/author/book, thông báo khi có review/bài mới.
7) **Danh sách/Collection**: Top 10 thể loại X, Sách 2025 nên đọc, v.v.
8) **Quản trị & Kiểm duyệt**: báo cáo nội dung, log moderator, dashboard.
9) **Tích hợp**: đăng nhập Google/Facebook/Apple; import sách qua CSV/ISBN; OpenLibrary API (tuỳ chọn).
10) **SEO & Social**: OpenGraph, sitemap, canonical, slug.

## 4. User Stories (tiêu chí chấp nhận kèm ID)
- **US-REG-01**: Là người dùng, tôi có thể đăng ký/đăng nhập (email + OAuth) để tạo review. *AC:* OTP/Email verify; password reset hoạt động; rate-limit 5 req/phút.
- **US-BOOK-01**: Tôi có thể tìm sách theo tên, tác giả, ISBN. *AC:* tìm trong < 500ms cache hit; hỗ trợ gợi ý autocomplete.
- **US-REV-01**: Tôi có thể viết review (markdown) với rating 1–5. *AC:* bắt buộc tối thiểu 100 ký tự; 1 rating/user/sách; anti-spam.
- **US-REV-02**: Tôi có thể chỉnh sửa/xoá review của mình. *AC:* lưu lịch sử sửa.
- **US-CMT-01**: Tôi có thể bình luận dưới review. *AC:* hỗ trợ mention @username; rate-limit.
- **US-LIKE-01**: Tôi có thể like review/bình luận. *AC:* toggle like idempotent.
- **US-SHL-01**: Tôi có thể thêm sách vào kệ Want-to-Read/Reading/Read. *AC:* không trùng bản ghi; cập nhật trạng thái.
- **US-PROG-01**: Tôi cập nhật tiến độ đọc theo trang hoặc %. *AC:* vẽ biểu đồ tuần; không vượt tổng trang.
- **US-FLW-01**: Tôi follow tác giả/người dùng/sách để nhận thông báo. *AC:* có thể tắt từng loại noti.
- **US-COLL-01**: Tôi tạo collection công khai/riêng tư. *AC:* kéo-thả sắp xếp; mô tả; ảnh đại diện.
- **US-RPT-01**: Tôi báo cáo nội dung vi phạm. *AC:* Moderator nhận queue; SLA xử lý 48h.
- **US-SEO-01**: Google index trang chi tiết sách. *AC:* sitemap.xml, robots.txt, schema.org Book/Review.

## 5. Yêu cầu chức năng chi tiết
### 5.1 Auth & Profile
- Đăng ký email (verify link), đăng nhập, quên mật khẩu.
- OAuth: Google/Facebook/Apple (django-allauth hoặc social-auth).
- Hồ sơ: avatar, bio, liên kết mạng xã hội, khu vực, ngôn ngữ, cài đặt thông báo.

### 5.2 Sách & Ấn bản
- Sách: tiêu đề, mô tả, năm xuất bản, trang, bìa, ISBN13, thể loại, tag.
- Ấn bản: ràng buộc với Sách + NXB + định dạng (paperback/hardcover/ebook/audiobook), ngôn ngữ.
- Tác giả/NXB/Thể loại: CRUD, slug duy nhất.
- Tự động tính **điểm trung bình** và **đếm review** theo sách.

### 5.3 Review/Rating/Comment
- Review: markdown + sanitized HTML, đính kèm tối đa 5 ảnh, trạng thái (public/draft/hidden), lịch sử chỉnh sửa.
- Rating: 1–5 (0.5 step tuỳ chọn), mỗi user 1 rating/sách; cho phép update.
- Comment: thread 2 cấp (comment + reply), mention, hashtag.
- Like: cho review & comment; soft-delete.

### 5.4 Tìm kiếm & Khám phá
- Tìm kiếm text theo Sách/Tác giả/Review (Postgres trigram/Full Text hoặc Elasticsearch tuỳ chọn).
- Bộ lọc: thể loại, năm, ngôn ngữ, điểm trung bình, số review, sắp xếp theo trending/mới/điểm cao.
- Trang "Khám phá": thịnh hành tuần, mới đăng, đề xuất theo hành vi.

### 5.5 Kệ sách & Tiến độ
- Mặc định 3 kệ hệ thống; cho phép kệ tuỳ chỉnh (public/private).
- Tiến độ: lưu snapshot (date, page/percent); hiển thị biểu đồ.

### 5.6 Thông báo
- Loại: có người theo dõi bạn, review mới từ người theo dõi, bình luận/mention, like, nội dung bị phản hồi.
- Kênh: onsite + email; tắt theo loại.

### 5.7 Báo cáo & Kiểm duyệt
- Người dùng gửi report với lý do + ghi chú.
- Moderator dashboard: hàng đợi, bộ lọc, hành động (ẩn, xoá, cảnh cáo), nhật ký.

### 5.8 Quản trị
- Django Admin: model quản trị đầy đủ + list_filter/search.
- Trang cấu hình: banner, từ cấm, trọng số đề xuất, meta SEO mặc định.

## 6. Yêu cầu phi chức năng
- **Hiệu năng:** P95 < 800ms cho trang động; P95 < 200ms cache hit. Tải 200 RPS (đọc) và 20 RPS (ghi) ở giai đoạn đầu.
- **Bảo mật:** CSRF, XSS, SSRF, SQLi; mật khẩu Argon2/BCrypt; 2FA tuỳ chọn; reCAPTCHA/Turnstile; rate-limit bằng Redis.
- **Khả dụng:** 99.5% giai đoạn MVP; backup DB hằng ngày, giữ 7/30/365.
- **Khả mở rộng:** tách dịch vụ tìm kiếm; dùng CDN cho media; cache layer (Redis) cho danh mục, top list.
- **Khả dụng trên mobile:** responsive; Lighthouse Performance ≥ 80, Accessibility ≥ 95.
- **Tuân thủ:** GDPR-like (export/delete data), cookie consent, ToS/Privacy.

## 7. Mô hình dữ liệu (đề xuất)
- **User** (Django auth), **Profile**(1-1 User)
- **Author(id, name, slug, bio)**
- **Genre(id, name, slug, parent_id)**
- **Publisher(id, name, slug)**
- **Book(id, title, slug, description, year, pages, language, cover, avg_rating, rating_count, publisher_id)**
- **BookEdition(id, book_id, isbn13, format, published_at, language)**
- **BookAuthor(book_id, author_id)** (N-N)
- **Tag(id, name, slug)**, **BookTag(book_id, tag_id)**
- **Review(id, book_id, user_id, title, body_md, body_html, rating, status, created_at, updated_at, edited_at)**
- **ReviewImage(id, review_id, url)**
- **Comment(id, review_id, user_id, parent_id, body, status)**
- **Like(id, user_id, content_type, object_id, created_at)**
- **Shelf(id, user_id, name, system_type: {WTR, READING, READ}|null, visibility)**
- **ShelfItem(id, shelf_id, book_id, added_at)**
- **ReadingProgress(id, user_id, book_id, page, percent, created_at)**
- **Follow(id, follower_id, target_type{user,author,book}, target_id)**
- **Notification(id, user_id, type, payload(json), is_read, created_at)**
- **Report(id, reporter_id, target_type, target_id, reason, note, status)**
- **ModeratorAction(id, moderator_id, action, target_type, target_id, note, created_at)**

> Gợi ý: dùng GenericForeignKey cho Like/Report/ModeratorAction; dùng soft delete (is_active) cho nội dung.

## 8. API/URL (REST trước, GraphQL tuỳ chọn)
- `GET /books/?q=&genre=&year=&ordering=` – danh sách sách + filter.
- `GET /books/{slug}/` – chi tiết sách + điểm trung bình + top reviews.
- `POST /books/` – (admin) tạo sách.
- `GET /authors/{slug}/` – chi tiết tác giả + sách liên quan.
- `GET /reviews/?book=&user=&ordering=` – danh sách review.
- `POST /reviews/` – tạo review (body_md, rating, images[]).
- `PATCH /reviews/{id}/`, `DELETE /reviews/{id}/` – sửa/xoá của chủ sở hữu.
- `POST /reviews/{id}/like`, `DELETE /reviews/{id}/like` – like/unlike.
- `GET /reviews/{id}/comments`, `POST /reviews/{id}/comments`.
- `POST /reports/` – báo cáo vi phạm.
- `GET /me/shelves`, `POST /me/shelves` – kệ cá nhân; `POST /me/shelves/{id}/items`.
- `POST /progress/` – cập nhật tiến độ đọc.
- `GET /feed/` – bản tin theo follow.
- `GET /notifications/`, `PATCH /notifications/{id}` – đánh dấu đã đọc.
- Auth: `POST /auth/register`, `/auth/login`, `/auth/logout`, `/auth/oauth/`.

## 9. Giao diện (wireframe mô tả)
- **Trang chủ:** hero + ô tìm kiếm; khối "Thịnh hành", "Review mới", "Đề xuất theo bạn".
- **Trang sách:** bìa, metadata, nút Thêm vào kệ; biểu đồ phân bố điểm; review nổi bật, tab Ấn bản.
- **Trang review:** tiêu đề, nội dung markdown render, ảnh đính kèm, like, chia sẻ, bình luận thread.
- **Trang người dùng:** avatar, bio, kệ sách công khai, collection, hoạt động gần đây.
- **Trang khám phá:** filter trái, danh sách thẻ/genre, sort.
- **Trang moderator:** hàng đợi report, bộ lọc, bảng chi tiết, quick actions.

## 10. Luồng nghiệp vụ chính
1) **Tạo review:** Auth → truy cập sách → viết review + rating → preview → publish → cập nhật avg_rating (signal) → thông báo cho follower.
2) **Bình luận/Like:** Post comment → gửi noti cho chủ review; Like toggle idempotent.
3) **Theo dõi:** Follow → feed cập nhật → có thể unfollow.
4) **Báo cáo & duyệt:** User gửi report → Moderator xử lý → ghi log hành động.

## 11. Quy tắc & Ràng buộc
- Mỗi user chỉ một rating/sách; sửa rating cập nhật lại avg.
- Review tối thiểu 100 ký tự; cấm từ nhạy cảm (configurable); ảnh ≤ 2MB/tấm.
- Slug duy nhất; ISBN13 chuẩn hoá; pages > 0.

## 12. Hiệu năng & Cache
- Cache trang sách (key: book:{id}) 60s; cache danh mục 5 phút.
- Precompute top books tuần (Celery job mỗi 6h).
- Dùng select_related/prefetch_related tránh N+1.

## 13. Bảo mật & Quyền riêng tư
- CSRF, XSS sanitize (bleach) cho markdown.
- Tách quyền Moderator qua group/permission Django.
- Nhật ký audit cho hành động moderator và admin.
- Ẩn email user; cho phép export dữ liệu cá nhân (GDPR-like).

## 14. Kiểm thử (test cases mẫu)
- **TC-REV-01:** Tạo review hợp lệ → 201; body_html được sanitize; avg_rating tăng chính xác.
- **TC-REV-02:** Review <100 ký tự → 400.
- **TC-RATE-01:** 2 lần rating cùng user/sách → update thay vì tạo mới.
- **TC-SEARCH-01:** tìm theo tiêu đề có dấu/không dấu khớp.
- **TC-AUTH-01:** reset password gửi email thành công.
- **TC-NOTI-01:** like review gửi noti 1 lần.
- **TC-REPORT-01:** report tạo ticket; moderator thấy trong queue.

## 15. Triển khai & Môi trường
- **Dev:** Django, Poetry/venv, Postgres, Redis, MinIO (S3), Docker Compose.
- **Prod:** Docker + Gunicorn + Nginx, Auto TLS, CDN cho media; Postgres managed; Redis managed; Celery worker + beat.
- **Env vars:** SECRET_KEY, DB_URL, REDIS_URL, EMAIL_BACKEND, S3 creds, SOCIAL_KEYS.

## 16. Logging & Giám sát
- Django logging JSON; request ID (correlation-id);
- Sentry error tracking; Prometheus metrics (RQPS, latency, Celery job duration); Health check `/healthz`.

## 17. SEO/Analytics
- Tạo sitemap động (books, authors, reviews); robots.txt; Schema.org (Book, Review, Person).
- OpenGraph/Twitter Card; URL canonical; phân trang có rel=next/prev.
- Google Analytics/GTM (opt-in).

## 18. i18n & Accessibility
- Đa ngôn ngữ (vi, en); gettext.
- ARIA roles; contrast ≥ WCAG AA; keyboard navigation.

## 19. Nhập liệu & Tích hợp
- Import CSV: sách cơ bản (title, author, isbn, year, pages).
- OpenLibrary/Google Books API: tra cứu metadata theo ISBN (tối ưu hoá qua Celery job).

## 20. Lộ trình (MVP → V1)
- **MVP (6–8 tuần):** Auth, Sách/Author/Genre, Review/Rating, Comment/Like, Shelves hệ thống, Tìm kiếm cơ bản, SEO cơ bản, Admin, Báo cáo vi phạm tối thiểu.
- **V1:** Shelves tuỳ chỉnh, Tiến độ đọc, Collections, Noti email, Moderator dashboard đầy đủ, Đề xuất cá nhân hoá, i18n.

## 21. Rủi ro & Giảm thiểu
- Spam/abuse → rate limit + moderation queue + từ cấm.
- Hiệu năng tìm kiếm → chuyển ES khi data > 200k bản ghi.
- Bản quyền ảnh bìa → sử dụng API/nguồn có license; hoặc yêu cầu người dùng xác nhận quyền sử dụng.

## 22. Phụ lục: Migrations sơ bộ (Django)
1. users/profile
2. authors/genres/publishers/tags
3. books/book_editions/book_authors/book_tags
4. reviews/ratings/review_images
5. comments/likes
6. shelves/shelf_items
7. reading_progress
8. follow/notifications
9. reports/moderator_actions

## 23. Định nghĩa chất lượng hoàn thành (DoD)
- 90% test coverage domain chính; lint/format CI pass; security checks pass.
- Docs: README, ENV example, hướng dẫn deploy.
- Zero P0 bug mở khi release.

