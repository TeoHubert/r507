
function showToast(title, message, type = 'info') {
    const toast = document.getElementById('notificationToast');
    const toastTitle = document.getElementById('toastTitle');
    const toastMessage = document.getElementById('toastMessage');
    const toastIcon = document.getElementById('toastIcon');
    const toastTime = document.getElementById('toastTime');
    
    toastTitle.textContent = title;
    toastMessage.textContent = message;
    toastTime.textContent = new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
    
    toastIcon.className = 'rounded me-2';
    switch(type) {
        case 'success':
            toastIcon.style.backgroundColor = '#198754';
            break;
        case 'error':
            toastIcon.style.backgroundColor = '#dc3545';
            break;
        case 'warning':
            toastIcon.style.backgroundColor = '#fd7e14';
            break;
        default: // info
            toastIcon.style.backgroundColor = '#0d6efd';
    }
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}