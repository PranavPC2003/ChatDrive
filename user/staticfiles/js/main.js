$(document).ready(function () {
    // Code to run when the document is ready

    // Example code: Show an alert when a button is clicked
    $('#myButton').click(function () {
        alert('Button clicked!');
    });

    // Example code: Toggle a CSS class on an element
    $('#myToggleElement').click(function () {
        $(this).toggleClass('active');
    });

    // Example code: Initialize DataTables plugin
    $('#myDataTable').DataTable();

    // You can add more functionality and event handlers here...
});

