document.addEventListener("DOMContentLoaded", function () {
    const menuLinks = document.querySelectorAll(".menu-container a");
    const sections = document.querySelectorAll(".section");

    menuLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            const targetId = this.getAttribute("href").substring(1);
            const targetSection = document.getElementById(targetId);

            if (targetSection) {
                sections.forEach(section => section.classList.remove("active"));
                targetSection.classList.add("active");

                // Fetch lab materials only when "Laboratory Materials" is clicked
                if (targetId === "laboratory-materials") {
                    fetch("/labtech/materials/") // Django URL
                        .then(response => response.json())
                        .then(data => {
                            const materialsList = document.getElementById("materials-list");
                            materialsList.innerHTML = ""; // Clear previous items
                            if (data.length === 0) {
                                materialsList.innerHTML = "<p>No materials available.</p>";
                            } else {
                                data.forEach(material => {
                                    const li = document.createElement("li");
                                    li.textContent = `${material.name} - ${material.quantity} Available`;
                                    materialsList.appendChild(li);
                                });
                            }
                        })
                        .catch(error => console.error("Error fetching materials:", error));
                }
            }
        });
    });

    if (!document.querySelector(".section.active")) {
        document.getElementById("borrowers-request").classList.add("active");
    }
});
