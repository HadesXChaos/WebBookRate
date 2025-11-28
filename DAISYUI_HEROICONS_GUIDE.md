# Hướng dẫn sử dụng DaisyUI, Heroicons, AOS và Swiper.js

Tài liệu này mô tả cách sử dụng các thư viện UI đã được tích hợp vào BookReview.vn.

## 📚 Danh sách thư viện

### 1. DaisyUI 4.4.19
**Mục đích:** Component library cho Tailwind CSS

**Cách sử dụng:**
```html
<!-- Buttons -->
<button class="btn btn-primary">Primary Button</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-outline">Outline</button>
<button class="btn btn-ghost">Ghost</button>

<!-- Cards -->
<div class="card bg-base-100 shadow-xl">
  <figure><img src="image.jpg" alt="Book" /></figure>
  <div class="card-body">
    <h2 class="card-title">Card Title</h2>
    <p>Card description</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary">Buy Now</button>
    </div>
  </div>
</div>

<!-- Alerts -->
<div class="alert alert-success">
  <svg>...</svg>
  <span>Success message!</span>
</div>

<!-- Badges -->
<span class="badge badge-primary">New</span>
<span class="badge badge-secondary">Hot</span>

<!-- Modals -->
<button onclick="my_modal_1.showModal()" class="btn">Open Modal</button>
<dialog id="my_modal_1" class="modal">
  <div class="modal-box">
    <h3 class="font-bold text-lg">Hello!</h3>
    <p class="py-4">Press ESC key or click outside to close</p>
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>

<!-- Dropdown -->
<div class="dropdown">
  <div tabindex="0" role="button" class="btn m-1">Click</div>
  <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
    <li><a>Item 1</a></li>
    <li><a>Item 2</a></li>
  </ul>
</div>

<!-- Stats -->
<div class="stats shadow">
  <div class="stat">
    <div class="stat-title">Total Books</div>
    <div class="stat-value">31K</div>
    <div class="stat-desc">21% more than last month</div>
  </div>
</div>

<!-- Rating -->
<div class="rating">
  <input type="radio" name="rating-2" class="mask mask-star-2 bg-orange-400" />
  <input type="radio" name="rating-2" class="mask mask-star-2 bg-orange-400" checked />
  <input type="radio" name="rating-2" class="mask mask-star-2 bg-orange-400" />
  <input type="radio" name="rating-2" class="mask mask-star-2 bg-orange-400" />
  <input type="radio" name="rating-2" class="mask mask-star-2 bg-orange-400" />
</div>
```

**Tài liệu:** https://daisyui.com/components/

---

### 2. Heroicons
**Mục đích:** Beautiful SVG icons

**Cách sử dụng:**
```html
<!-- Sử dụng JavaScript helper -->
<script>
  // Render icon
  const heartIcon = Heroicons.render('heart', 'outline', { class: 'w-6 h-6 text-red-500' });
  document.getElementById('icon-container').innerHTML = heartIcon;
</script>

<!-- Hoặc sử dụng trực tiếp SVG -->
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
  <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
</svg>

<!-- Icons có sẵn: heart, book, user, search, bell, home, star, bookmark, chevronDown, menu, xMark -->
```

**Tài liệu:** https://heroicons.com/

---

### 3. AOS (Animate On Scroll) 2.3.4
**Mục đích:** Animation khi scroll

**Cách sử dụng:**
```html
<!-- Basic usage -->
<div data-aos="fade-up">Content</div>
<div data-aos="fade-down">Content</div>
<div data-aos="fade-left">Content</div>
<div data-aos="fade-right">Content</div>

<!-- With delay -->
<div data-aos="zoom-in" data-aos-delay="200">Content</div>

<!-- With duration -->
<div data-aos="flip-left" data-aos-duration="1000">Content</div>

<!-- Animation types -->
<!-- fade-up, fade-down, fade-left, fade-right -->
<!-- zoom-in, zoom-out, zoom-in-up, zoom-in-down -->
<!-- flip-left, flip-right, flip-up, flip-down -->
<!-- slide-up, slide-down, slide-left, slide-right -->
```

**Tài liệu:** https://michalsnik.github.io/aos/

---

### 4. Swiper.js 11
**Mục đích:** Modern carousel/slider

**Cách sử dụng:**
```html
<!-- Basic Swiper -->
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
  // Initialize with BookReview utility
  BookReview.initSwiper('.swiper', {
    slidesPerView: 3,
    spaceBetween: 20,
    loop: true,
    autoplay: {
      delay: 3000,
    }
  });
</script>

<!-- Auto-initialize with data attributes -->
<div class="swiper" data-swiper data-swiper-config='{"slidesPerView": 3, "loop": true}'>
  <div class="swiper-wrapper">
    <div class="swiper-slide">Slide 1</div>
    <div class="swiper-slide">Slide 2</div>
  </div>
  <div class="swiper-pagination"></div>
</div>
```

**Tài liệu:** https://swiperjs.com/

---

### 5. Font Awesome 6.5.1
**Mục đích:** Icon library (đã có sẵn)

**Cách sử dụng:**
```html
<i class="fas fa-heart"></i>
<i class="far fa-bookmark"></i>
<i class="fab fa-facebook"></i>
```

**Tài liệu:** https://fontawesome.com/icons

---

## 🎨 Ví dụ tích hợp

### Book Card với DaisyUI
```html
<div class="card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow" data-aos="fade-up">
  <figure class="aspect-[2/3] overflow-hidden">
    <img data-src="{{ book.cover }}" alt="{{ book.title }}" class="lazyload w-full h-full object-cover" />
  </figure>
  <div class="card-body">
    <h2 class="card-title">{{ book.title }}</h2>
    <p class="text-gray-600">{{ book.author }}</p>
    <div class="card-actions justify-between items-center mt-4">
      <div class="rating rating-sm">
        {% for i in "12345" %}
        <input type="radio" name="rating-{{ book.id }}" class="mask mask-star-2 bg-yellow-400" {% if forloop.counter <= book.rating %}checked{% endif %} disabled />
        {% endfor %}
      </div>
      <span class="badge badge-primary">{{ book.rating|floatformat:1 }}</span>
    </div>
    <div class="card-actions justify-end mt-2">
      <button class="btn btn-primary btn-sm">Xem chi tiết</button>
    </div>
  </div>
</div>
```

### Modal với DaisyUI
```html
<!-- Trigger Button -->
<button onclick="book_modal_{{ book.id }}.showModal()" class="btn btn-primary">
  Xem chi tiết
</button>

<!-- Modal -->
<dialog id="book_modal_{{ book.id }}" class="modal">
  <div class="modal-box" data-aos="zoom-in">
    <h3 class="font-bold text-lg mb-4">{{ book.title }}</h3>
    <div class="flex gap-4">
      <img src="{{ book.cover }}" alt="{{ book.title }}" class="w-32 h-48 object-cover rounded" />
      <div class="flex-1">
        <p class="text-gray-600 mb-2">{{ book.author }}</p>
        <p class="mb-4">{{ book.description }}</p>
        <div class="flex gap-2">
          <button class="btn btn-primary">Thêm vào kệ</button>
          <button class="btn btn-outline">Đánh giá</button>
        </div>
      </div>
    </div>
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>
```

### Swiper Carousel với Books
```html
<div class="swiper my-8" data-aos="fade-up">
  <div class="swiper-wrapper">
    {% for book in books %}
    <div class="swiper-slide">
      <div class="card bg-base-100 shadow-md">
        <figure class="aspect-[2/3]">
          <img data-src="{{ book.cover }}" alt="{{ book.title }}" class="lazyload w-full h-full object-cover" />
        </figure>
        <div class="card-body p-4">
          <h3 class="card-title text-sm">{{ book.title }}</h3>
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
  BookReview.initSwiper('.swiper', {
    slidesPerView: 1,
    spaceBetween: 20,
    breakpoints: {
      640: { slidesPerView: 2 },
      768: { slidesPerView: 3 },
      1024: { slidesPerView: 4 }
    }
  });
</script>
```

### Stats với DaisyUI
```html
<div class="stats shadow w-full" data-aos="fade-up">
  <div class="stat">
    <div class="stat-figure text-primary">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-8 h-8 stroke-current">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25"></path>
      </svg>
    </div>
    <div class="stat-title">Tổng sách</div>
    <div class="stat-value text-primary">{{ total_books }}</div>
    <div class="stat-desc">21% tăng so với tháng trước</div>
  </div>
  
  <div class="stat">
    <div class="stat-figure text-secondary">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-8 h-8 stroke-current">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h69.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z"></path>
      </svg>
    </div>
    <div class="stat-title">Tổng reviews</div>
    <div class="stat-value text-secondary">{{ total_reviews }}</div>
    <div class="stat-desc">400 reviews mới trong tháng</div>
  </div>
  
  <div class="stat">
    <div class="stat-figure text-accent">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-8 h-8 stroke-current">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"></path>
      </svg>
    </div>
    <div class="stat-title">Thành viên</div>
    <div class="stat-value text-accent">{{ total_users }}</div>
    <div class="stat-desc">90 thành viên mới</div>
  </div>
</div>
```

### Dropdown Menu với DaisyUI
```html
<div class="dropdown dropdown-end">
  <div tabindex="0" role="button" class="btn btn-ghost btn-circle avatar">
    <div class="w-10 rounded-full">
      <img alt="User" src="{{ user.profile.avatar.url }}" />
    </div>
  </div>
  <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
    <li><a href="{% url 'user_profile' user.username %}"><i class="fas fa-user mr-2"></i>Hồ sơ</a></li>
    <li><a href="{% url 'user_shelves' %}"><i class="fas fa-book mr-2"></i>Kệ sách</a></li>
    <li><a href="{% url 'settings' %}"><i class="fas fa-cog mr-2"></i>Cài đặt</a></li>
    <li><hr class="my-1"></li>
    <li><a href="{% url 'logout' %}"><i class="fas fa-sign-out-alt mr-2"></i>Đăng xuất</a></li>
  </ul>
</div>
```

---

## 🔧 Utility Functions

### Heroicons
```javascript
// Render icon
const icon = Heroicons.render('heart', 'outline', { class: 'w-6 h-6 text-red-500' });

// Available icons: heart, book, user, search, bell, home, star, bookmark, chevronDown, menu, xMark
// Variants: 'outline' or 'solid'
```

### Swiper
```javascript
// Initialize Swiper
const swiper = BookReview.initSwiper('.swiper', {
  slidesPerView: 3,
  spaceBetween: 20,
  loop: true,
  autoplay: {
    delay: 3000,
  }
});
```

### AOS
```javascript
// Refresh AOS after dynamic content
AOS.refresh();

// Disable AOS
AOS.init({ disable: 'mobile' });
```

---

## 🎯 Best Practices

1. **Sử dụng DaisyUI components** cho UI nhất quán
2. **Kết hợp AOS** với các components để tăng UX
3. **Sử dụng Swiper** cho carousels và sliders
4. **Heroicons** cho icons đơn giản, Font Awesome cho icons phức tạp
5. **Lazy load images** trong Swiper slides
6. **Test responsive** trên mọi breakpoint

---

## 📚 Tài liệu tham khảo

- [DaisyUI Components](https://daisyui.com/components/)
- [Heroicons](https://heroicons.com/)
- [AOS Documentation](https://michalsnik.github.io/aos/)
- [Swiper.js Guide](https://swiperjs.com/get-started)
- [Font Awesome Icons](https://fontawesome.com/icons)

