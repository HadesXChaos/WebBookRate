(function(window, document) {
    'use strict';

    const form = document.getElementById('review-editor-form');
    if (!form) {
        return;
    }

    const utils = window.BookReview ? window.BookReview.utils : null;
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
    let lastSavedAt = null;

    function updateRatingDisplay(value) {
        ratingDisplay.textContent = parseFloat(value).toFixed(1);
    }

    function getSelectedStatus() {
        const checked = form.querySelector('input[name="status"]:checked');
        return checked ? checked.value : 'draft';
    }

    function getPayloadStatus() {
        return submitIntent === 'publish' ? 'public' : getSelectedStatus();
    }

    function updateStatusChip(state) {
        if (!statusChip) return;
        statusChip.textContent = state;
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

    function readDraft() {
        try {
            const raw = window.localStorage.getItem(storageKey);
            return raw ? JSON.parse(raw) : null;
        } catch (err) {
            console.warn('Cannot read draft:', err);
            return null;
        }
    }

    function persistDraft() {
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
                autosaveIndicator.textContent = 'Chưa lưu';
                return;
            }
            window.localStorage.setItem(storageKey, JSON.stringify(payload));
            lastSavedAt = new Date();
            autosaveIndicator.textContent = `Đã lưu nháp lúc ${lastSavedAt.toLocaleTimeString('vi-VN')}`;
        } catch (err) {
            console.warn('Cannot save draft:', err);
        }
    }

    function scheduleAutosave() {
        autosaveIndicator.textContent = 'Đang lưu...';
        clearTimeout(autosaveTimer);
        autosaveTimer = setTimeout(persistDraft, 800);
    }

    function populateForm(data) {
        if (!data) return;

        if (data.title) titleInput.value = data.title;
        if (typeof data.rating !== 'undefined' && data.rating !== null) {
            ratingInput.value = data.rating;
            updateRatingDisplay(data.rating);
        }
        if (data.body_md) textarea.value = data.body_md;
        if (data.book && data.book.id) {
            hiddenBookField.value = data.book.id;
            if (manualBookInput) manualBookInput.value = data.book.id;
        }
        if (data.status) {
            statusRadios.forEach(radio => {
                radio.checked = radio.value === data.status;
            });
            updateStatusChip(data.status === 'public' ? 'Đã xuất bản' : 'Nháp');
        }

        renderPreview(textarea.value);
    }

    function populateFromDraft(draft) {
        if (!draft) return;
        titleInput.value = draft.title || '';
        textarea.value = draft.body_md || '';
        if (draft.rating) {
            ratingInput.value = draft.rating;
            updateRatingDisplay(draft.rating);
        }
        if (draft.book_id) {
            hiddenBookField.value = draft.book_id;
            if (manualBookInput) manualBookInput.value = draft.book_id;
        }
        statusRadios.forEach(radio => {
            radio.checked = radio.value === (draft.status || 'draft');
        });
        renderPreview(textarea.value);
        persistDraft();
        if (utils) {
            utils.showAlert('Đã khôi phục bản nháp tự động.', 'info');
        }
    }

    function showDraftBannerIfNeeded() {
        const draft = readDraft();
        if (!draft) return;

        const isDifferentFromInitial =
            !initialReview ||
            draft.saved_at !== initialReview.saved_at ||
            draft.body_md !== initialReview.body_md;

        if (isDifferentFromInitial && draftBanner) {
            draftBanner.hidden = false;
            if (restoreDraftBtn) {
                restoreDraftBtn.addEventListener('click', () => {
                    populateFromDraft(draft);
                    draftBanner.hidden = true;
                });
            }
            if (dismissDraftBtn) {
                dismissDraftBtn.addEventListener('click', () => {
                    draftBanner.hidden = true;
                });
            }
        }
    }

    function resolveBookId() {
        return hiddenBookField.value || (manualBookInput ? manualBookInput.value : '') || '';
    }

    async function submitForm(event) {
        event.preventDefault();

        const bookId = resolveBookId();
        if (!bookId) {
            if (utils) {
                utils.showAlert('Vui lòng chọn sách trước khi gửi.', 'error');
            }
            (manualBookInput || hiddenBookField).focus();
            return;
        }

        const payload = {
            book: Number(bookId),
            title: titleInput.value.trim(),
            body_md: textarea.value.trim(),
            rating: parseFloat(ratingInput.value),
            status: getPayloadStatus(),
        };

        if (!payload.title || payload.body_md.length < 50) {
            if (utils) {
                utils.showAlert('Vui lòng nhập đầy đủ tiêu đề và nội dung.', 'error');
            }
            return;
        }

        const url = existingReviewId ? `/api/reviews/${existingReviewId}/` : '/api/reviews/';
        const method = existingReviewId ? 'PUT' : 'POST';

        try {
            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': utils ? utils.getCsrfToken() : '',
                },
                body: JSON.stringify(payload),
            });

            const data = await response.json();
            if (!response.ok) {
                const message = (data && (data.detail || data.error)) || 'Không thể lưu review. Vui lòng kiểm tra lại.';
                throw new Error(message);
            }

            window.localStorage.removeItem(storageKey);
            autosaveIndicator.textContent = 'Đã lưu thành công';
            updateStatusChip(payload.status === 'public' ? 'Đã xuất bản' : 'Nháp');
            if (utils) {
                utils.showAlert('Lưu review thành công!', 'success');
            }

            if (payload.status === 'public' && data.id) {
                setTimeout(() => {
                    window.location.href = `/reviews/${data.id}/`;
                }, 800);
            }
        } catch (error) {
            console.error(error);
            if (utils) {
                utils.showAlert(error.message || 'Có lỗi xảy ra.', 'error');
            }
        }
    }

    function triggerSubmit() {
        if (typeof form.requestSubmit === 'function') {
            form.requestSubmit();
        } else {
            const event = new Event('submit', { cancelable: true });
            form.dispatchEvent(event);
        }
    }

    document.querySelectorAll('[data-submit-intent]').forEach(button => {
        button.addEventListener('click', () => {
            submitIntent = button.dataset.submitIntent;
            triggerSubmit();
        });
    });

    form.addEventListener('submit', submitForm);

    textarea.addEventListener('input', () => {
        renderPreview(textarea.value);
        scheduleAutosave();
    });

    titleInput.addEventListener('input', scheduleAutosave);
    ratingInput.addEventListener('input', event => {
        updateRatingDisplay(event.target.value);
        scheduleAutosave();
    });
    statusRadios.forEach(radio => radio.addEventListener('change', scheduleAutosave));
    if (manualBookInput) {
        manualBookInput.addEventListener('input', event => {
            hiddenBookField.value = event.target.value;
            scheduleAutosave();
        });
    }

    if (cancelBtn) {
        cancelBtn.addEventListener('click', () => {
            if (document.referrer) {
                window.history.back();
            } else {
                window.location.href = '/';
            }
        });
    }

    if (window.marked) {
        window.marked.setOptions({
            gfm: true,
            breaks: true,
        });
    }

    updateRatingDisplay(ratingInput.value);

    if (initialReview) {
        populateForm(initialReview);
        autosaveIndicator.textContent = 'Đã tải dữ liệu';
    } else {
        renderPreview('');
    }

    showDraftBannerIfNeeded();
})(window, document);


