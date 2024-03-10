$(document).ready(function() {
    // Hide the navigation initially
    $('.navbar').hide();

    // Track cursor movement
    $(document).mousemove(function(event) {
        var y = event.clientY;

        // If cursor is near the top, show the navigation
        if (y < 50) {
            $('.navbar').slideDown();
        } else {
            // Otherwise, hide it
            $('.navbar').slideUp();
        }
    });
});
