// Common utility functions
function showLoading(element) {
    if (element) {
        const loadingSpinner = document.createElement('div');
        loadingSpinner.className = 'loading me-2';
        element.prepend(loadingSpinner);
        element.disabled = true;
    }
}

function hideLoading(element) {
    if (element) {
        const loadingSpinner = element.querySelector('.loading');
        if (loadingSpinner) {
            loadingSpinner.remove();
        }
        element.disabled = false;
    }
}

// Add loading state to all forms
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');
            showLoading(submitButton);
        });
    });
});

// Handle file size validation
function validateFileSize(input, maxSize = 25 * 1024 * 1024) { // 25MB default
    if (input.files && input.files[0]) {
        if (input.files[0].size > maxSize) {
            alert('File is too large. Maximum size is 25MB. Please use a URL for larger files.');
            input.value = '';
            return false;
        }
    }
    return true;
}

// Format time for display
function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    const ms = Math.floor((seconds % 1) * 1000);
    
    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')},${String(ms).padStart(3, '0')}`;
}

// Handle errors
function handleError(error, errorElement) {
    if (errorElement) {
        errorElement.textContent = error.message || 'An unexpected error occurred. Please try again.';
        errorElement.classList.remove('d-none');
        
        // Auto-hide error after 5 seconds
        setTimeout(() => {
            errorElement.classList.add('d-none');
        }, 5000);
    }
}

// Copy to clipboard with feedback
function copyToClipboard(text, successMessage = 'Copied to clipboard!') {
    navigator.clipboard.writeText(text).then(function() {
        // Create and show toast notification
        const toast = document.createElement('div');
        toast.className = 'toast-notification';
        toast.textContent = successMessage;
        document.body.appendChild(toast);
        
        // Remove toast after animation
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }).catch(function(err) {
        console.error('Failed to copy text: ', err);
        alert('Failed to copy to clipboard');
    });
}

// Add toast notification styles
const style = document.createElement('style');
style.textContent = `
    .toast-notification {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background-color: #333;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        z-index: 1000;
        animation: fadeInOut 3s ease-in-out;
    }
    
    @keyframes fadeInOut {
        0% { opacity: 0; transform: translate(-50%, 20px); }
        10% { opacity: 1; transform: translate(-50%, 0); }
        90% { opacity: 1; transform: translate(-50%, 0); }
        100% { opacity: 0; transform: translate(-50%, -20px); }
    }
`;
document.head.appendChild(style);

// Handle navigation active state
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// Prevent form resubmission on page refresh
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}

// Add smooth scrolling to all links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
