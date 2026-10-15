/**
 * AccessEvent — вспомогательный JavaScript.
 * Все уведомления ВИЗУАЛЬНЫЕ (никаких звуковых сигналов).
 */

// ===== Тема (светлая/тёмная) =====
function initTheme() {
    const saved = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = saved || (prefersDark ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', theme);
}

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
}

// ===== Визуальные уведомления =====
function showNotification(message, type = 'info') {
    const container = document.getElementById('notifications');
    if (!container) return;

    const notice = document.createElement('div');
    notice.className = 'notification notification-' + type;
    notice.setAttribute('role', 'status');
    notice.setAttribute('aria-live', 'polite');
    notice.textContent = message;

    container.appendChild(notice);

    setTimeout(function() {
        notice.style.opacity = '0';
        notice.style.transform = 'translateX(100%)';
        setTimeout(() => notice.remove(), 300);
    }, 4000);
}

// ===== Валидация форм =====
function setupFormValidation() {
    const forms = document.querySelectorAll('.validate-me, form[id$="-form"]');

    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;

            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    valid = false;
                    field.style.borderColor = 'var(--error)';
                    field.setAttribute('aria-invalid', 'true');
                } else {
                    field.style.borderColor = '';
                    field.removeAttribute('aria-invalid');
                }
            });

            if (!valid) {
                e.preventDefault();
                showNotification('Пожалуйста, заполните обязательные поля', 'error');
            }
        });
    });
}

// ===== Кнопка «Наверх» =====
function setupBackToTop() {
    const btn = document.getElementById('back-to-top');
    if (!btn) return;

    window.addEventListener('scroll', function() {
        if (window.scrollY > 400) {
            btn.classList.add('visible');
        } else {
            btn.classList.remove('visible');
        }
    });

    btn.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ===== Запуск =====
initTheme();

document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.getElementById('theme-toggle');
    if (toggle) toggle.addEventListener('click', toggleTheme);

    setupFormValidation();
    setupBackToTop();
});
