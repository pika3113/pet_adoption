// Add an event listener to execute code when the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Set the initial position of the background element to 'fixed'
    document.querySelector('.background').style.position = 'fixed';
});

// Add the scroll event listener
window.addEventListener('scroll', function() {
    var scrollPosition = window.scrollY;
    var scrollThreshold = 500;

    if (scrollPosition >= scrollThreshold) {
        document.querySelector('.background').style.position = 'absolute';
    } else {
        document.querySelector('.background').style.position = 'fixed';
    }
});
