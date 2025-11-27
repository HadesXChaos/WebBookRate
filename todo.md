# TODO – Kế hoạch hoàn thiện BookReview.vn

**Nguồn tham chiếu chính:** `requirement.md`, tài liệu rubric *“Yêu cầu tiểu luận và tiêu chí đánh giá.pdf”*, repo code hiện tại (Django + DRF).  
**Mục tiêu:** đưa sản phẩm đạt đủ 6 chương theo rubric, đáp ứng toàn bộ user stories trong SRS, sẵn sàng bảo vệ đồ án.

---

## Chương 1 – Giới thiệu, mục tiêu và kế hoạch

| ID | Task | Liên quan | Trạng thái |
|----|------|-----------|------------|
| C1-01 | Viết lại phần mô tả đề tài, mục tiêu, đối tượng, phạm vi dựa trên Section 1–4 của `requirement.md`. | Document | ☐ |
| C1-02 | Lập stakeholder map + ma trận vai trò/quyền (Anonymous/User/Moderator/Admin). | Document | ☐ |
| C1-03 | Thiết kế sitemap tổng thể (home, books, reviews, shelves, social, moderation, auth, explore). Xuất bản trong phụ lục. | Frontend/Docs | ☐ |
| C1-04 | Mô tả kiến trúc triển khai (Dockerized Django + Postgres + Redis + Celery + S3). Gắn với tiêu chí “domain & hosting”. | DevOps/Docs | ☐ |
| C1-05 | Lập kế hoạch thực hiện (timeline theo sprint + phân công nhiệm vụ). Chuyển roadmap MVP/V1 trong SRS thành bảng tiến độ. | PM/Docs | ☐ |

---

## Chương 2 – Thiết kế & Xây dựng Frontend

| ID | Task | Liên quan | Trạng thái |
|----|------|-----------|------------|
| C2-01 | Xây dựng brand kit: palette, typography, spacing, components guideline; cập nhật `static/css/main.css`. | UI/CSS | ☐ |
| C2-02 | Tạo wireframe/hi-fi cho: Home, Explore, Book detail, Review detail, Profile, Shelves, Notifications, Moderator dashboard, Collections, Reading progress chart. | UX/Docs | ☐ |
| C2-03 | Bổ sung template cho Collections CRUD (tận dụng `social` app) + giao diện drag-drop reorder. | Templates/JS | ☐ |
| C2-04 | Implement reading progress visualization (chart + history timeline) trong `shelves` templates + JS (Chart.js/D3). | Templates/JS | ☐ |
| C2-05 | Hoàn thiện Explore page: filter panel (genre/year/lang/rating), sections trending/new/personalized. | Templates | ☐ |
| C2-06 | Thêm inline markdown preview + autosave draft khi viết review (JS module trong `static/js/main.js`). | JS/Reviews | ☐ |
| C2-07 | Thêm mention autocomplete UI trong comment editor (frontend). | JS/Reviews | ☐ |
| C2-08 | Thêm realtime notification badge (polling/WebSocket stub) + UI update. | JS/Social | ☐ |
| C2-09 | Đảm bảo responsive breakpoints, dark mode toggle cơ bản. | CSS | ☐ |
| C2-10 | Viết phần mô tả “Chức năng nâng cao” (lazy-load hình, markdown preview, realtime badge) trong tài liệu chương 2. | Docs | ☐ |

**Chi tiết thực hiện C2**

- **C2-01 Brand kit**
  - Tổng hợp yêu cầu nhận diện trong `requirement.md`, tham khảo palette thương hiệu BookReview.vn hiện có.
  - Định nghĩa màu chính/phụ, trạng thái (hover, error, success), typography scale (heading H1–H6, body, caption), spacing system (4/8pt).
  - Cập nhật `static/css/main.css` với CSS variables (`:root { --color-primary: ... }`) và chuẩn hóa mixins/utility classes.
  - Xuất bảng guideline (PDF/appendix) để reuse cho các template khác.
- **C2-02 Wireframe/Hi-fi**
  - Dùng Figma (hoặc công cụ tương đương) tạo flow đầy đủ cho 10 màn hình đã nêu; mỗi màn hình gồm desktop + mobile breakpoint.
  - Dán link Figma vào phụ lục + export PNG đặt tại `docs/figures/frontend`.
  - Note state quan trọng: empty state, loading, error, skeleton.
- **C2-03 Collections UI**
  - Tạo template mới `templates/social/collection_list.html`, `collection_detail.html`, `collection_form.html`.
  - Bổ sung form partial, include validation error, flash message.
  - Thêm module JS xử lý drag-and-drop (HTML5 API hoặc SortableJS), gửi thứ tự mới qua endpoint `/collections/<id>/reorder/`.
  - Style card collection dùng brand kit; đảm bảo trạng thái public/private badge.
- **C2-04 Reading progress viz**
  - Quyết định thư viện (Chart.js ưu tiên). Load qua `static/js/vendor/chart.min.js`.
  - API `shelves/progress` trả JSON { week, pages, status }; hiển thị line chart + timeline card list.
  - Thêm legend, tooltip, xử lý empty state (“Chưa có log đọc nào”).
  - Responsive: chart chuyển sang sparkline trên mobile.
- **C2-05 Explore page**
  - Thiết kế filter panel trái (accordion) với multi-select genre, slider year, toggle language, rating stars.
  - Section top: Trending, New arrivals, Personalized (dữ liệu mock nếu backend chưa xong).
  - Áp dụng infinite scroll/lazy-load; fallback pagination.
  - SEO: heading, breadcrumb, meta description customizable.
- **C2-06 Markdown preview + autosave**
  - Module `static/js/review-editor.js`: debounce input, render markdown preview (marked.js) bên phải.
  - Autosave draft vào localStorage mỗi 5s; hiển thị toast khi khôi phục.
  - Sanitizer cho preview (DOMPurify) để tránh XSS.
  - Hook vào form submit để xóa draft sau khi thành công.
- **C2-07 Mention autocomplete**
  - Reuse API `/api/mentions/search?q=` trả user/book/author.
  - JS component lắng nghe `@` trong textarea, hiển thị dropdown (keyboard navigation).
  - Insert tag dạng `[@username](user:123)` để backend parse.
  - Bao phủ cả comment + review editor; cân nhắc aria-role listbox.
- **C2-08 Realtime notification badge**
  - Tạo endpoint polling `/notifications/unread-count/` (5s) hoặc WebSocket stub qua Django Channels.
  - Badge trên navbar cập nhật số lượng, pulsate khi >0.
  - Dropdown hiển thị 5 mục mới nhất, link tới trang Notifications.
  - Graceful degradation: nếu WebSocket lỗi fallback polling.
- **C2-09 Responsive + dark mode**
  - Xác định breakpoint xs (<480), sm, md, lg, xl; tạo mixin SCSS hoặc CSS @media chuẩn.
  - Kiểm tra từng template chính; sửa layout để tránh overflow.
  - Dark mode toggle lưu prefer trong localStorage, apply class `theme-dark`; dùng CSS variables để đổi màu.
  - Test contrast ratio ≥4.5/3.0, focus state rõ ràng.
- **C2-10 Docs “Chức năng nâng cao”**
  - Tổng hợp mô tả kỹ thuật cho lazy-load image (IntersectionObserver), markdown preview, realtime badge.
  - Đưa screenshot minh họa + flow diagram (nếu cần) vào Chapter 2 document.
  - Liên kết commit/PR tương ứng, mô tả lợi ích (UX, performance).
  - Chuẩn bị checklist demo để giảng viên dễ kiểm chứng.

---

## Chương 3 – Backend & Cơ sở dữ liệu

| ID | Task | Liên quan | Trạng thái |
|----|------|-----------|------------|
| C3-01 | Cập nhật ERD + docs phản ánh models hiện tại (Users, Books, Reviews, Shelves, Social, Moderation). | Docs | ☐ |
| C3-02 | Hoàn thiện OAuth (Google/Facebook/Apple) bằng django-allauth hoặc social-auth; cấu hình callback + secrets. | Auth | ☐ |
| C3-03 | Implement anti-spam pipeline: banned words config, Akismet (hoặc rule engine), nâng throttle review/comment. | Moderation | ☐ |
| C3-04 | Thêm review edit history (version table + API + admin view). | Reviews | ☐ |
| C3-05 | Implement mention backend: parser, `Mention` model (or reuse notifications), trigger noti + highlight. | Reviews/Social | ☐ |
| C3-06 | Hoàn thiện follow system cho author/book/user (API + signals cho feed). | Social | ☐ |
| C3-07 | Collections API đầy đủ (CRUD, share/private, cover upload). | Social | ☐ |
| C3-08 | Reading progress API v2: weekly aggregation, summary endpoint, Celery job để rebuild stats. | Shelves/Celery | ☐ |
| C3-09 | Reports SLA tracking: store timestamps, expose SLA status, auto reminders, moderator action log UI/API. | Moderation | ☐ |
| C3-10 | Precompute trending/top books job (Celery) + cache invalidation. | Books/Celery | ☐ |
| C3-11 | Import CSV/ISBN + OpenLibrary integration (async fetch via Celery, CLI command, admin UI). | Books/Integrations | ☐ |
| C3-12 | GDPR export/delete workflow + data packaging job. | Users/Compliance | ☐ |
| C3-13 | Document session/cookie strategy + client-side state management per rubric. | Docs/Security | ☐ |
| C3-14 | Harden security: 2FA (TOTP/email), CAPTCHA, CSP headers, rate-limit for moderation endpoints. | Security | ☐ |

---

## Chương 4 – Kiểm thử & Tối ưu hóa

| ID | Task | Liên quan | Trạng thái |
|----|------|-----------|------------|
| C4-01 | Viết test matrix chi tiết (theo Section 14 requirement). | QA/Docs | ☐ |
| C4-02 | Nâng code coverage ≥90%: thêm unit/integration tests cho social, moderation, import, Celery jobs, OAuth. | QA/Code | ☐ |
| C4-03 | Thiết lập load test (k6/Locust) cho search, review creation, notification feed; lưu kết quả. | Performance | ☐ |
| C4-04 | Tối ưu truy vấn (prefetch/select_related audits) và cache miss analysis cho endpoints nặng. | Backend/Perf | ☐ |
| C4-05 | SEO/A11y audit: Lighthouse ≥80/95, fix ARIA roles, heading structure, keyboard trap. | Frontend | ☐ |
| C4-06 | Cross-browser/device test matrix (Chrome/Firefox/Safari/Edge + mobile breakpoints). | QA | ☐ |
| C4-07 | Performance profiling Celery jobs (stats in Prometheus/Sentry). | DevOps | ☐ |

---

## Chương 5 – Triển khai & Đánh giá

| ID | Task | Liên quan | Trạng thái |
|----|------|-----------|------------|
| C5-01 | Hoàn thiện `.env` templates cho dev/staging/prod + secrets rotation guide. | DevOps | ☐ |
| C5-02 | Thiết lập CI/CD (GitHub Actions) chạy lint, tests, docker build, security scan (Bandit, Trivy). | DevOps | ☐ |
| C5-03 | Viết script deploy (Ansible/Terraform or documented manual) và chạy thử lên staging; ghi log so sánh hiệu suất trước/sau tối ưu (cache/CDN). | DevOps/Docs | ☐ |
| C5-04 | Thiết lập monitoring: Sentry, Prometheus metrics, Grafana dashboards, alert rules (latency, error rate, Celery backlog). | Observability | ☐ |
| C5-05 | Hoàn thiện health checks (`/healthz`, Celery beat job) + uptime documentation. | DevOps | ☐ |
| C5-06 | Chuẩn bị tài liệu đánh giá triển khai theo rubric (screenshot deploy, thông số). | Docs | ☐ |

---

## Chương 6 – Tổng kết & Phụ lục

| ID | Task | Liên quan | Trạng thái |
|----|------|-----------|------------|
| C6-01 | Viết chương tổng kết: kết quả đạt được, hạn chế, hướng phát triển (tham chiếu roadmap Section 20 SRS). | Docs | ☐ |
| C6-02 | Tổng hợp phụ lục: wireframe, ERD, test reports, Lighthouse, load test charts, deployment evidence. | Docs | ☐ |
| C6-03 | Chuẩn bị slide/demo script + account demo. | Presentation | ☐ |
| C6-04 | Checklist DoD (Section 23 SRS) + xác nhận không còn bug P0. | QA/Docs | ☐ |

---

## Cross-cutting Enhancements (không gắn chương cụ thể)

| ID | Task | Liên quan | Trạng thái |
|----|------|-----------|------------|
| X-01 | i18n: gettext setup (vi/en), locale switcher, translate templates. | Frontend/Backend | ☐ |
| X-02 | CDN/static optimization (Whitenoise/CloudFront config, cache headers). | DevOps | ☐ |
| X-03 | Advanced analytics dashboard (user growth, top genres, retention). | Backend/Data | ☐ |
| X-04 | Content moderation tooling UI (bulk actions, filters, audit trail). | Frontend/Moderation | ☐ |
| X-05 | Accessibility sweep (aria-labels, focus states, color contrast). | Frontend | ☐ |

---

## Theo dõi tiến độ

- Mỗi task cập nhật tình trạng: ☐ (chưa), ◐ (đang làm), ☐→☑ (hoàn thành).  
- Ưu tiên trước: C1-01 → C3-08 song song với C2-03/C2-04 để khóa nội dung chương 2–3; tiếp đến C4 nhóm testing; cuối cùng C5–C6 cho tài liệu và triển khai.  
- Họp sync hàng tuần: rà soát blocking issues, điều chỉnh timeline.

**Ghi chú:** File phải được cập nhật liên tục; mọi thay đổi quan trọng cần tham chiếu rõ tới module/code commit tương ứng.

