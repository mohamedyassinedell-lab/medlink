// Main JavaScript file

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss flash messages
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transition = 'opacity 0.5s ease';
            setTimeout(() => msg.remove(), 500);
        }, 5000);
    });
    
    // Mobile menu toggle
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Search form auto-submit on filter change
    const filterForm = document.getElementById('filterForm');
    if (filterForm) {
        const selects = filterForm.querySelectorAll('select');
        selects.forEach(select => {
            select.addEventListener('change', () => {
                filterForm.submit();
            });
        });
    }
    
    // Image preview for uploads
    const imageInput = document.querySelector('input[type="file"][accept*="image"]');
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            const preview = document.getElementById('imagePreview');
            if (preview && this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.classList.remove('hidden');
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
});

// Share profile function
function shareProfile(url, title) {
    if (navigator.share) {
        navigator.share({
            title: title,
            url: url
        }).catch(() => {});
    } else {
        // Fallback: copy to clipboard
        if (navigator.clipboard) {
            navigator.clipboard.writeText(url).then(() => {
                alert('تم نسخ الرابط إلى الحافظة');
            }).catch(() => {});
        }
    }
}

// Report modal functions
function showReportModal() {
    const modal = document.getElementById('reportModal');
    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
}

function hideReportModal() {
    const modal = document.getElementById('reportModal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

// Close modal on outside click
document.addEventListener('click', function(e) {
    const modal = document.getElementById('reportModal');
    if (modal && !modal.classList.contains('hidden')) {
        if (e.target === modal) {
            hideReportModal();
        }
    }
});