# 1. Tổng quan dự án
**Tên dự án:** BookRate (có thể đổi)

**Mô tả ngắn:** Xây dựng website cộng đồng cho phép người dùng khám phá, đánh giá, nhận xét, xếp hạng và thảo luận về sách. Hệ thống cung cấp trang quản trị để quản lý sách, tác giả, nhà xuất bản, người dùng, nội dung do người dùng tạo (UGC) và báo cáo.

**Phạm vi:** Web app responsive (Desktop/Mobile), có API nội bộ cho SPA/mobile sau này.

**Công nghệ đề xuất:**
- **PHP framework:** Laravel 11 (có thể thay bằng Symfony 7 nếu cần).
- **CSDL:** MySQL 8.0 / MariaDB 10.6+.
- **Cache/Search:** Redis, Meilisearch/Elasticsearch cho tìm kiếm full‑text.
- **Frontend:** Blade + TailwindCSS + Alpine.js (hoặc Vue 3 Inertia.js nếu muốn SPA nhẹ).
- **Triển khai:** Docker Compose (Nginx + PHP-FPM + MySQL + Redis). CI/CD (GitHub Actions).

**Đối tượng sử dụng:** Khách vãng lai, Người dùng đã đăng ký, Biên tập viên/Moderator, Quản trị viên.

---

# 2. Mục tiêu & KPI
- Tăng tỷ lệ đăng ký tài khoản ≥ 15%/tháng trong 3 tháng đầu.
- Tỷ lệ nội dung do người dùng tạo (đánh giá/nhận xét) ≥ 0.8 bài/người dùng hoạt động/tháng.
- Thời gian phản hồi (TTFB) < 300ms cho trang cache; < 1.5s cho truy vấn chưa cache.
- 99.9% uptime (SLA nội bộ).

---

# 3. Phân hệ & Tính năng chính
## 3.1. Quản lý người dùng & xác thực
- Đăng ký/Đăng nhập (email + mật khẩu, OAuth: Google, Facebook – tùy chọn giai đoạn 2).
- Xác thực email, đặt lại mật khẩu, đổi email, đổi mật khẩu.
- Hồ sơ người dùng: avatar, bio ngắn, liên kết mạng xã hội, danh sách kệ sách (bookshelf), trạng thái đọc (đang đọc/đã đọc/muốn đọc/bỏ dở), thống kê cá nhân.
- Quyền & vai trò: Guest, User, Moderator, Admin.
- Quản lý chặn người dùng, khóa/bật tài khoản, rate limit hành vi (đăng nhận xét, gửi báo cáo).

## 3.2. Danh mục sách
- Thực thể: Sách, Tác giả, Dịch giả (optional), Nhà xuất bản, Thể loại/Tag, Series, Ấn bản (Edition), Ngôn ngữ, ISBN-10/13, năm xuất bản, số trang, bìa, mô tả, trích dẫn.
- CRUD cho Admin/Moderator; gợi ý chỉnh sửa từ cộng đồng (moderation queue).
- Nhập liệu: nhập thủ công, import CSV; tích hợp tra cứu ngoài (giai đoạn 2 — module adapter Google Books API/Open Library).

## 3.3. Đánh giá & Nhận xét (UGC)
- Người dùng cho **điểm số** (1–5 sao, cho phép nửa sao) **một lần/ấn bản**; có thể chỉnh sửa.
- **Review dài** (markdown cơ bản), **comment** tại review và tại trang sách.
- **Reactions** (hữu ích/cảm ơn) cho review; tính điểm uy tín (reputation) tác giả review.
- Gắn **spoiler tag**; ẩn nội dung spoiler mặc định.
- Báo cáo vi phạm (report) với lý do; moderation tools.

## 3.4. Khám phá & Tìm kiếm
- Tìm kiếm nhanh theo tiêu đề/tác giả/ISBN; nâng cao theo thể loại, năm xuất bản, ngôn ngữ, NXB, số trang, xếp hạng trung bình, số lượng đánh giá.
- Trang **Khám phá**: sách thịnh hành, sách mới, xếp hạng theo thể loại, đề xuất theo lịch sử đọc.
- Bộ lọc, sắp xếp (mới nhất, nổi bật, điểm trung bình cao, nhiều đánh giá nhất).

## 3.5. Kệ sách & Trạng thái đọc
- Tạo kệ tùy biến (ví dụ: “Sách mua 2025”, “Fantasy yêu thích”).
- Mark trạng thái: muốn đọc/đang đọc/đã đọc/bỏ dở; trường ngày bắt đầu/kết thúc, ghi chú, số lần đọc lại.
- Thống kê tiến độ: số trang/ngày, biểu đồ (giai đoạn 2 bằng chart lib phía client).

## 3.6. Thông báo & Theo dõi
- Theo dõi tác giả/sách/người dùng.
- Thông báo trong site (in‑app) khi có bình luận mới, phản hồi, sách mới cùng series, review từ người theo dõi.
- Email digest (tùy chọn bật/tắt) hằng tuần.

## 3.7. Quản trị (Admin)
- Dashboard: tổng số user, review, bình luận, báo cáo, sách chờ duyệt.
- Moderation queue: duyệt/chỉnh sửa/gộp trùng sách, xử lý report, tạm ẩn nội dung.
- Quản lý banner, trang tĩnh (Giới thiệu/FAQ/Điều khoản/Chính sách riêng tư).
- Công cụ SEO: chỉnh slug, meta tags, sitemap.xml, robots.txt.
- Nhật ký hệ thống (audit log) theo hành động Admin/Moderator.

---

# 4. Phân quyền & Ma trận quyền
| Hành động | Guest | User | Moderator | Admin |
|---|---|---|---|---|
| Xem sách, review | ✓ | ✓ | ✓ | ✓ |
| Tạo review/đánh giá |  | ✓ | ✓ | ✓ |
| Bình luận/reaction |  | ✓ | ✓ | ✓ |
| Báo cáo vi phạm |  | ✓ | ✓ | ✓ |
| Sửa/Xóa review của người khác |  |  | ✓ (theo phạm vi) | ✓ |
| CRUD Sách/Tác giả |  |  | ✓ | ✓ |
| Quản lý user |  |  |  | ✓ |

---

# 5. Yêu cầu phi chức năng
- **Bảo mật:** OWASP Top 10; CSRF, XSS, SQLi bảo vệ mặc định Laravel; mật khẩu bcrypt/argon2id; 2FA (giai đoạn 2). Rate limiting & throttling.
- **Hiệu năng:** Cache view/route/query; phân trang mọi listing; index DB bắt buộc; queue cho email/thông báo; CDN cho ảnh bìa.
- **Khả năng mở rộng:** Triển khai scale‑out (Nginx + nhiều PHP‑FPM), tách search engine, object storage (S3/minio) cho ảnh.
- **Khả dụng:** Backup hàng ngày; snapshot DB; phục hồi RTO ≤ 2h, RPO ≤ 15m (giai đoạn 2 với binlog).
- **Khả dụng đa ngôn ngữ (i18n):** VN/EN; định dạng số/ngày theo locale.
- **Khả năng truy cập (a11y):** Tuân theo WCAG 2.1 AA cơ bản.
- **SEO:** SSR, meta OpenGraph/Twitter, sitemap, canonical, breadcrumbs, URL thân thiện.
- **Logging & Quan sát:** Monolog + JSON log; request ID; metrics Prometheus (giai đoạn 2); Sentry/Elastic APM.

---

# 6. Kiến trúc & luồng
- **Kiến trúc:** MVC (Laravel). Module hoá theo domain: Catalog, Review, User, Moderation, Notification.
- **Luồng điển hình:**
  1) User tìm sách → mở trang sách.
  2) Đăng nhập → chấm sao + viết review (markdown, spoiler optional).
  3) Review vào moderation soft‑rules (chặn từ nhạy cảm) → nếu sạch, public; nếu vi phạm, vào hàng đợi.
  4) Người khác comment/reaction → chủ review nhận thông báo.

---

# 7. Thiết kế dữ liệu (DB schema đề xuất)
> Kiểu dữ liệu dùng MySQL 8.0, `utf8mb4`.

**Bảng chính:**
- `users(id, name, email, password_hash, avatar_url, bio, role, is_active, email_verified_at, created_at, updated_at)`
- `authors(id, name, slug, bio, birthday, country, created_at, updated_at)`
- `publishers(id, name, slug, website, created_at, updated_at)`
- `series(id, name, slug, description)`
- `books(id, title, slug, author_id, publisher_id, series_id, language, published_year, pages, isbn10, isbn13, cover_url, description, avg_rating, ratings_count, reviews_count, created_at, updated_at)`
- `book_tags(id, name, slug)`
- `book_tag_pivot(book_id, tag_id)` (PK: book_id+tag_id)
- `editions(id, book_id, format, isbn10, isbn13, published_year, pages, cover_url)`
- `reviews(id, user_id, book_id, edition_id, title, body_md, body_html, rating, is_spoiler, status[ pending|published|hidden ], helpful_count, created_at, updated_at)`
- `comments(id, user_id, review_id/null, book_id/null, body_md, body_html, is_spoiler, status, created_at, updated_at)`
- `reactions(id, user_id, review_id, type[helpful|like|insightful], created_at)` (unique: user_id+review_id)
- `bookshelves(id, user_id, name, is_public)`
- `bookshelf_items(id, bookshelf_id, book_id, note, added_at)` (unique: bookshelf_id+book_id)
- `reading_statuses(id, user_id, book_id, status[want|reading|read|abandoned], started_at, finished_at, progress_pages)` (unique: user_id+book_id)
- `follows(id, follower_id, target_user_id/null, author_id/null, book_id/null, created_at)`
- `notifications(id, user_id, type, data(JSON), read_at, created_at)`
- `reports(id, reporter_id, target_type, target_id, reason, note, status[open|reviewing|resolved], created_at, updated_at)`
- `audit_logs(id, actor_id, action, target_type, target_id, meta JSON, created_at)`

**Chỉ mục khuyến nghị:**
- `books(slug)`, `authors(slug)`, `publishers(slug)`, `book_tags(slug)` unique.
- `reviews(book_id, rating)`, `reviews(user_id)`, `comments(book_id)`, `comments(review_id)`.
- Full‑text: `books(title, description)`, `authors(name)`, `reviews(title, body_html)` nếu dùng MySQL InnoDB FTS (hoặc đẩy qua search engine).

---

# 8. API nội bộ (REST)
Tiền tố `/api/v1` (JWT cho user, token riêng cho admin tool).

**Auth**
- `POST /auth/register` → 201 {user}
- `POST /auth/login` → 200 {token}
- `POST /auth/logout` → 204
- `POST /auth/password/forgot` → 204
- `POST /auth/password/reset` → 204

**Catalog**
- `GET /books` (q, filters, sort, page) → {items, meta}
- `GET /books/{id|slug}` → {book, editions, stats, top_reviews}
- `GET /authors` / `GET /authors/{id|slug}`
- `GET /tags` / `GET /tags/{slug}/books`

**UGC**
- `POST /books/{id}/ratings` → 200 {avg_rating}
- `POST /books/{id}/reviews` → 201 {review}
- `PATCH /reviews/{id}` / `DELETE /reviews/{id}`
- `POST /reviews/{id}/comments` → 201 {comment}
- `POST /reviews/{id}/reactions` → 200 {helpful_count}
- `POST /reports` → 201 {report}

**Social**
- `POST /follow` / `DELETE /follow`
- `GET /notifications` → {items}
- `GET /me/bookshelves` / `POST /me/bookshelves` / `POST /me/bookshelves/{id}/items`
- `POST /me/reading-status`

**Admin**
- `GET /admin/dashboard`
- `POST /admin/books` / `PATCH /admin/books/{id}` / `DELETE /admin/books/{id}`
- `POST /admin/moderation/{type}/{id}/status`

---

# 9. Giao diện (UI/UX)
## 9.1. Trang chính
- Thanh tìm kiếm nổi bật, carousel sách nổi bật, danh sách “Xu hướng”, “Mới cập nhật”, “Xếp hạng cao”.

## 9.2. Trang sách
- Ảnh bìa, metadata, điểm trung bình, phân phối đánh giá (biểu đồ cột), nút “Đánh giá”, “Thêm vào kệ”, trạng thái đọc.
- Tab: Tổng quan | Review | Bình luận | Ấn bản | Trích dẫn.

## 9.3. Trang viết review
- Trình soạn thảo markdown (preview), checkbox **Spoiler**, chọn ấn bản, gợi ý quy tắc cộng đồng.

## 9.4. Trang hồ sơ cá nhân
- Avatar, bio, thống kê (số sách đã đọc/năm, điểm TB), danh sách kệ công khai, hoạt động gần đây.

## 9.5. Quản trị
- Bảng điều khiển, hàng đợi kiểm duyệt, CRUD danh mục, trang cài đặt SEO.

**Thiết kế responsive**, dark mode (giai đoạn 2).

---

# 10. Quy tắc kinh doanh & ràng buộc
- Mỗi người dùng chỉ được 1 rating/1 ấn bản; cho phép sửa nhưng ghi nhật ký.
- Review phải ≥ 50 ký tự; comment ≥ 5 ký tự; chống spam (akismet-like optional, throttle).
- Nội dung có thể bị ẩn khi bị báo cáo ≥ N lần (ngưỡng cấu hình) cho đến khi Moderator xử lý.
- Tên sách/slug duy nhất; sách trùng có thể gộp (merge) và chuyển hướng slug cũ → mới.

---

# 11. Bảo mật & riêng tư
- Bắt buộc HTTPS, HSTS, secure cookie, SameSite=Lax/Strict.
- Chính sách dữ liệu: cho phép tải xuống dữ liệu cá nhân, xoá tài khoản (GDPR‑like).
- Phân tách quyền theo policy/gate Laravel; audit log mọi hành động quan trọng.

---

# 12. Kiểm thử & chấp nhận
- **Unit test:** Model, Service, Policy.
- **Feature test:** Auth, CRUD review, rating, comment, search.
- **API contract test:** OpenAPI/Swagger.
- **Performance test:** k6/JMeter: trang sách P95 < 800ms (không cache), P99 < 1.2s.
- **Bảo mật:** kiểm tra OWASP ZAP, dependency audit (Composer audit).

**Tiêu chí nghiệm thu (UAT):**
- Tạo tài khoản, xác thực email thành công.
- Thêm 200k bản ghi sách qua import CSV, tìm kiếm vẫn đáp ứng P95 < 1.2s (with index/search engine).
- Viết/sửa/xoá review, đánh dấu spoiler, người khác thấy bị ẩn spoiler.
- Moderator xử lý report → thay đổi trạng thái hiển thị tức thời.

---

# 13. Lộ trình triển khai (Roadmap gợi ý)
- **Sprint 1 (2 tuần):** Auth cơ bản, Catalog tối thiểu (Book/Author), trang sách, rating đơn giản.
- **Sprint 2 (2 tuần):** Review/Comment/Reaction, Search cơ bản, Bookshelf/Reading status.
- **Sprint 3 (2 tuần):** Admin dashboard, Moderation queue, SEO cơ bản.
- **Sprint 4 (2 tuần):** Thông báo in‑app, Email digest, Import CSV, tối ưu hiệu năng.
- **Giai đoạn 2:** OAuth, Recommendation, External API import, Dark mode, Mobile PWA.

---

# 14. DevOps & vận hành
- Docker Compose mẫu: `nginx`, `app`, `db`, `redis`, `meilisearch`.
- CI/CD: chạy test, static analysis (PHPStan Psalm), deploy tới staging → production.
- Migrations & seeders; bật Telescope/Debugbar ở local.
- Backup chiến lược: full dump hằng ngày + binlog; lưu object storage 7–30 ngày.

---

# 15. Tài liệu & bàn giao
- Tài liệu kiến trúc (ADR), ERD, OpenAPI, Hướng dẫn cài đặt & .env mẫu.
- Bộ mock data (CSV) ~1k sách để UAT.

---

# 16. Phụ lục
## 16.1. Trường hợp sử dụng (User Stories – mẫu)
- *Là người dùng*, tôi muốn tìm sách theo tên hoặc tác giả để nhanh chóng mở trang chi tiết.
- *Là người dùng*, tôi muốn chấm điểm và viết review có spoiler để chia sẻ trải nghiệm đọc.
- *Là moderator*, tôi muốn xem báo cáo vi phạm và ẩn nội dung trong 1 click.
- *Là admin*, tôi muốn gộp 2 sách trùng để tránh dữ liệu rác.

## 16.2. Quy ước mã & chất lượng
- PSR-12 coding style, PHP 8.3.
- Repository/Service pattern cho logic nghiệp vụ; Form Request cho validate.
- DTO (spatie/laravel-data) cho payload; Policy/Gate cho uỷ quyền; Observer cho thống kê.

> **Ghi chú:** Tài liệu này có thể dùng làm SRS/PRD khởi đầu và được tinh chỉnh theo phản hồi stakeholder. Có thể chuyển đổi sang checklist thực thi cho từng sprint.

