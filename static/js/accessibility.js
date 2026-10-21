// Умный режим доступности
document.addEventListener("DOMContentLoaded", function() {
    const navLinks = document.querySelector('.nav-links');
    if (navLinks) {
        const fontBtn = document.createElement('button');
        fontBtn.className = 'theme-toggle';
        fontBtn.innerHTML = 'A+';
        fontBtn.title = 'Увеличить шрифт';
        fontBtn.style.fontSize = '0.9rem';
        fontBtn.style.fontWeight = 'bold';
        
        const contrastBtn = document.createElement('button');
        contrastBtn.className = 'theme-toggle';
        contrastBtn.innerHTML = '🌓';
        contrastBtn.title = 'Высокий контраст';
        
        navLinks.insertBefore(fontBtn, navLinks.querySelector('#theme-toggle'));
        navLinks.insertBefore(contrastBtn, navLinks.querySelector('#theme-toggle'));

        let currentFontSize = 100;
        fontBtn.addEventListener('click', () => {
            if (currentFontSize === 100) currentFontSize = 120;
            else if (currentFontSize === 120) currentFontSize = 140;
            else currentFontSize = 100;
            
            document.documentElement.style.fontSize = currentFontSize + '%';
            localStorage.setItem('fontSize', currentFontSize);
            showNotification('Размер шрифта: ' + currentFontSize + '%');
        });

        const savedFontSize = localStorage.getItem('fontSize');
        if (savedFontSize) {
            currentFontSize = parseInt(savedFontSize);
            document.documentElement.style.fontSize = currentFontSize + '%';
        }

        contrastBtn.addEventListener('click', () => {
            const isHighContrast = document.body.classList.toggle('high-contrast');
            localStorage.setItem('highContrast', isHighContrast);
            showNotification(isHighContrast ? 'Высокий контраст включен' : 'Высокий контраст выключен');
        });

        if (localStorage.getItem('highContrast') === 'true') {
            document.body.classList.add('high-contrast');
        }
    }
});

function showNotification(message) {
    let notification = document.getElementById('visual-notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'visual-notification';
        notification.style.cssText = 'position: fixed; bottom: 20px; right: 20px; background: #3b82f6; color: white; padding: 15px 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); font-family: Inter, sans-serif; z-index: 9999; transition: opacity 0.3s, transform 0.3s; opacity: 0; transform: translateY(20px);';
        document.body.appendChild(notification);
    }
    notification.textContent = message;
    notification.style.opacity = '1';
    notification.style.transform = 'translateY(0)';
    
    clearTimeout(notification.timeout);
    notification.timeout = setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateY(20px)';
    }, 3000);
}
