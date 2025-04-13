// Initialize tooltips and popovers
$(document).ready(function() {
    // Enable dropdowns
    $('.dropdown-toggle').dropdown();
    
    // Enable tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();
    
    // Enable popovers
    $('[data-bs-toggle="popover"]').popover();
});