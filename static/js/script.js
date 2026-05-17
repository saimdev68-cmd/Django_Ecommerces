document.addEventListener('DOMContentLoaded', () => {
    const dropdownContainers = document.querySelectorAll('.has-dropdown');
    
    // Time in milliseconds to wait before closing/opening (prevents accidental flickering)
    const hoverDelay = 150; 

    dropdownContainers.forEach(container => {
        let timeoutId = null;

        // When the mouse enters the navigation item area
        container.addEventListener('mouseenter', () => {
            // Clear any pending close actions
            clearTimeout(timeoutId);
            
            // Add the open class immediately on hover for responsive feedback
            container.classList.add('open');
        });

        // When the mouse leaves the navigation item or its open dropdown box
        container.addEventListener('mouseleave', () => {
            // Delay the removal of the 'open' class slightly
            timeoutId = setTimeout(() => {
                container.classList.remove('open');
            }, hoverDelay);
        });
    });

    // Prevent dead layout links (#) from snapping the browser screen to the top header
    const deadLinks = document.querySelectorAll('a[href="#"]');
    deadLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
        });
    });
});

