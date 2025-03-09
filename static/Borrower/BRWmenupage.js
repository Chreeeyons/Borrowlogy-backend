document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript loaded successfully!");

    const menuLinks = document.querySelectorAll(".menu-container a");
    const sections = document.querySelectorAll(".section");
    const addToCartButtons = document.querySelectorAll(".add-to-cart");
    const cartSection = document.getElementById("caaart");
    const cartContainer = document.createElement("div");
    cartContainer.className = "cart-container";

    let cart = [];

    // ✅ Handle Click Events for Menu Buttons
    menuLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault();

            const targetId = this.getAttribute("href").substring(1);
            const targetSection = document.getElementById(targetId);

            sections.forEach(section => {
                section.classList.remove("active");
                section.style.display = "none";
            });

            if (targetSection) {
                targetSection.classList.add("active");
                targetSection.style.display = "block";
                window.scrollTo({ top: targetSection.offsetTop, behavior: 'smooth' });
                console.log("Navigated to:", targetId);
            } else {
                console.warn("Section not found:", targetId);
            }
        });
    });

    // ✅ Handle Add to Cart
    addToCartButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            const card = button.closest(".equipment-card");
            const itemName = card.querySelector("h2").innerText;
            const quantitySelect = card.querySelector(".qty-dropdown");
            const quantity = parseInt(quantitySelect.value);

            addItemToCart(itemName, quantity);
            alert("Item added to cart successfully!");
        });
    });

    // ✅ Add item to cart
    function addItemToCart(itemName, quantity) {
        const existingItem = cart.find(item => item.name === itemName);

        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            cart.push({ name: itemName, quantity: quantity });
        }
        renderCart();
    }

    // ✅ Render Cart Items
    function renderCart() {
        cartSection.innerHTML = "<h1 class='header'>BORROWER'S CART</h1>";
        cartContainer.innerHTML = "";

        if (cart.length === 0) {
            cartContainer.innerHTML = "<p>No items in cart.</p>";
        } else {
            cart.forEach((item, index) => {
                const cartItem = document.createElement("div");
                cartItem.className = "cart-item";

                cartItem.innerHTML = `
                    <p>${item.name} - Quantity: ${item.quantity}</p>
                    <button onclick="removeItem(${index})">Remove</button>
                `;

                cartContainer.appendChild(cartItem);
            });
        }
        cartSection.appendChild(cartContainer);
    }

    // ✅ Remove item from cart
    window.removeItem = function(index) {
        cart.splice(index, 1);
        renderCart();
    }

    // ✅ Function to Go to Cart Section (Fixed)
    window.goToCart = function() {
        sections.forEach(section => {
            section.classList.remove("active");
            section.style.display = "none";
        });

        cartSection.classList.add("active");
        cartSection.style.display = "block";
        window.scrollTo({ top: cartSection.offsetTop, behavior: 'smooth' });
        console.log("Navigated to Cart Section.");
    }

    // ✅ Fix Go to Cart Button Click (Now Works)
    const goToCartButton = document.querySelector(".go-to-cart");
    if (goToCartButton) {
        goToCartButton.addEventListener("click", function (event) {
            event.preventDefault();
            goToCart();
        });
    }

    // ✅ Ensure Cart Button Works After Page Load
    document.body.addEventListener("click", function(event) {
        if (event.target.classList.contains("go-to-cart")) {
            event.preventDefault();
            goToCart();
        }
    });

    // ✅ Default section to Laboratory Materials
    sections.forEach(section => section.classList.remove("active"));
    const firstSection = document.getElementById("laboratory-materials");
    if (firstSection) {
        firstSection.classList.add("active");
        firstSection.style.display = "block";
    }
});
