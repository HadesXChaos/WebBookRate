(function(window, document) {
    'use strict';

    const form = document.getElementById('review-editor-form');
    if (!form) return;

    // --- 1. HÀM LẤY CSRF TOKEN (QUAN TRỌNG: Phải nằm trong file này) ---
    function getCookie(name) {
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
    }

    // --- KHỞI TẠO BIẾN ---
    const textarea = document.getElementById('review-body');
    const titleInput = document.getElementById('review-title');
    const ratingInput = document.getElementById('review-rating');
    const ratingDisplay = document.getElementById('rating-display');
    const autosaveIndicator = document.getElementById('autosave-indicator');
    const statusChip = document.getElementById('editor-status-chip');
    const previewTarget = document.querySelector(textarea.dataset.previewTarget);
    const hiddenBookField = form.querySelector('input[name="book_id"]');
    const manualBookInput = document.getElementById('book-id-input');
    const draftBanner = document.getElementById('draft-restore-banner');
    const restoreDraftBtn = document.getElementById('restore-draft-btn');
    const dismissDraftBtn = document.getElementById('dismiss-draft-btn');
    const cancelBtn = document.getElementById('editor-cancel-btn');
    const storageKey = form.dataset.storageKey;
    const existingReviewId = form.dataset.reviewId || null;

    const initialReviewElement = document.getElementById('initial-review-data');
    const initialReview = initialReviewElement ? JSON.parse(initialReviewElement.textContent) : null;
    const statusRadios = form.querySelectorAll('input[name="status"]');
    
    let submitIntent = 'draft';
    let autosaveTimer = null;

    // --- CÁC HÀM GIAO DIỆN ---
    function updateRatingDisplay(value) {
        if(ratingDisplay) ratingDisplay.textContent = parseFloat(value).toFixed(1);
    }

    function getSelectedStatus() {
        const checked = form.querySelector('input[name="status"]:checked');
        return checked ? checked.value : 'draft';
    }

    function getPayloadStatus() {
        return submitIntent === 'publish' ? 'public' : getSelectedStatus();
    }

    function updateStatusChip(state) {
        if (statusChip) statusChip.textContent = state;
    }

    function renderPreview(source) {
        if (!previewTarget) return;
        const text = (source || '').trim();
        if (!text.length) {
            previewTarget.innerHTML = '<p class="empty-placeholder">Nội dung preview sẽ xuất hiện tại đây.</p>';
            return;
        }
        if (window.marked) {
            const html = window.marked.parse(text, { gfm: true, breaks: true });
            previewTarget.innerHTML = window.DOMPurify ? window.DOMPurify.sanitize(html) : html;
        } else {
            previewTarget.textContent = text;
        }
    }

    // --- AUTOSAVE ---
    function persistDraft() {
        if (!storageKey) return;
        const payload = {
            title: titleInput.value,
            body_md: textarea.value,
            rating: ratingInput.value,
            status: getSelectedStatus(),
            book_id: hiddenBookField.value || (manualBookInput ? manualBookInput.value : ''),
            saved_at: new Date().toISOString(),
        };
        const isEmpty = !payload.title && !payload.body_md.trim();
        try {
            if (isEmpty) {
                window.localStorage.removeItem(storageKey);
                if(autosaveIndicator) autosaveIndicator.textContent = 'Chưa lưu';
            } else {
                window.localStorage.setItem(storageKey, JSON.stringify(payload));
                if(autosaveIndicator) autosaveIndicator.textContent = `Đã lưu nháp lúc ${new Date().toLocaleTimeString('vi-VN')}`;
            }
        } catch (err) {}
    }

    function scheduleAutosave() {
        if(autosaveIndicator) autosaveIndicator.textContent = 'Đang lưu...';
        clearTimeout(autosaveTimer);
        autosaveTimer = setTimeout(persistDraft, 800);
    }

    // --- SUBMIT FORM (ĐÃ SỬA LỖI TOKEN & JSON) ---
    async function submitForm(event) {
        event.preventDefault();

        const bookId = hiddenBookField.value || (manualBookInput ? manualBookInput.value : '');
        if (!bookId) {
            alert('Vui lòng chọn sách hoặc nhập ID sách trước khi gửi.');
            if (manualBookInput) manualBookInput.focus();
            return;
        }

        const payload = {
            book: Number(bookId),
            title: titleInput.value.trim(),
            body_md: textarea.value.trim(),
            rating: parseFloat(ratingInput.value),
            status: getPayloadStatus(),
        };

        if (!payload.title || !payload.body_md) {
            alert('Vui lòng nhập đầy đủ tiêu đề và nội dung.');
            return;
        }

        const url = existingReviewId ? `/api/reviews/${existingReviewId}/` : '/api/reviews/';
        const method = existingReviewId ? 'PUT' : 'POST';
        
        // Lấy CSRF Token bằng hàm nội bộ, không phụ thuộc bên ngoài
        const csrfToken = getCookie('csrftoken'); 

        const submitBtn = document.querySelector(`button[data-submit-intent="${submitIntent}"]`);
        const originalText = submitBtn ? submitBtn.textContent : '';
        if(submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Đang xử lý...';
        }

        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken, // <-- SỬ DỤNG TOKEN CHUẨN Ở ĐÂY
                },
                body: JSON.stringify(payload),
            });

            // Kiểm tra xem server có trả về HTML lỗi không
            const contentType = response.headers.get("content-type");
            if (!contentType || !contentType.includes("application/json")) {
                const text = await response.text();
                console.error("Server Error Response:", text);
                throw new Error("Lỗi Server (500). Vui lòng kiểm tra Terminal của Server để biết chi tiết.");
            }

            const data = await response.json();

            if (!response.ok) {
                console.error("API Error:", data);
                // Hiển thị lỗi chi tiết từ backend
                let msg = '';
                if(data.detail) msg = data.detail;
                else if(typeof data === 'object') {
                    for (const [key, value] of Object.entries(data)) {
                        msg += `${key}: ${value}\n`;
                    }
                }
                throw new Error(msg || 'Không thể lưu review.');
            }

            // Thành công
            if(storageKey) window.localStorage.removeItem(storageKey);
            
            if(autosaveIndicator) autosaveIndicator.textContent = 'Đã lưu thành công';
            updateStatusChip(payload.status === 'public' ? 'Đã xuất bản' : 'Nháp');
            
            alert('Lưu thành công!');

            if (data.id) {
                setTimeout(() => {
                    window.location.href = `/reviews/${data.id}/`;
                }, 500);
            }

        } catch (error) {
            console.error(error);
            alert(error.message || 'Có lỗi xảy ra.');
        } finally {
            if(submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }
        }
    }

    // --- EVENT LISTENERS ---
    document.querySelectorAll('[data-submit-intent]').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            submitIntent = button.dataset.submitIntent;
            const event = new Event('submit', { cancelable: true });
            form.dispatchEvent(event);
        });
    });

    form.addEventListener('submit', submitForm);

    textarea.addEventListener('input', () => { renderPreview(textarea.value); scheduleAutosave(); });
    titleInput.addEventListener('input', scheduleAutosave);
    ratingInput.addEventListener('input', event => { updateRatingDisplay(event.target.value); scheduleAutosave(); });
    statusRadios.forEach(radio => radio.addEventListener('change', scheduleAutosave));
    
    if (manualBookInput) {
        manualBookInput.addEventListener('input', event => {
            hiddenBookField.value = event.target.value;
            scheduleAutosave();
        });
    }

    if (cancelBtn) {
        cancelBtn.addEventListener('click', () => {
            if (document.referrer) window.history.back();
            else window.location.href = '/';
        });
    }

    if (window.marked) window.marked.setOptions({ gfm: true, breaks: true });
    updateRatingDisplay(ratingInput.value);

    // Populate Data
    function populateForm(data) {
        if (!data) return;
        if (data.title) titleInput.value = data.title;
        if (data.body_md) textarea.value = data.body_md;
        if (data.rating) { ratingInput.value = data.rating; updateRatingDisplay(data.rating); }
        if (data.book && data.book.id) { hiddenBookField.value = data.book.id; }
        renderPreview(textarea.value);
    }

    // Restore Draft Logic
    function showDraftBannerIfNeeded() {
        if(!storageKey || !draftBanner) return;
        try {
            const raw = window.localStorage.getItem(storageKey);
            if(!raw) return;
            const draft = JSON.parse(raw);
            
            if(draft.title || draft.body_md) {
                draftBanner.style.display = 'flex';
                draftBanner.hidden = false;
                
                if(restoreDraftBtn) {
                    restoreDraftBtn.addEventListener('click', (e) => {
                        e.preventDefault();
                        populateForm(draft);
                        draftBanner.style.display = 'none';
                    });
                }
                if(dismissDraftBtn) {
                    dismissDraftBtn.addEventListener('click', (e) => {
                        e.preventDefault();
                        window.localStorage.removeItem(storageKey);
                        draftBanner.style.display = 'none';
                    });
                }
            }
        } catch(e) {}
    }

    if (initialReview) {
        populateForm(initialReview);
        if(autosaveIndicator) autosaveIndicator.textContent = 'Đã tải dữ liệu';
    } else {
        renderPreview('');
        showDraftBannerIfNeeded();
    }

})(window, document);