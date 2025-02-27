document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript loaded successfully!");

    const menuLinks = document.querySelectorAll(".menu-container a");
    const sections = document.querySelectorAll(".section");

    // Function to switch sections
    menuLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent default jump behavior

            const targetId = this.getAttribute("href").substring(1);
            const targetSection = document.getElementById(targetId);

            console.log("Clicked on:", targetId);
            console.log("Target section found:", targetSection);

            if (targetSection) {
                // Hide all sections first
                sections.forEach(section => {
                    section.classList.remove("active");
                    section.style.display = "none"; // Ensures no blank space
                });

                // Show only the clicked section
                targetSection.classList.add("active");
                targetSection.style.display = "block";

                // Scroll smoothly to the section
                targetSection.scrollIntoView({ behavior: "smooth" });

                console.log("Activated section:", targetId);
                console.log("Section HTML:", targetSection.innerHTML);
            } else {
                console.warn("Target section not found:", targetId);
            }
        });
    });

    // Initially show only the first section
    sections.forEach(section => section.classList.remove("active"));
    const firstSection = document.getElementById("laboratory-materials");
    if (firstSection) {
        firstSection.classList.add("active");
        firstSection.style.display = "block";
    }
});
