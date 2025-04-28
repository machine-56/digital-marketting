function validateField(fieldName, value, errorSpanId, userId) {
    const errorSpan = document.getElementById(errorSpanId);
    errorSpan.textContent = '';
  

    if (!value.trim()) {
      errorSpan.textContent = `${fieldName.charAt(0).toUpperCase() + fieldName.slice(1)} is required`;
      return;
    }
  

    if (fieldName === 'email') {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(value)) {
        errorSpan.textContent = 'Invalid email format';
        return;
      }
    }
  
    if (fieldName === 'phone') {
      const phoneRegex = /^\d{10}$/;
      if (!phoneRegex.test(value)) {
        errorSpan.textContent = 'Phone number must be 10 digits';
        return;
      }
    }
  

    fetch(`/ad/validate_user/?field=${fieldName}&value=${encodeURIComponent(value)}&exclude_id=${userId}`)
      .then(response => response.json())
      .then(data => {
        if (!data.available) {
          errorSpan.textContent = `${fieldName.charAt(0).toUpperCase() + fieldName.slice(1)} is already taken`;
        } else {
          errorSpan.textContent = '';
        }
      })
      .catch(() => {
        errorSpan.textContent = 'Error validating field';
      });
  }
  