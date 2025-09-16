document.addEventListener('DOMContentLoaded', function() {

    // --- 1. Active Navigation Link Highlighter ---
    // This script adds the 'active' class to the nav link corresponding to the current page.
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        // Check if the link's href is the current page.
        // For the home page, the pathname is '/', so we need a special check.
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });

    // --- 2. Smooth Fade-In for Main Content ---
    // Adds a 'visible' class to the main container after a short delay for a fade-in effect.
    const mainContainer = document.querySelector('.main-container');
    if (mainContainer) {
        // Use a short timeout to ensure the CSS transition is applied correctly
        setTimeout(() => {
            mainContainer.classList.add('visible');
        }, 100);
    }

    // --- 3. "Back to Top" Button Functionality ---
    const backToTopButton = document.getElementById('back-to-top');

    if (backToTopButton) {
        // Show the button when the user scrolls down 300px from the top
        window.onscroll = function() {
            if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
                backToTopButton.style.display = 'block';
            } else {
                backToTopButton.style.display = 'none';
            }
        };

        // When the user clicks on the button, scroll to the top of the document smoothly
        backToTopButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

});