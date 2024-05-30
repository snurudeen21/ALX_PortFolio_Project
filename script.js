document.getElementById('soilForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission
    
    // Get form values
    var sieveSize = document.getElementById('sieveSize').value;
    var cumulativeRetained = document.getElementById('cumulativeRetained').value;
    var percentPassing = document.getElementById('percentPassing').value;
    var liquidLimit = document.getElementById('liquidLimit').value;
    var plasticLimit = document.getElementById('plasticLimit').value;
    
    // Perform client-side validation
    if (sieveSize === '' || cumulativeRetained === '' || percentPassing === '' || liquidLimit === '' || plasticLimit === '') {
        alert('Please fill in all fields.');
        return;
    }
    
    // Send form data to backend for processing (AJAX request)
    var formData = new FormData();
    formData.append('sieveSize', sieveSize);
    formData.append('cumulativeRetained', cumulativeRetained);
    formData.append('percentPassing', percentPassing);
    formData.append('liquidLimit', liquidLimit);
    formData.append('plasticLimit', plasticLimit);
    
    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Display response from backend
        document.getElementById('response').innerHTML = `<p>${data.message}</p>`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
