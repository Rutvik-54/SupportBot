document.addEventListener('DOMContentLoaded', function() {
    // Get all forms with the needs-validation class
    const forms = document.querySelectorAll('.needs-validation');
    
    // Password validation regex
    const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
    
    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            // Custom password validation
            const password = form.querySelector('#password');
            const confirmPassword = form.querySelector('#confirm_password');
            
            if (password && confirmPassword) {
                if (!passwordRegex.test(password.value)) {
                    password.setCustomValidity('Password must be at least 8 characters long and include uppercase, lowercase, and numbers.');
                    event.preventDefault();
                    event.stopPropagation();
                } else {
                    password.setCustomValidity('');
                }
                
                if (password.value !== confirmPassword.value) {
                    confirmPassword.setCustomValidity('Passwords do not match.');
                    event.preventDefault();
                    event.stopPropagation();
                } else {
                    confirmPassword.setCustomValidity('');
                }
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Real-time password matching validation
    const confirmPassword = document.querySelector('#confirm_password');
    if (confirmPassword) {
        confirmPassword.addEventListener('input', function() {
            const password = document.querySelector('#password');
            if (this.value !== password.value) {
                this.setCustomValidity('Passwords do not match.');
            } else {
                this.setCustomValidity('');
            }
        });
    }
    
    // Real-time password strength validation
    const password = document.querySelector('#password');
    if (password) {
        password.addEventListener('input', function() {
            if (!passwordRegex.test(this.value)) {
                this.setCustomValidity('Password must be at least 8 characters long and include uppercase, lowercase, and numbers.');
            } else {
                this.setCustomValidity('');
            }
        });
    }
}); 