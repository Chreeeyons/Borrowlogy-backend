document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript loaded successfully!");

    const menuLinks = document.querySelectorAll(".menu-container a");
    const sections = document.querySelectorAll(".section");
    const addToCartButtons = document.querySelectorAll(".add-to-cart");
    const cartSection = document.getElementById("caaart");
    const cartContainer = document.createElement("div");
    cartContainer.className = "cart-container";

    let cart = [];
    let currentUserEmail = localStorage.getItem("currentUserEmail") || "guest"; 
    let userHistoryLog = JSON.parse(localStorage.getItem(`historyLog_${currentUserEmail}`)) || [];

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

                if (targetId === "history") {
                    renderHistory();
                }
            }
        });
    });

    addToCartButtons.forEach(button => {
        button.addEventListener("click", function () {
            const card = button.closest(".equipment-card");
            const itemName = card.querySelector("h2").innerText;
            const quantityInput = card.querySelector(".qty-input");
            let quantity = parseInt(quantityInput.value);
            const availableStock = parseInt(quantityInput.getAttribute("max"));

            if (isNaN(quantity) || quantity < 1) {
                alert("Please enter a valid quantity.");
                return;
            }

            const existingItem = cart.find(item => item.name === itemName);
            const totalQuantity = existingItem ? existingItem.quantity + quantity : quantity;

            if (totalQuantity > availableStock) {
                alert(`Only ${availableStock} item(s) are available. You already have ${existingItem ? existingItem.quantity : 0} in cart.`);
                return;
            }

            addItemToCart(itemName, quantity);
            alert("Item added to cart successfully!");
        });
    });

    function addItemToCart(itemName, quantity) {
        const existingItem = cart.find(item => item.name === itemName);

        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            cart.push({ name: itemName, quantity: quantity });
        }

        renderCart();
    }

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
        
            const confirmButton = document.createElement("button");
            confirmButton.innerText = "Confirm Borrow Request";
            confirmButton.className = "confirm-borrow";
            confirmButton.onclick = confirmBorrowRequest;
        
            cartContainer.appendChild(confirmButton);
        }        
        cartSection.appendChild(cartContainer);
    }

    function confirmBorrowRequest() {
        if (cart.length === 0) {
            alert("Your cart is empty!");
            return;
        }
    
        let transactionNumber = userHistoryLog.length + 1;
        let timestamp = new Date().toLocaleString();
        let transaction = { transactionId: `Transaction #${transactionNumber}`, timestamp: timestamp, items: [...cart] };
        userHistoryLog.push(transaction);
    
        localStorage.setItem(`historyLog_${currentUserEmail}`, JSON.stringify(userHistoryLog));
    
        // ✅ Update Stock Quantities in the UI
        cart.forEach(cartItem => {
            const itemCards = document.querySelectorAll(".equipment-card");
    
            itemCards.forEach(card => {
                const itemNameElement = card.querySelector("h2");
                const qtyInput = card.querySelector(".qty-input");
                const stockDisplay = card.querySelector(".quantity"); // ✅ Fix: Get the "Quantity: X" text
                const statusElement = card.querySelector(".status .available"); // ✅ Get status element
    
                if (itemNameElement.innerText === cartItem.name) {
                    let currentStock = parseInt(qtyInput.getAttribute("max"));
                    let newStock = currentStock - cartItem.quantity;
    
                    // ✅ Prevent stock from going below zero
                    qtyInput.setAttribute("max", newStock);
                    qtyInput.value = newStock;
    
                    // ✅ Update the "Quantity: X" text
                    if (stockDisplay) {
                        stockDisplay.innerText = `Quantity: ${newStock}`;
                    }
    
                    // ✅ Handle Out of Stock scenario
                    if (newStock <= 0) {
                        qtyInput.disabled = true;
                        qtyInput.style.opacity = "0.5";
                        card.querySelector(".add-to-cart").disabled = true;
                        card.querySelector(".add-to-cart").style.opacity = "0.5";
                        card.querySelector(".add-to-cart").style.cursor = "not-allowed";
    
                        if (statusElement) {
                            statusElement.classList.remove("available");
                            statusElement.classList.add("out-of-stock");
                            statusElement.innerText = "Out of Stock";
                        }
                    }
                }
            });
        });
    
        cart = [];
        renderCart();
        renderHistory();
        
        alert("Borrow request confirmed!");
    }    

    function renderHistory() {
        const historySection = document.getElementById("history-log");
    
        // ✅ Ensure we only load history for the logged-in user
        let savedHistory = localStorage.getItem(`historyLog_${currentUserEmail}`);
        userHistoryLog = savedHistory ? JSON.parse(savedHistory) : [];
    
        historySection.innerHTML = "";
    
        if (userHistoryLog.length === 0) {
            historySection.innerHTML = "<p>No borrow history yet.</p>";
        } else {
            userHistoryLog.forEach(transaction => {
                let transactionDiv = document.createElement("div");
                transactionDiv.className = "transaction";
                transactionDiv.innerHTML = `<h3>${transaction.transactionId}</h3><p>${transaction.timestamp}</p>`;
    
                transaction.items.forEach(item => {
                    let logEntry = document.createElement("p");
                    logEntry.textContent = `${item.name} - Quantity: ${item.quantity}`;
                    transactionDiv.appendChild(logEntry);
                });
    
                historySection.appendChild(transactionDiv);
            });
    
            // ✅ Make sure the "Clear History" button only affects the logged-in user
            const clearButton = document.createElement("button");
            clearButton.innerText = "Clear History";
            clearButton.classList.add("clear-history-btn");
            clearButton.onclick = clearHistoryLog;
            historySection.appendChild(clearButton);
        }
    }    
    
    window.onload = function () {
        renderHistory();
    };

    window.removeItem = function(index) {
        cart.splice(index, 1);
        renderCart();
    };

    window.goToCart = function() {
        sections.forEach(section => {
            section.classList.remove("active");
            section.style.display = "none";
        });

        cartSection.classList.add("active");
        cartSection.style.display = "block";
        window.scrollTo({ top: cartSection.offsetTop, behavior: 'smooth' });
    };

    renderHistory();

    function clearHistoryLog() {
        userHistoryLog = []; // ✅ Reset only the current user's log
        localStorage.removeItem(`historyLog_${currentUserEmail}`); // ✅ Remove only their history
        renderHistory(); // ✅ Refresh the display
    }      
    
    // ✅ Add a Clear History Button
    document.addEventListener("DOMContentLoaded", function () {
        const historySection = document.getElementById("history-log");
        
        const clearButton = document.createElement("button");
        clearButton.innerText = "Clear History";
        clearButton.classList.add("clear-history-btn");
        clearButton.onclick = clearHistoryLog;
        
        historySection.appendChild(clearButton);
    });
    
});
