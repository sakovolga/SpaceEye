//// static/main/js/favorites.js

class FavoritesManager {
    constructor() {
        this.setupEventListeners();
        console.log('FavoritesManager initialized');
    }

    setupEventListeners() {
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('favorite-btn') || e.target.closest('.favorite-btn')) {
                e.preventDefault();
                e.stopPropagation();
                const btn = e.target.classList.contains('favorite-btn') ? e.target : e.target.closest('.favorite-btn');
                console.log('Favorite button clicked:', btn);
                this.toggleFavorite(btn);
            }
        });
    }

    async toggleFavorite(button) {
        const action = button.dataset.action;
        const type = button.dataset.type;
        const imageUrl = button.dataset.imageUrl;
        const photoData = button.dataset.photoData ? JSON.parse(button.dataset.photoData) : null;

        console.log('Toggle favorite:', { action, type, imageUrl });

        button.disabled = true;
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

        try {
            let url, data;

            if (action === 'add') {
                url = '/favorites/add/';
                if (type === 'apod') {
                    data = {
                        type: 'apod',
                        data: window.currentApodData || this.getApodDataFromPage()
                    };
                } else if (type === 'mars_rover') {
                    if (!photoData) {
                        throw new Error('No photo data available');
                    }
                    data = {
                        type: 'mars_rover',
                        data: photoData
                    };
                }
            } else {
                url = '/favorites/remove/';
                data = {
                    type: type,
                    image_url: imageUrl
                };
            }

            console.log('Sending request to:', url, 'with data:', data);

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            console.log('Response:', result);

            if (result.success) {
                if (result.action === 'added') {
                    this.updateButtonToRemove(button, imageUrl);
                    this.showToast('Added to favorites!', 'success');

                    // Update modal button if exists
                    if (type === 'mars_rover' && window.updateModalFavoriteButton) {
                        window.updateModalFavoriteButton('remove', imageUrl);
                    }
                } else if (result.action === 'removed') {
                    this.updateButtonToAdd(button, type);
                    this.showToast('Removed from favorites!', 'info');

                    // Update modal button if exists
                    if (type === 'mars_rover' && window.updateModalFavoriteButton) {
                        window.updateModalFavoriteButton('add', imageUrl);
                    }
                }
            } else {
                this.showToast(result.error || 'An error occurred', 'error');
                button.innerHTML = originalText;
            }
        } catch (error) {
            console.error('Error:', error);
            this.showToast('An error occurred while performing the operation', 'error');
            button.innerHTML = originalText;
        } finally {
            button.disabled = false;
        }
    }

    updateButtonToRemove(button, imageUrl) {
        button.dataset.action = 'remove';
        button.dataset.imageUrl = imageUrl;
        button.classList.remove('btn-outline-warning');
        button.classList.add('btn-warning');

        if (button.innerHTML.includes('Add to Favorites')) {
            button.innerHTML = '<i class="fas fa-star"></i> In Favorites';
        } else {
            button.innerHTML = '<i class="fas fa-star"></i>';
        }

        button.title = 'Remove from favorites';
    }

    updateButtonToAdd(button, type) {
        button.dataset.action = 'add';
        button.removeAttribute('data-image-url');
        button.classList.remove('btn-warning');
        button.classList.add('btn-outline-warning');

        if (button.innerHTML.includes('In Favorites')) {
            button.innerHTML = '<i class="far fa-star"></i> Add to Favorites';
        } else {
            button.innerHTML = '<i class="far fa-star"></i>';
        }

        button.title = 'Add to favorites';
    }

    getApodDataFromPage() {
        return {
            title: document.querySelector('.nasa-title')?.textContent || document.querySelector('h2')?.textContent || '',
            explanation: document.querySelector('.nasa-explanation')?.textContent || document.querySelector('.card-text')?.textContent || '',
            url: document.querySelector('.nasa-image')?.src || document.querySelector('img')?.src || '',
            date: document.querySelector('input[name="date"]')?.value || new Date().toISOString().split('T')[0],
            media_type: 'image'
        };
    }

    getCsrfToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }

    showToast(message, type = 'info') {
        const toastId = 'toast-' + Date.now();
        const toastClass = type === 'success' ? 'bg-success' :
                          type === 'error' ? 'bg-danger' : 'bg-info';

        const toastHtml = `
            <div class="toast align-items-center text-white ${toastClass} border-0"
                 id="${toastId}" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">${message}</div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto"
                            data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;

        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
            toastContainer.style.zIndex = '9999';
            document.body.appendChild(toastContainer);
        }

        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, { autohide: true, delay: 3000 });
        toast.show();

        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    }
}

// Initialize favorites manager
document.addEventListener('DOMContentLoaded', () => {
    window.favoritesManager = new FavoritesManager();
});