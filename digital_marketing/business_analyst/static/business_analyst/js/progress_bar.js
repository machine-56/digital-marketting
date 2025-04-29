document.addEventListener('DOMContentLoaded', function () {
    const progressValues = document.querySelectorAll('.progress-value');
    progressValues.forEach((valueElement) => {
        const percentage = parseInt(valueElement.textContent.trim());
        const progressBar = valueElement.closest('.card').querySelector('.progress-bar');

        // Set width and text
        progressBar.style.width = percentage + '%';
        progressBar.textContent = percentage + '%';

        // Set color based on percentage
        if (percentage >= 100) {
            progressBar.style.backgroundColor = '#28a745'; // Green
        } else if (percentage >= 50) {
            progressBar.style.backgroundColor = '#ffc107'; // Yellow
        } else {
            progressBar.style.backgroundColor = '#dc3545'; // Red
        }
    });
});



