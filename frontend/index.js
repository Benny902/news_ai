document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('token');
    
    if (!token) {
        // redirect to login page if token is missing
        window.location.replace('./login.html');
    } else {
        // fetch and display user profile if token is present
        fetchUserProfile(token);
    }

    function fetchUserProfile(token) {
        fetch('http://localhost:5000/profile', {
            method: 'GET',
            headers: {
                'Authorization': token
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch profile');
            }
            return response.json();
        })
        .then(data => {
            console.log('Profile data:', data);
            displayUserProfile(data);
            populateEditForm(data);
        })
        .catch(error => {
            console.error('Error fetching profile:', error);
        });
    }

    function displayUserProfile(user) {
        const profileInfo = document.getElementById('profileInfo');
        if (!profileInfo) return;

        profileInfo.innerHTML = `
            <p><strong>Username:</strong> ${user.username}</p>
            <p><strong>Email:</strong> ${user.email ? user.email : 'Not provided'}</p>
            <p><strong>Preferences:</strong> ${user.preferences ? user.preferences : 'Not set'}</p>
            <p><strong>Categories:</strong> ${user.category_preferences ? user.category_preferences : 'Not set'}</p>
        `;
    }

    function populateEditForm(user) {
        const editPreferencesInput = document.getElementById('editPreferences');
        const editEmailInput = document.getElementById('editEmail');

        if (!editPreferencesInput || !editEmailInput || !dropdownContent) return;

        editPreferencesInput.value = user.preferences || ''; // set input value to current preferences or empty string
        editEmailInput.value = user.email || ''; // set input value to current email number or empty string

        const selectedCategories = user.category_preferences ? user.category_preferences.split(',') : [];

        dropdownContent.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = selectedCategories.includes(checkbox.value);
        });
    }

    // event listener for editPreferencesForm submission
    const editPreferencesForm = document.getElementById('editPreferencesForm');
    editPreferencesForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const editPreferences = document.getElementById('editPreferences').value;

        const formData = {
            preferences: editPreferences
        };

        fetch('http://localhost:5000/profile', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update preferences');
            }
            return response.json();
        })
        .then(data => {
            console.log('Preferences updated:', data);
            displayEditProfileMessage('Preferences updated successfully');
            setTimeout(() => {
                window.location.reload();
            }, 1000); // delay reload for 1 second
        })
        .catch(error => {
            console.error('Error updating preferences:', error);
            displayEditProfileMessage(`Error: ${error.message}`);
        });
    });

    // event listener for editEmailForm submission
    const editEmailForm = document.getElementById('editEmailForm');
    editEmailForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const editEmail = document.getElementById('editEmail').value;

        const formData = {
            email: editEmail
        };

        fetch('http://localhost:5000/profile', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update email number');
            }
            return response.json();
        })
        .then(data => {
            console.log('Email number updated:', data);
            displayEditProfileMessage('Email number updated successfully');
            setTimeout(() => {
                window.location.reload();
            }, 1000); // delay reload for 1 second
        })
        .catch(error => {
            console.error('Error updating email number:', error);
            displayEditProfileMessage(`Error: ${error.message}`);
        });
    });

    function displayEditProfileMessage(message) {
        const editProfileMessage = document.getElementById('editProfileMessage');
        if (editProfileMessage) {
            editProfileMessage.textContent = message;
        }
    }


    // handle form submission for categoryPreferences
    const editCategoryPreferencesForm = document.getElementById('editCategoryPreferencesForm');
    editCategoryPreferencesForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const selectedCategories = Array.from(dropdownContent.querySelectorAll('input[type="checkbox"]:checked'))
                                        .map(checkbox => checkbox.value)
                                        .join(',');

        const formData = {
            category_preferences: selectedCategories
        };

        fetch('http://localhost:5000/profile', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update category preferences');
            }
            return response.json();
        })
        .then(data => {
            console.log('Category preferences updated:', data);
            displayEditProfileMessage('Category preferences updated successfully');
            setTimeout(() => {
                window.location.reload();
            }, 1000); // delay reload for 1 second
        })
        .catch(error => {
            console.error('Error updating category preferences:', error);
            displayEditProfileMessage(`Error: ${error.message}`);
        });
    });

    function displayEditProfileMessage(message) {
        const editProfileMessage = document.getElementById('editProfileMessage');
        if (editProfileMessage) {
            editProfileMessage.textContent = message;
        }
    }

    // get the dropdown elements
    const dropdownButton = document.getElementById('dropdownButton');
    const dropdownContent = document.getElementById('dropdownContent');
    const checkboxes = dropdownContent.querySelectorAll("input[type='checkbox']");

    dropdownButton.addEventListener('click', function(event) {
        event.stopPropagation();
        dropdownContent.classList.toggle('show');
    });

    document.addEventListener('click', function(event) {
        if (!dropdownContent.contains(event.target) && event.target !== dropdownButton) {
            dropdownContent.classList.remove('show');
        }
    });

    dropdownContent.addEventListener('click', function(event) {
        event.stopPropagation();
    });

    // enforce selection limit to 5 - this is because newsdata.io has a limit of 5 categories per search
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const selectedCheckboxes = dropdownContent.querySelectorAll("input[type='checkbox']:checked");
            if (selectedCheckboxes.length >= 5) {
                checkboxes.forEach(cb => {
                    if (!cb.checked) {
                        cb.disabled = true;
                    }
                });
            } else {
                checkboxes.forEach(cb => cb.disabled = false);
            }
        });
    });

    // close dropdown if clicked outside
    window.onclick = function(event) {
        if (!event.target.matches('#dropdownButton')) {
            if (dropdownContent.style.display === "block") {
                dropdownContent.style.display = "none";
            }
        }
    };
});

function logout() {
    // clear any stored token or session data and redirect to the login page
    localStorage.removeItem('token');
    window.location.href = 'login.html';
}

// get the modal and open/close button elements
const modal = document.getElementById("tipsModal");
const openBtn = document.getElementById("openTipsModal");
const closeBtn = document.getElementsByClassName("close-button")[0]; // Assuming there's only one close button

// when the user clicks the modal (advance tips) button, open the modal 
openBtn.onclick = function() {
  modal.style.display = "block";
}

// when the user clicks on X, close the modal
closeBtn.onclick = function() {
  modal.style.display = "none";
}

// when the user presses the ESC key, close the modal
window.onkeydown = function(event) {
    if (event.key === "Escape" || event.key === "Esc") {
        modal.style.display = "none";
    }
}