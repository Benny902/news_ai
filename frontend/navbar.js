function loadNavbar() {
    fetch('navbar.html')
        .then(response => response.text())
        .then(data => {
            const navbarContainer = document.getElementById('navbarContainer');
            if (navbarContainer) {
                navbarContainer.innerHTML = data;
            } else {
                console.error('Navbar container not found.');
            }
        })
        .catch(error => console.error('Error fetching navbar:', error));
}

document.addEventListener('DOMContentLoaded', loadNavbar);

