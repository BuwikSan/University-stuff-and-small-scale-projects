/* ==================== MAIN JS ==================== */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 KrizeMapa app loaded');
    
    // Auto-hide alerts po 5 sekundách
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.3s';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        }, 5000);
    });
});
