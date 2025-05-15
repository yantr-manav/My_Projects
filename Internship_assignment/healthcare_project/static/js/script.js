// Check if password and confirm password match
document.addEventListener('DOMContentLoaded', function() {
    const password1Field = document.getElementById('id_password1');
    const password2Field = document.getElementById('id_password2');
    const form = document.querySelector('form');
    
    if (form && password1Field && password2Field) {
        form.addEventListener('submit', function(e) {
            if (password1Field.value !== password2Field.value) {
                e.preventDefault();
                alert('Passwords do not match!');
                
                // Add error styling
                password1Field.classList.add('is-invalid');
                password2Field.classList.add('is-invalid');
            }
        });
        
        // Reset validation styling when typing
        password1Field.addEventListener('input', function() {
            password1Field.classList.remove('is-invalid');
            password2Field.classList.remove('is-invalid');
        });
        
        password2Field.addEventListener('input', function() {
            password1Field.classList.remove('is-invalid');
            password2Field.classList.remove('is-invalid');
        });
    }
});