document.addEventListener('DOMContentLoaded', function() {
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const loginBtn = document.getElementById('loginBtn');

    if (!usernameInput || !passwordInput || !loginBtn) {
        console.error('Error: Username, password input elements, or login button not found.');
        return;
    }

    loginBtn.addEventListener('click', function() {
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();

        fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Login failed');
            }
            return response.json();
        })
        .then(data => {
            if (data.token) {
                localStorage.setItem('token', data.token); // save token in localStorage
                window.location.href = './index.html'; // redirect to profile page
            } else {
                console.error('Login failed:', data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
