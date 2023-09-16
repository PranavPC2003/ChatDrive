$(document).ready(function () {
    const input = document.getElementById("upload");
    const filewrapper = document.getElementById("filewrapper");

    input.addEventListener("change", function (e) {
        let fileName = e.target.files[0].name;
        let filetype = e.target.value.split(".").pop();
        fileshow(fileName, filetype);
        uploadFile(e.target.files[0]); // Upload the file to the server
    });

    const uploadFile = function (file) {
        let formData = new FormData();
        formData.append("uploadedFile", file);

        $.ajax({
            type: "POST",
            url: "upload.php", // Path to your upload script
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                console.log(response); // Log the response from the server
            },
            error: function () {
                console.log("Error uploading file.");
            }
        });
    };
});