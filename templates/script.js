async function submitForm(event) {
    event.preventDefault();                                                 // Prevent default form submission

    const formData = new FormData(event.target);                            // Form data collection.
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const data = await response.json();
        alert(data.message);                                                // Show success message

        // Clear file names display after successful upload
        const infoArea = document.getElementById('file-upload-filenames');
        infoArea.textContent = '';                                          // Clear the displayed file names
        event.target.reset();                                               // Reset the form fields

    } else {
        alert('Failed to sign PDF. Please try again.'); // Error handling
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const input = document.getElementById('file-upload');
    const infoArea = document.getElementById('file-upload-filenames');

    input.addEventListener('change', function() {
        const fileList = Array.from(input.files);
        const fileNames = fileList.map(file => file.name).join(', ');

        infoArea.textContent = fileNames;                                   // Display the uploaded file names.
    });
});
