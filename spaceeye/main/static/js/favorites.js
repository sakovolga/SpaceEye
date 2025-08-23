// static/main/js/favorites.js

class FavoritesManager {
    constructor() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Handler for add/remove from favorites buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('favorite-btn') || e.target.closest('.favorite-btn')) {
                e.preventDefault();
                const btn = e.target.classList.contains('favorite-btn') ? e.target : e.target.closest('.favorite-btn');
                this.toggleFavorite(btn);
            }
        });
    }

    async toggleFavorite(button) {
        const action = button.dataset.action;
        const type = button.dataset.type;
        const imageUrl = button.dataset.imageUrl;

        // Disable button during request
        button.disabled = true;
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

        try {
            let url, data;

            if (action === 'add') {
                url = '/favorites/add/';
                // Get data from data-attributes or global variables
                if (type === 'apod') {
                    data = {
                        type: 'apod',
                        data: window.currentApodData || this.getApodDataFromPage()
                    };
                } else if (type === 'mars_rover') {
                    data = {
                        type: 'mars_rover',
                        data: JSON.parse(button.dataset.photoData)
                    };
                }
            } else {
                url = '/favorites/remove/';
                data = {
                    type: type,
                    image_url: imageUrl
                };
            }

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                if (result.action === 'added') {
                    this.updateButtonToRemove(button, imageUrl);
                    this.showToast('Added to favorites!', 'success');
                } else if (result.action === 'removed') {
                    this.updateButtonToAdd(button, type);
                    this.showToast('Removed from favorites!', 'info');
                }
            } else {
                this.showToast(result.error || 'An error occurred', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showToast('An error occurred while performing the operation', 'error');
        } finally {
            // Restore button
            button.disabled = false;
            if (!button.dataset.updated) {
                button.innerHTML = originalText;
            }
        }
    }

    updateButtonToRemove(button, imageUrl) {
        button.dataset.action = 'remove';
        button.dataset.imageUrl = imageUrl;
        button.classList.remove('btn-outline-warning');
        button.classList.add('btn-warning');
        button.innerHTML = '<i class="fas fa-star"></i>';
        button.title = 'Remove from favorites';
        button.dataset.updated = 'true';
    }

    updateButtonToAdd(button, type) {
        button.dataset.action = 'add';
        button.removeAttribute('data-image-url');
        button.classList.remove('btn-warning');
        button.classList.add('btn-outline-warning');
        button.innerHTML = '<i class="far fa-star"></i>';
        button.title = 'Add to favorites';
        button.dataset.updated = 'true';
    }

    getApodDataFromPage() {
        // Extract APOD data from DOM
        const title = document.querySelector('h1')?.textContent || '';
        const explanation = document.querySelector('.nasa-explanation')?.textContent || '';
        const imageUrl = document.querySelector('.nasa-image')?.src || '';
        const date = document.querySelector('input[name="date"]')?.value || '';

        return {
            title: title,
            explanation: explanation,
            url: imageUrl,
            date: date,
            media_type: 'image'
        };
    }

    getCsrfToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }

    showToast(message, type = 'info') {
        // Create toast notification
        const toastId = 'toast-' + Date.now();
        const toastClass = type === 'success' ? 'bg-success' :
                          type === 'error' ? 'bg-danger' : 'bg-info';

        const toastHtml = `
            <div class="toast align-items-center text-white ${toastClass} border-0"
                 id="${toastId}" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto"
                            data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;

        // Add toast to container
        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
            toastContainer.style.zIndex = '9999';
            document.body.appendChild(toastContainer);
        }

        toastContainer.insertAdjacentHTML('beforeend', toastHtml);

        // Show toast
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: 3000
        });
        toast.show();

        // Remove toast from DOM after hiding
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    }
}

// Initialize favorites manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FavoritesManager();
});

// Global function for quick adding to favorites
window.addToFavorites = function(type, data) {
    const manager = new FavoritesManager();
    const fakeButton = {
        dataset: {
            action: 'add',
            type: type,
            photoData: typeof data === 'object' ? JSON.stringify(data) : data
        },
        disabled: false,
        innerHTML: '',
        classList: {
            contains: () => false,
            remove: () => {},
            add: () => {}
        },
        title: ''
    };

    if (type === 'apod') {
        window.currentApodData = data;
    }

    manager.toggleFavorite(fakeButton);
};