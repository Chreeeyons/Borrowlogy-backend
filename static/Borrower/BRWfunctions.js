document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission

        const username = document.getElementById("username").value;

        if (username.trim() !== "") { // Ensure username is entered
            alert("Login successful!");
            window.location.href = "../templates/BRWmenupage.html"; // Adjust the path
        } else {
            alert("Please enter UP Mail.");
        }
    });
});
