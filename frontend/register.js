// register.js

const registerForm = document.getElementById('registerForm');

registerForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(registerForm);
    const formDataJSON = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('http://localhost:5000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formDataJSON)
        });

        if (!response.ok) {
            throw new Error('Registration failed');
        }

        // else, registration successful so redirect to login page
        window.location.href = 'login.html';

    } catch (error) {
        console.error('Error:', error);
    }
});
