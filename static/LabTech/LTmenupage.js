document.addEventListener("DOMContentLoaded", function () {
    const menuLinks = document.querySelectorAll(".menu-container a");
    const sections = document.querySelectorAll(".section");

    menuLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent default jump behavior

            const targetId = this.getAttribute("href").substring(1);
            const targetSection = document.getElementById(targetId);

            if (targetSection) {
                // Hide all sections first
                sections.forEach(section => section.classList.remove("active"));

                // Show only the clicked section
                targetSection.classList.add("active");

                // Scroll smoothly to the section
                targetSection.scrollIntoView({ behavior: "smooth" });
            }
        });
    });

    // Initially show only the first section
    sections.forEach(section => section.classList.remove("active"));
    document.getElementById("borrowers-request").classList.add("active");
});
