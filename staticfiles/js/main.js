/**
 * BookReview.vn - Main JavaScript
 */

(function () {
  "use strict";
  console.log("Main JS loaded.");

  // ===================================
  // Utility Functions
  // ===================================
  const utils = {
    /**
     * Get CSRF token from cookies
     */
    getCsrfToken: function () {
      const name = "csrftoken";
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },

    /**
     * Make API request
     */
    apiRequest: function (url, method = "GET", data = null) {
      const options = {
        method: method,
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": utils.getCsrfToken(),
        },
      };

      if (data) {
        options.body = JSON.stringify(data);
      }

      return fetch(url, options)
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .catch((error) => {
          console.error("API Request error:", error);
          throw error;
        });
    },

    /**
     * Debounce function
     */
    debounce: function (func, wait) {
      let timeout;
      return function executedFunction(...args) {
        const later = () => {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    },

    /**
     * Show notification/alert using SweetAlert2
     */
    showAlert: function (message, type = "info", options = {}) {
      // Map our types to SweetAlert2 types
      const swalType = {
        success: "success",
        error: "error",
        warning: "warning",
        info: "info",
      }[type] || "info";

      const defaultOptions = {
        title: message,
        icon: swalType,
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
      };

      // Use SweetAlert2 if available, otherwise fallback to old method
      if (typeof Swal !== "undefined") {
        Swal.fire({ ...defaultOptions, ...options });
      } else {
        // Fallback to old alert method
        const container =
          document.querySelector(".messages-container") ||
          document.createElement("div");

        if (!container.classList.contains("messages-container")) {
          container.className = "messages-container";
          document.body.appendChild(container);
        }

        const alert = document.createElement("div");
        alert.className = `alert alert-${type}`;
        alert.innerHTML = `
          <span>${message}</span>
          <button class="alert-close" aria-label="Close">&times;</button>
        `;

        container.appendChild(alert);

        setTimeout(() => {
          alert.remove();
        }, 5000);

        alert.querySelector(".alert-close").addEventListener("click", () => {
          alert.remove();
        });
      }
    },

    /**
     * Show confirmation dialog using SweetAlert2
     */
    showConfirm: function (message, title = "Xác nhận", options = {}) {
      const defaultOptions = {
        title: title,
        text: message,
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Xác nhận",
        cancelButtonText: "Hủy",
        confirmButtonColor: "#2563eb",
      };

      if (typeof Swal !== "undefined") {
        return Swal.fire({ ...defaultOptions, ...options });
      } else {
        return Promise.resolve({ isConfirmed: confirm(message) });
      }
    },

    /**
     * Render markdown to HTML (with sanitization)
     */
    renderMarkdown: function (markdown) {
      if (typeof marked === "undefined") {
        return markdown; // Fallback if marked.js not loaded
      }

      const html = marked.parse(markdown);
      
      // Sanitize with DOMPurify if available
      if (typeof DOMPurify !== "undefined") {
        return DOMPurify.sanitize(html);
      }
      
      return html;
    },

    /**
     * Initialize lazy loading for images
     */
    initLazyLoading: function () {
      if (typeof lazysizes !== "undefined") {
        // LazySizes will automatically handle images with data-src attribute
        // Just ensure images use class="lazyload" and data-src instead of src
      }
    },

    /**
     * Initialize Sortable for drag and drop
     */
    initSortable: function (element, options = {}) {
      if (typeof Sortable === "undefined") {
        console.warn("SortableJS not loaded");
        return null;
      }

      const defaultOptions = {
        animation: 150,
        ghostClass: "sortable-ghost",
        chosenClass: "sortable-chosen",
        dragClass: "sortable-drag",
      };

      return new Sortable(element, { ...defaultOptions, ...options });
    },

    /**
     * Initialize Swiper carousel
     */
    initSwiper: function (selector, options = {}) {
      if (typeof Swiper === "undefined") {
        console.warn("Swiper not loaded");
        return null;
      }

      const defaultOptions = {
        slidesPerView: 1,
        spaceBetween: 20,
        loop: false,
        autoplay: false,
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
        pagination: {
          el: ".swiper-pagination",
          clickable: true,
          dynamicBullets: true,
        },
        breakpoints: {
          640: {
            slidesPerView: 2,
            spaceBetween: 20,
          },
          768: {
            slidesPerView: 3,
            spaceBetween: 24,
          },
          1024: {
            slidesPerView: 4,
            spaceBetween: 30,
          },
        },
        // AOS integration
        on: {
          init: function() {
            if (typeof AOS !== 'undefined') {
              AOS.refresh();
            }
          }
        }
      };

      const element = typeof selector === "string" 
        ? document.querySelector(selector)
        : selector;

      if (!element) {
        console.warn("Swiper element not found:", selector);
        return null;
      }

      const swiper = new Swiper(element, { ...defaultOptions, ...options });
      
      // Refresh AOS after Swiper initialization
      if (typeof AOS !== 'undefined') {
        setTimeout(() => AOS.refresh(), 100);
      }
      
      return swiper;
    },
  };

  // ===================================
  // Mobile Menu
  // ===================================
  const initMobileMenu = function () {
    const menuToggle = document.getElementById("mobile-menu-btn");
    const mobileMenu = document.getElementById("mobile-menu");

    if (menuToggle && mobileMenu) {
      menuToggle.addEventListener("click", function () {
        const isExpanded = menuToggle.getAttribute("aria-expanded") === "true";
        menuToggle.setAttribute("aria-expanded", !isExpanded);
        mobileMenu.classList.toggle("hidden");
        
        // Update icon
        const icon = menuToggle.querySelector("i");
        if (icon) {
          if (isExpanded) {
            icon.classList.remove("fa-times");
            icon.classList.add("fa-bars");
          } else {
            icon.classList.remove("fa-bars");
            icon.classList.add("fa-times");
          }
        }
      });

      // Close menu when clicking outside
      document.addEventListener("click", function (event) {
        if (
          !menuToggle.contains(event.target) &&
          !mobileMenu.contains(event.target) &&
          !mobileMenu.classList.contains("hidden")
        ) {
          menuToggle.setAttribute("aria-expanded", "false");
          mobileMenu.classList.add("hidden");
          const icon = menuToggle.querySelector("i");
          if (icon) {
            icon.classList.remove("fa-times");
            icon.classList.add("fa-bars");
          }
        }
      });
    }
  };

  // ===================================
  // User Dropdown (Fallback if Alpine.js not available)
  // ===================================
  const initUserDropdown = function () {
    // Alpine.js handles dropdown in base.html, but we keep this as fallback
    const menuBtn = document.querySelector('[x-data]') ? null : document.getElementById("user-menu-btn");
    const dropdown = document.querySelector('[x-data]') ? null : document.getElementById("user-dropdown-menu");

    if (menuBtn && dropdown && typeof Alpine === "undefined") {
      menuBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        const isExpanded = menuBtn.getAttribute("aria-expanded") === "true";
        menuBtn.setAttribute("aria-expanded", !isExpanded);
        dropdown.classList.toggle("show");
      });

      // Close dropdown when clicking outside
      document.addEventListener("click", function () {
        menuBtn.setAttribute("aria-expanded", "false");
        dropdown.classList.remove("show");
      });

      dropdown.addEventListener("click", function (e) {
        e.stopPropagation();
      });
    }
  };

  // ===================================
  // Search Autocomplete
  // ===================================
  const initSearchAutocomplete = function () {
    const searchInput = document.getElementById("main-search");
    if (!searchInput) return;

    let autocompleteContainer = null;

    const showAutocomplete = function (results) {
      if (!autocompleteContainer) {
        autocompleteContainer = document.createElement("div");
        autocompleteContainer.className = "autocomplete-container";
        autocompleteContainer.style.cssText = `
                    position: absolute;
                    top: 100%;
                    left: 0;
                    right: 0;
                    background: white;
                    border: 1px solid #e2e8f0;
                    border-radius: 0.5rem;
                    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                    max-height: 400px;
                    overflow-y: auto;
                    z-index: 1000;
                    margin-top: 0.25rem;
                `;
        searchInput.parentElement.style.position = "relative";
        searchInput.parentElement.appendChild(autocompleteContainer);
      }

      autocompleteContainer.innerHTML = "";

      if (results.length === 0) {
        autocompleteContainer.innerHTML =
          '<div style="padding: 1rem; color: #64748b;">Không tìm thấy kết quả</div>';
        return;
      }

      results.forEach((item) => {
        const itemDiv = document.createElement("a");
        itemDiv.href = item.url;
        itemDiv.className = "autocomplete-item";
        itemDiv.style.cssText = `
                    display: block;
                    padding: 0.75rem 1rem;
                    color: #334155;
                    text-decoration: none;
                    transition: background-color 0.15s;
                `;
        itemDiv.innerHTML = `
                    <div style="font-weight: 500;">${item.title}</div>
                    ${
                      item.subtitle
                        ? `<div style="font-size: 0.875rem; color: #64748b;">${item.subtitle}</div>`
                        : ""
                    }
                `;
        itemDiv.addEventListener("mouseenter", () => {
          itemDiv.style.backgroundColor = "#f1f5f9";
        });
        itemDiv.addEventListener("mouseleave", () => {
          itemDiv.style.backgroundColor = "transparent";
        });
        autocompleteContainer.appendChild(itemDiv);
      });
    };

    const hideAutocomplete = function () {
      if (autocompleteContainer) {
        autocompleteContainer.remove();
        autocompleteContainer = null;
      }
    };

    const searchAutocomplete = utils.debounce(async function (query) {
      if (query.length < 2) {
        hideAutocomplete();
        return;
      }

      try {
        const response = await fetch(
          `/api/search/autocomplete/?q=${encodeURIComponent(query)}`
        );
        const data = await response.json();
        showAutocomplete(data.results || []);
      } catch (error) {
        console.error("Autocomplete error:", error);
      }
    }, 300);

    searchInput.addEventListener("input", function () {
      const query = this.value.trim();
      searchAutocomplete(query);
    });

    searchInput.addEventListener("blur", function () {
      // Delay to allow clicking on autocomplete items
      setTimeout(hideAutocomplete, 200);
    });

    searchInput.addEventListener("focus", function () {
      const query = this.value.trim();
      if (query.length >= 2) {
        searchAutocomplete(query);
      }
    });
  };

  // ===================================
  // Close Alerts
  // ===================================
  const initAlerts = function () {
    document.querySelectorAll(".alert-close").forEach((button) => {
      button.addEventListener("click", function () {
        this.closest(".alert").remove();
      });
    });
  };

  // ===================================
  // Rating Stars
  // ===================================
  const renderStars = function (rating, container) {
    if (!container) return;

    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

    container.innerHTML = "";

    for (let i = 0; i < fullStars; i++) {
      container.innerHTML += "<span>★</span>";
    }
    if (hasHalfStar) {
      container.innerHTML += '<span style="opacity: 0.5">★</span>';
    }
    for (let i = 0; i < emptyStars; i++) {
      container.innerHTML += '<span style="opacity: 0.3">☆</span>';
    }
  };

  // ===================================
  // Like/Unlike Actions
  // ===================================
  const initLikeButtons = function () {
    document.querySelectorAll("[data-like-url]").forEach((button) => {
      button.addEventListener("click", async function (e) {
        e.preventDefault();
        const url = this.dataset.likeUrl;
        const countElement = this.querySelector("[data-like-count]");
        const isLiked = this.classList.contains("liked");

        try {
          const method = isLiked ? "DELETE" : "POST";
          await utils.apiRequest(url, method);

          this.classList.toggle("liked");
          if (countElement) {
            const currentCount = parseInt(countElement.textContent) || 0;
            countElement.textContent = isLiked
              ? currentCount - 1
              : currentCount + 1;
          }
        } catch (error) {
          utils.showAlert("Có lỗi xảy ra. Vui lòng thử lại.", "error");
          console.error("Like action error:", error);
        }
      });
    });
  };

  // sửa đổi method cập nhật hồ sơ người dùng từ POST thành PUT
  const csrftoken = utils.getCsrfToken();

  const form = document.getElementById("profile-form");
  if (form) {
    const redirectUrl = form.dataset.redirectUrl;
    form.addEventListener("submit", async function (e) {
      e.preventDefault(); // chặn submit mặc định (POST)

      const formData = new FormData(form);
      const avatarInput = form.querySelector('input[name="avatar"]');
      if (avatarInput && avatarInput.files.length === 0) {
        formData.delete("avatar"); // không gửi field avatar -> giữ hình cũ
      }

      const response = await fetch("/api/auth/profile/", {
        method: "PUT",
        headers: {
          "X-CSRFToken": csrftoken,
        },
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        utils.showAlert("Cập nhật hồ sơ thành công!", "success");
        setTimeout(() => {
          window.location.href = redirectUrl;
        }, 1500);
      } else {
        console.log(data);
        const errorMsg = data.detail || data.message || "Có lỗi khi cập nhật hồ sơ!";
        utils.showAlert(errorMsg, "error");
      }
    });
  }

  // ẩn/hiện mật khẩu

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".toggle-password").forEach((btn) => {
      btn.addEventListener("click", function () {
        const targetId = this.dataset.target;
        const input = document.getElementById(targetId);
        if (!input) return;

        const isHidden = input.type === "password";

        // Đổi kiểu input
        input.type = isHidden ? "text" : "password";

        // Thêm / bỏ class để CSS tự đổi chữ Hiện / Ẩn
        this.classList.toggle("is-visible", isHidden);
      });
    });
  });

  // doi mật khẩu
  document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("change-password-form");
    if (!form) return;

    const csrftoken = utils.getCsrfToken();

    form.addEventListener("submit", async function (e) {
      e.preventDefault(); // ❗ không cho form redirect sang API

      const oldPassword = document.getElementById("old_password").value;
      const newPassword1 = document.getElementById("new_password1").value;
      const newPassword2 = document.getElementById("new_password2").value;

      const payload = {
        old_password: oldPassword,
        new_password: newPassword1,
        new_password_confirm: newPassword2,
      };

      try {
        const response = await fetch("/api/auth/password-change/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify(payload),
        });

        const data = await response.json();
        if (response.ok) {
          utils.showAlert("Đổi mật khẩu thành công! Vui lòng đăng nhập lại.", "success");
          setTimeout(() => {
            window.location.href = "/login/";
          }, 2000);
        } else {
          console.log("Change password error:", data);
          const errorMsg = data.detail || data.message || "Đổi mật khẩu thất bại";
          utils.showAlert(errorMsg, "error");
        }
      } catch (err) {
        console.error(err);
        utils.showAlert("Có lỗi kết nối server!", "error");
      }
    });
  });

  // ===================================
  // Initialize everything
  // ===================================
  document.addEventListener("DOMContentLoaded", function () {
    initMobileMenu();
    initUserDropdown();
    initSearchAutocomplete();
    initAlerts();
    initLikeButtons();
    initLazyLoading();

    // Render stars for all rating elements
    document.querySelectorAll("[data-rating]").forEach((element) => {
      const rating = parseFloat(element.dataset.rating);
      renderStars(rating, element);
    });

    // Initialize AOS animations (if not already initialized in base.html)
    if (typeof AOS !== "undefined" && AOS.init) {
      AOS.init({
        duration: 800,
        easing: "ease-in-out",
        once: true,
        offset: 100,
      });
    }
  });

  // ===================================
  // Initialize Lazy Loading
  // ===================================
  const initLazyLoading = function () {
    utils.initLazyLoading();
  };

  // ===================================
  // Export utils for use in other scripts
  // ===================================
  window.BookReview = {
    utils: utils,
    renderStars: renderStars,
    initSortable: utils.initSortable,
    initSwiper: utils.initSwiper,
    renderMarkdown: utils.renderMarkdown,
    Swal: typeof Swal !== "undefined" ? Swal : null,
    Chart: typeof Chart !== "undefined" ? Chart : null,
    Swiper: typeof Swiper !== "undefined" ? Swiper : null,
  };
})();
