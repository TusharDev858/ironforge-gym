/* IronForge Gym - Main JavaScript */

document.addEventListener('DOMContentLoaded', function () {

    // ==========================================
    // THEME TOGGLE
    // ==========================================
    const html = document.documentElement;
    const themeToggle = document.getElementById('themeToggle');
    const themeToggleMobile = document.getElementById('themeToggleMobile');
    const themeIcon = document.getElementById('themeIcon');
    const themeIconMobile = document.getElementById('themeIconMobile');

    const savedTheme = localStorage.getItem('ironforge-theme') || 'dark';
    html.setAttribute('data-theme', savedTheme);
    updateThemeIcons(savedTheme);

    function updateThemeIcons(theme) {
        const iconClass = theme === 'dark' ? 'bi-sun-fill' : 'bi-moon-fill';
        if (themeIcon) themeIcon.className = 'bi ' + iconClass;
        if (themeIconMobile) themeIconMobile.className = 'bi ' + iconClass;
    }

    function toggleTheme() {
        const current = html.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', next);
        localStorage.setItem('ironforge-theme', next);
        updateThemeIcons(next);
    }

    if (themeToggle) themeToggle.addEventListener('click', toggleTheme);
    if (themeToggleMobile) themeToggleMobile.addEventListener('click', toggleTheme);

    // ==========================================
    // NAVBAR SCROLL
    // ==========================================
    const nav = document.getElementById('mainNav');
    function handleScroll() {
        if (nav) {
            nav.classList.toggle('scrolled', window.scrollY > 50);
        }
    }
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();

    // ==========================================
    // SCROLL REVEAL
    // ==========================================
    const revealElements = document.querySelectorAll('.reveal');
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    revealElements.forEach(el => revealObserver.observe(el));

    // ==========================================
    // AUTO-DISMISS MESSAGES
    // ==========================================
    const autoToasts = document.querySelectorAll('[data-auto-dismiss]');
    autoToasts.forEach(toast => {
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            toast.style.transition = 'all 0.4s ease';
            setTimeout(() => toast.remove(), 400);
        }, 5000);
    });

    // ==========================================
    // SCHEDULE TABS
    // Only activate on pages that have actual schedule panels,
    // NOT on gallery or other pages that reuse the .schedule-tab class for filter links.
    // ==========================================
    const schedulePanels = document.querySelectorAll('.schedule-panel');

    if (schedulePanels.length > 0) {
        // Only select tabs that are <button> elements (not <a> links used in gallery filters)
        const scheduleTabs = document.querySelectorAll('button.schedule-tab');

        scheduleTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const day = tab.dataset.day;

                scheduleTabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');

                schedulePanels.forEach(panel => {
                    panel.style.display = panel.dataset.day === day ? 'block' : 'none';
                    if (panel.dataset.day === day) {
                        panel.style.animation = 'fadeIn 0.3s ease';
                    }
                });
            });
        });

        // Activate first tab by default (safe — only runs when panels exist)
        if (scheduleTabs.length > 0) {
            scheduleTabs[0].click();
        }
    }

    // ==========================================
    // COUNTER ANIMATION (hero stats)
    // ==========================================
    const counters = document.querySelectorAll('[data-count]');
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.dataset.count);
                const duration = 2000;
                const step = target / (duration / 16);
                let current = 0;
                const timer = setInterval(() => {
                    current = Math.min(current + step, target);
                    entry.target.textContent = Math.floor(current).toLocaleString() + (entry.target.dataset.suffix || '');
                    if (current >= target) clearInterval(timer);
                }, 16);
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(c => counterObserver.observe(c));

    // ==========================================
    // GALLERY LIGHTBOX
    // ==========================================
    const galleryItems = document.querySelectorAll('.gallery-item');
    let lightbox = null;

    if (galleryItems.length > 0) {
        lightbox = document.createElement('div');
        lightbox.className = 'lightbox';
        lightbox.innerHTML = `
            <div class="lightbox-overlay"></div>
            <div class="lightbox-content">
                <img class="lightbox-img" src="" alt="">
                <button class="lightbox-close"><i class="bi bi-x-lg"></i></button>
                <button class="lightbox-prev"><i class="bi bi-chevron-left"></i></button>
                <button class="lightbox-next"><i class="bi bi-chevron-right"></i></button>
            </div>
        `;
        document.body.appendChild(lightbox);

        const lightboxImg = lightbox.querySelector('.lightbox-img');
        let currentIndex = 0;
        const images = Array.from(galleryItems).map(item => item.querySelector('img')?.src).filter(Boolean);

        function openLightbox(index) {
            if (!images[index]) return;
            currentIndex = index;
            lightboxImg.src = images[index];
            lightbox.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }

        function closeLightbox() {
            lightbox.style.display = 'none';
            document.body.style.overflow = '';
        }

        galleryItems.forEach((item, i) => {
            item.addEventListener('click', () => openLightbox(i));
        });

        lightbox.querySelector('.lightbox-close').addEventListener('click', closeLightbox);
        lightbox.querySelector('.lightbox-overlay').addEventListener('click', closeLightbox);
        lightbox.querySelector('.lightbox-prev').addEventListener('click', () => {
            currentIndex = (currentIndex - 1 + images.length) % images.length;
            lightboxImg.src = images[currentIndex];
        });
        lightbox.querySelector('.lightbox-next').addEventListener('click', () => {
            currentIndex = (currentIndex + 1) % images.length;
            lightboxImg.src = images[currentIndex];
        });

        document.addEventListener('keydown', (e) => {
            if (lightbox.style.display !== 'none') {
                if (e.key === 'Escape') closeLightbox();
                if (e.key === 'ArrowLeft') lightbox.querySelector('.lightbox-prev').click();
                if (e.key === 'ArrowRight') lightbox.querySelector('.lightbox-next').click();
            }
        });
    }

    // ==========================================
    // FILTER FORM AUTO-SUBMIT
    // ==========================================
    const filterSelects = document.querySelectorAll('.filter-select[data-auto-submit]');
    filterSelects.forEach(select => {
        select.addEventListener('change', () => {
            select.closest('form').submit();
        });
    });

    // ==========================================
    // BOOKING DATE VALIDATION
    // ==========================================
    const bookingDateInput = document.getElementById('bookingDate');
    if (bookingDateInput) {
        const today = new Date().toISOString().split('T')[0];
        bookingDateInput.min = today;
    }
});

// Lightbox CSS (injected dynamically)
const lightboxStyles = document.createElement('style');
lightboxStyles.textContent = `
.lightbox {
    display: none;
    position: fixed;
    inset: 0;
    z-index: 10000;
    align-items: center;
    justify-content: center;
}
.lightbox-overlay {
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,0.9);
}
.lightbox-content {
    position: relative;
    max-width: 90vw;
    max-height: 90vh;
    z-index: 1;
}
.lightbox-img {
    max-width: 90vw;
    max-height: 85vh;
    border-radius: 8px;
    display: block;
}
.lightbox-close, .lightbox-prev, .lightbox-next {
    position: absolute;
    background: rgba(0,0,0,0.6);
    border: 1px solid rgba(255,255,255,0.2);
    color: white;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background 0.2s;
    font-size: 1rem;
}
.lightbox-close:hover, .lightbox-prev:hover, .lightbox-next:hover { background: rgba(232,66,10,0.8); }
.lightbox-close { top: -1rem; right: -1rem; }
.lightbox-prev { left: -1.5rem; top: 50%; transform: translateY(-50%); }
.lightbox-next { right: -1.5rem; top: 50%; transform: translateY(-50%); }
`;
document.head.appendChild(lightboxStyles);
