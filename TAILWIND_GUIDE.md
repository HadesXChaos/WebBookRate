# Hướng dẫn sử dụng Tailwind CSS và các thư viện UI/UX

Tài liệu này mô tả cách sử dụng Tailwind CSS và các thư viện JavaScript đã được tích hợp vào BookReview.vn.

## 📚 Danh sách thư viện

### 1. Tailwind CSS (CDN)
**Mục đích:** Utility-first CSS framework

**Cách sử dụng:**
```html
<!-- Sử dụng các class Tailwind -->
<button class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
  Nút chính
</button>

<div class="flex items-center justify-between p-4 bg-white rounded-lg shadow-md">
  <h2 class="text-2xl font-bold">Tiêu đề</h2>
  <span class="text-gray-500">Subtitle</span>
</div>
```

**Tài liệu:** https://tailwindcss.com/docs

---

### 2. Alpine.js 3.x
**Mục đích:** Lightweight JavaScript framework cho interactivity

**Cách sử dụng:**
```html
<!-- Toggle visibility -->
<div x-data="{ open: false }">
  <button @click="open = !open" class="btn">Toggle</button>
  <div x-show="open" x-transition>
    Nội dung hiển thị/ẩn
  </div>
</div>

<!-- Dropdown menu -->
<div x-data="{ open: false }" class="relative">
  <button @click="open = !open">Menu</button>
  <div x-show="open" 
       @click.away="open = false"
       x-transition
       class="absolute top-full right-0 mt-2">
    <a href="#">Item 1</a>
    <a href="#">Item 2</a>
  </div>
</div>
```

**Tài liệu:** https://alpinejs.dev/

---

### 3. Font Awesome 6.5.1
**Mục đích:** Icon library

**Cách sử dụng:**
```html
<i class="fas fa-heart text-red-500"></i>
<i class="far fa-bookmark"></i>
<i class="fab fa-facebook"></i>
```

**Tài liệu:** https://fontawesome.com/icons

---

### 4. AOS (Animate On Scroll) 2.3.4
**Mục đích:** Animation khi scroll

**Cách sử dụng:**
```html
<div data-aos="fade-up">Nội dung sẽ fade up khi scroll đến</div>
<div data-aos="zoom-in" data-aos-delay="200">Zoom in với delay</div>
```

**Các animation phổ biến:**
- `fade-up`, `fade-down`, `fade-left`, `fade-right`
- `zoom-in`, `zoom-out`
- `flip-left`, `flip-right`
- `slide-up`, `slide-down`

**Tài liệu:** https://michalsnik.github.io/aos/

---

### 5. Swiper 11
**Mục đích:** Carousel/Slider hiện đại

**Cách sử dụng:**
```html
<div class="swiper">
  <div class="swiper-wrapper">
    <div class="swiper-slide">Slide 1</div>
    <div class="swiper-slide">Slide 2</div>
    <div class="swiper-slide">Slide 3</div>
  </div>
  <div class="swiper-pagination"></div>
  <div class="swiper-button-prev"></div>
  <div class="swiper-button-next"></div>
</div>

<script>
BookReview.initSwiper('.swiper', {
  slidesPerView: 3,
  spaceBetween: 20,
  loop: true
});
</script>
```

**Tài liệu:** https://swiperjs.com/

---

### 6. Chart.js 4.4.1
**Mục đích:** Vẽ biểu đồ

**Cách sử dụng:**
```html
<div class="chart-container">
  <canvas id="myChart"></canvas>
</div>

<script>
const ctx = document.getElementById('myChart');
new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Tháng 1', 'Tháng 2', 'Tháng 3'],
    datasets: [{
      label: 'Số sách đọc',
      data: [12, 19, 15],
      borderColor: 'rgb(37, 99, 235)',
      tension: 0.4
    }]
  }
});
</script>
```

**Tài liệu:** https://www.chartjs.org/docs/latest/

---

### 7. SweetAlert2 11.10.5
**Mục đích:** Thông báo và dialog đẹp

**Cách sử dụng:**
```javascript
// Sử dụng qua BookReview.utils
BookReview.utils.showAlert('Thành công!', 'success');
BookReview.utils.showAlert('Có lỗi xảy ra!', 'error');

// Confirmation dialog
BookReview.utils.showConfirm('Bạn có chắc muốn xóa?', 'Xác nhận')
  .then((result) => {
    if (result.isConfirmed) {
      // Xử lý khi xác nhận
    }
  });
```

**Tài liệu:** https://sweetalert2.github.io/

---

### 8. LazySizes 5.3.2
**Mục đích:** Lazy loading images

**Cách sử dụng:**
```html
<!-- Thay src bằng data-src và thêm class lazyload -->
<img data-src="{% static 'images/book.jpg' %}" 
     class="lazyload rounded-lg" 
     alt="Book cover">
```

**Tài liệu:** https://github.com/aFarkas/lazysizes

---

### 9. SortableJS 1.15.0
**Mục đích:** Drag and drop để sắp xếp

**Cách sử dụng:**
```javascript
const sortable = BookReview.initSortable(document.getElementById('my-list'), {
  onEnd: function(evt) {
    const newOrder = Array.from(evt.to.children).map((el, index) => ({
      id: el.dataset.id,
      order: index
    }));
    // Gửi API để cập nhật thứ tự
  }
});
```

**Tài liệu:** https://sortablejs.github.io/Sortable/

---

### 10. Marked.js 11.1.1
**Mục đích:** Parse Markdown thành HTML

**Cách sử dụng:**
```javascript
const markdown = '# Tiêu đề\n\nĐây là **nội dung** markdown.';
const html = BookReview.utils.renderMarkdown(markdown);
document.getElementById('preview').innerHTML = html;
```

**Tài liệu:** https://marked.js.org/

---

### 11. DOMPurify 3.0.6
**Mục đích:** Sanitize HTML để tránh XSS

**Cách sử dụng:**
```javascript
// Đã được tích hợp tự động trong renderMarkdown
// Hoặc sử dụng trực tiếp
const dirty = '<img src=x onerror=alert(1)>';
const clean = DOMPurify.sanitize(dirty);
```

**Tài liệu:** https://github.com/cure53/DOMPurify

---

## 🎨 Ví dụ tích hợp Tailwind

### Card với Tailwind
```html
<div class="max-w-sm rounded-lg overflow-hidden shadow-lg bg-white">
  <img class="w-full h-48 object-cover" src="book.jpg" alt="Book">
  <div class="px-6 py-4">
    <div class="font-bold text-xl mb-2">Tên sách</div>
    <p class="text-gray-700 text-base">Mô tả ngắn về cuốn sách...</p>
  </div>
  <div class="px-6 pt-4 pb-2">
    <span class="inline-block bg-blue-200 rounded-full px-3 py-1 text-sm font-semibold text-blue-800 mr-2 mb-2">
      #Fiction
    </span>
  </div>
</div>
```

### Grid Layout với Tailwind
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  <div class="bg-white rounded-lg shadow p-4">Item 1</div>
  <div class="bg-white rounded-lg shadow p-4">Item 2</div>
  <div class="bg-white rounded-lg shadow p-4">Item 3</div>
  <div class="bg-white rounded-lg shadow p-4">Item 4</div>
</div>
```

### Button với Tailwind
```html
<button class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition-colors duration-200">
  Click me
</button>

<button class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">
  Outline Button
</button>
```

### Form với Tailwind
```html
<form class="max-w-md mx-auto">
  <div class="mb-4">
    <label class="block text-gray-700 text-sm font-bold mb-2" for="email">
      Email
    </label>
    <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" 
           id="email" type="email" placeholder="Email">
  </div>
  <div class="mb-6">
    <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
      Password
    </label>
    <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" 
           id="password" type="password" placeholder="Password">
  </div>
  <div class="flex items-center justify-between">
    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" 
            type="button">
      Sign In
    </button>
  </div>
</form>
```

---

## 🔧 Global Objects

Tất cả các thư viện và utilities có thể truy cập qua `window.BookReview`:

```javascript
// Utilities
BookReview.utils.showAlert(message, type);
BookReview.utils.showConfirm(message, title);
BookReview.utils.renderMarkdown(markdown);
BookReview.utils.getCsrfToken();
BookReview.utils.apiRequest(url, method, data);
BookReview.utils.debounce(func, wait);

// Functions
BookReview.renderStars(rating, container);
BookReview.initSortable(element, options);
BookReview.initSwiper(selector, options);

// Libraries
BookReview.Swal  // SweetAlert2
BookReview.Chart // Chart.js
BookReview.Swiper // Swiper
```

---

## 📝 Ví dụ hoàn chỉnh

### Book List với Swiper và Tailwind
```html
<div class="swiper my-8">
  <div class="swiper-wrapper">
    {% for book in books %}
    <div class="swiper-slide">
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <img data-src="{{ book.cover.url }}" 
             class="lazyload w-full h-64 object-cover" 
             alt="{{ book.title }}">
        <div class="p-4">
          <h3 class="font-bold text-lg mb-2">{{ book.title }}</h3>
          <p class="text-gray-600 text-sm">{{ book.author.name }}</p>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
  <div class="swiper-pagination"></div>
  <div class="swiper-button-prev"></div>
  <div class="swiper-button-next"></div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  BookReview.initSwiper('.swiper', {
    slidesPerView: 1,
    spaceBetween: 20,
    breakpoints: {
      640: { slidesPerView: 2 },
      768: { slidesPerView: 3 },
      1024: { slidesPerView: 4 }
    }
  });
});
</script>
```

### Review Editor với Markdown Preview
```html
<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
  <div>
    <label class="block text-sm font-medium mb-2">Nhập Review (Markdown)</label>
    <textarea id="review-content" 
              class="w-full h-96 p-4 border rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="# Tiêu đề..."></textarea>
  </div>
  <div>
    <label class="block text-sm font-medium mb-2">Preview</label>
    <div id="markdown-preview" 
         class="w-full h-96 p-4 border rounded-lg bg-gray-50 overflow-y-auto">
      <p class="text-gray-500">Nhập nội dung để xem preview...</p>
    </div>
  </div>
</div>

<script>
const textarea = document.getElementById('review-content');
const preview = document.getElementById('markdown-preview');

textarea.addEventListener('input', function() {
  const html = BookReview.utils.renderMarkdown(this.value);
  preview.innerHTML = html || '<p class="text-gray-500">Nhập nội dung để xem preview...</p>';
});
</script>
```

---

## 🎯 Best Practices

1. **Sử dụng Tailwind utilities** thay vì viết CSS custom khi có thể
2. **Kết hợp Tailwind với Alpine.js** cho interactivity
3. **Luôn sử dụng BookReview.utils.showAlert()** thay vì `alert()`
4. **Sanitize HTML** trước khi render (tự động trong `renderMarkdown`)
5. **Sử dụng lazy loading** cho tất cả images lớn
6. **Thêm AOS animations** cho các section quan trọng
7. **Test responsive** trên mobile và desktop

---

## 🐛 Troubleshooting

### Tailwind classes không hoạt động?
- Đảm bảo Tailwind CDN đã load trong `base.html`
- Kiểm tra console để xem lỗi
- Một số class cần prefix như `hover:`, `md:`, `lg:`

### Alpine.js không hoạt động?
- Đảm bảo `x-data` đã được khai báo
- Kiểm tra xem Alpine đã load chưa: `typeof Alpine !== 'undefined'`

### Swiper không hiển thị?
- Đảm bảo HTML structure đúng (swiper-wrapper, swiper-slide)
- Kiểm tra CSS đã load chưa
- Gọi `BookReview.initSwiper()` sau khi DOM ready

---

## 📚 Tài liệu tham khảo

- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Alpine.js Docs](https://alpinejs.dev/)
- [Swiper Documentation](https://swiperjs.com/)
- [AOS Documentation](https://michalsnik.github.io/aos/)
- [Chart.js Guide](https://www.chartjs.org/docs/latest/)
- [SweetAlert2 Examples](https://sweetalert2.github.io/)

