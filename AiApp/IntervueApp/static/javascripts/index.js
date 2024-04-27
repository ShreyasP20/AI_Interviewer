document.querySelector('form').addEventListener('submit', function(event) {
    var input = document.getElementById('inputString').value.trim();
    if (!input) {
        event.preventDefault(); // Prevent form submission
        document.getElementById('error-message').style.display = 'block'; // Display error message
    }
});