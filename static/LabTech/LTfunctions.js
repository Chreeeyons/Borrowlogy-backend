document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent form from reloading the page

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value; 

        // Dummy validation (Replace with actual authentication logic)
        if (username === "admin" && password === "4444") {
            alert("Login successful!");
            window.location.href = "LTmenupage.html"; // Redirect to menu page
        } else {
            alert("Invalid username or password.");
        }
    });
});
