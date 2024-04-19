document.getElementById("petForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission

    var formData = new FormData(this);
    var xhr = new XMLHttpRequest();

    xhr.open("POST", "upload.php"); // Change "upload.php" to your server-side script
    xhr.upload.addEventListener("progress", function(event) {
        if (event.lengthComputable) {
            var percentComplete = (event.loaded / event.total) * 100;
            document.getElementById("progressBarFill").style.width = percentComplete + "%";
        }
    });

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // Upload complete
            alert("Upload complete!");
            // Optionally, you can redirect or perform other actions after upload completion
        }
    };

    xhr.send(formData);
});
