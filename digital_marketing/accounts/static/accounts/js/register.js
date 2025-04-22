function verifyField(fieldName, value, errorSpanId, inputId) {
    const input = document.getElementById(inputId);
    const errorSpan = document.getElementById(errorSpanId);
  
    if (!value.trim()) {
      errorSpan.textContent = `${fieldName.replace('_', ' ')} is required`;
      input.style.border = '2px solid red';
      return;
    }
  
    // Field-specific regex validation
    const regexMap = {
      username: /^[a-zA-Z0-9_-]{2,}$/,
      email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      phone: /^(\d{10}|\d{3} \d{3} \d{4}|\d{5} \d{5})$/
    };
  
    const pattern = regexMap[fieldName];
    if (pattern && !pattern.test(value)) {
      errorSpan.textContent = `Invalid ${fieldName.replace('_', ' ')} format`;
      input.style.border = '2px solid red';
      return;
    }
  
    // DB availability check
    fetch(`/verify/?field=${fieldName}&value=${encodeURIComponent(value)}`)
      .then(response => response.json())
      .then(data => {
        if (!data.available) {
          errorSpan.textContent = `${fieldName.replace('_', ' ')} is already taken`;
          input.style.border = '2px solid red';
        } else {
          errorSpan.textContent = '';
          input.style.border = '2px solid green';
        }
      })
      .catch(() => {
        errorSpan.textContent = 'Something went wrong. Try again.';
        input.style.border = '2px solid red';
      });
  }
  
  // Setup event listeners
  document.addEventListener("DOMContentLoaded", () => {
    const fieldsToVerify = [
      { id: 'username', field: 'username', errorSpan: 'error-username' },
      { id: 'email', field: 'email', errorSpan: 'error-email' },
      { id: 'phone', field: 'phone', errorSpan: 'error-phone' }
    ];
  
    fieldsToVerify.forEach(item => {
      const input = document.getElementById(item.id);
      if (input) {
        input.addEventListener('blur', function () {
          verifyField(item.field, input.value, item.errorSpan, item.id);
        });
      }
    });
  });
  