/**
 * BookReview.vn - Main JavaScript
 */

(function() {
    'use strict';

    // ===================================
    // Utility Functions
    // ===================================
    const utils = {
        /**
         * Get CSRF token from cookies
         */
        getCsrfToken: function() {
            const name = 'csrftoken';
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
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
        apiRequest: function(url, method = 'GET', data = null) {
            const options = {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': utils.getCsrfToken(),
                },
            };

            if (data) {
                options.body = JSON.stringify(data);
            }

            return fetch(url, options)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .catch(error => {
                    console.error('API Request error:', error);
                    throw error;
                });
        },

        /**
         * Debounce function
         */
        debounce: function(func, wait) {
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
         * Show notification/alert
         */
        showAlert: function(message, type = 'info') {
            const container = document.querySelector('.messages-container') || 
                            document.createElement('div');
            
            if (!container.classList.contains('messages-container')) {
                container.className = 'messages-container';
                document.body.appendChild(container);
            }

            const alert = document.createElement('div');
            alert.className = `alert alert-${type}`;
            alert.innerHTML = `
                <span>${message}</span>
                <button class="alert-close" aria-label="Close">&times;</button>
            `;
            
            container.appendChild(alert);

            // Auto remove after 5 seconds
            setTimeout(() => {
                alert.remove();
            }, 5000);

            // Close button
            alert.querySelector('.alert-close').addEventListener('click', () => {
                alert.remove();
            });
        }
    };

    // ===================================
    // Mobile Menu
    // ===================================
    const initMobileMenu = function() {
        const menuToggle = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');

        if (menuToggle && mobileMenu) {
            menuToggle.addEventListener('click', function() {
                const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
                menuToggle.setAttribute('aria-expanded', !isExpanded);
                mobileMenu.classList.toggle('active');
            });

            // Close menu when clicking outside
            document.addEventListener('click', function(event) {
                if (!menuToggle.contains(event.target) && !mobileMenu.contains(event.target)) {
                    menuToggle.setAttribute('aria-expanded', 'false');
                    mobileMenu.classList.remove('active');
                }
            });
        }
    };

    // ===================================
    // User Dropdown
    // ===================================
    const initUserDropdown = function() {
        const menuBtn = document.getElementById('user-menu-btn');
        const dropdown = document.getElementById('user-dropdown-menu');

        if (menuBtn && dropdown) {
            menuBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                const isExpanded = menuBtn.getAttribute('aria-expanded') === 'true';
                menuBtn.setAttribute('aria-expanded', !isExpanded);
                dropdown.classList.toggle('show');
            });

            // Close dropdown when clicking outside
            document.addEventListener('click', function() {
                menuBtn.setAttribute('aria-expanded', 'false');
                dropdown.classList.remove('show');
            });

            dropdown.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        }
    };

    // ===================================
    // Search Autocomplete
    // ===================================
    const initSearchAutocomplete = function() {
        const searchInput = document.getElementById('main-search');
        if (!searchInput) return;

        let autocompleteContainer = null;

        const showAutocomplete = function(results) {
            if (!autocompleteContainer) {
                autocompleteContainer = document.createElement('div');
                autocompleteContainer.className = 'autocomplete-container';
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
                searchInput.parentElement.style.position = 'relative';
                searchInput.parentElement.appendChild(autocompleteContainer);
            }

            autocompleteContainer.innerHTML = '';

            if (results.length === 0) {
                autocompleteContainer.innerHTML = '<div style="padding: 1rem; color: #64748b;">Không tìm thấy kết quả</div>';
                return;
            }

            results.forEach(item => {
                const itemDiv = document.createElement('a');
                itemDiv.href = item.url;
                itemDiv.className = 'autocomplete-item';
                itemDiv.style.cssText = `
                    display: block;
                    padding: 0.75rem 1rem;
                    color: #334155;
                    text-decoration: none;
                    transition: background-color 0.15s;
                `;
                itemDiv.innerHTML = `
                    <div style="font-weight: 500;">${item.title}</div>
                    ${item.subtitle ? `<div style="font-size: 0.875rem; color: #64748b;">${item.subtitle}</div>` : ''}
                `;
                itemDiv.addEventListener('mouseenter', () => {
                    itemDiv.style.backgroundColor = '#f1f5f9';
                });
                itemDiv.addEventListener('mouseleave', () => {
                    itemDiv.style.backgroundColor = 'transparent';
                });
                autocompleteContainer.appendChild(itemDiv);
            });
        };

        const hideAutocomplete = function() {
            if (autocompleteContainer) {
                autocompleteContainer.remove();
                autocompleteContainer = null;
            }
        };

        const searchAutocomplete = utils.debounce(async function(query) {
            if (query.length < 2) {
                hideAutocomplete();
                return;
            }

            try {
                const response = await fetch(`/api/search/autocomplete/?q=${encodeURIComponent(query)}`);
                const data = await response.json();
                showAutocomplete(data.results || []);
            } catch (error) {
                console.error('Autocomplete error:', error);
            }
        }, 300);

        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            searchAutocomplete(query);
        });

        searchInput.addEventListener('blur', function() {
            // Delay to allow clicking on autocomplete items
            setTimeout(hideAutocomplete, 200);
        });

        searchInput.addEventListener('focus', function() {
            const query = this.value.trim();
            if (query.length >= 2) {
                searchAutocomplete(query);
            }
        });
    };

    // ===================================
    // Close Alerts
    // ===================================
    const initAlerts = function() {
        document.querySelectorAll('.alert-close').forEach(button => {
            button.addEventListener('click', function() {
                this.closest('.alert').remove();
            });
        });
    };

    // ===================================
    // Rating Stars
    // ===================================
    const renderStars = function(rating, container) {
        if (!container) return;
        
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

        container.innerHTML = '';

        for (let i = 0; i < fullStars; i++) {
            container.innerHTML += '<span>★</span>';
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
    const initLikeButtons = function() {
        document.querySelectorAll('[data-like-url]').forEach(button => {
            button.addEventListener('click', async function(e) {
                e.preventDefault();
                const url = this.dataset.likeUrl;
                const countElement = this.querySelector('[data-like-count]');
                const isLiked = this.classList.contains('liked');

                try {
                    const method = isLiked ? 'DELETE' : 'POST';
                    await utils.apiRequest(url, method);
                    
                    this.classList.toggle('liked');
                    if (countElement) {
                        const currentCount = parseInt(countElement.textContent) || 0;
                        countElement.textContent = isLiked ? currentCount - 1 : currentCount + 1;
                    }
                } catch (error) {
                    utils.showAlert('Có lỗi xảy ra. Vui lòng thử lại.', 'error');
                }
            });
        });
    };

    // ===================================
    // Initialize everything
    // ===================================
    document.addEventListener('DOMContentLoaded', function() {
        initMobileMenu();
        initUserDropdown();
        initSearchAutocomplete();
        initAlerts();
        initLikeButtons();

        // Render stars for all rating elements
        document.querySelectorAll('[data-rating]').forEach(element => {
            const rating = parseFloat(element.dataset.rating);
            renderStars(rating, element);
        });
    });

    // Export utils for use in other scripts
    window.BookReview = {
        utils: utils,
        renderStars: renderStars
    };

})();

