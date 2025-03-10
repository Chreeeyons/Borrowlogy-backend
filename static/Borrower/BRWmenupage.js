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

        cart = [];
        renderCart();
        renderHistory();
    
        alert("Borrow request confirmed!");
    }

    function renderHistory() {
        const historySection = document.getElementById("history-log");
        const savedHistory = localStorage.getItem(`historyLog_${currentUserEmail}`);
        if (savedHistory) {
            userHistoryLog = JSON.parse(savedHistory);
        }
    
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
        }
    }

    function clearHistoryLog() {
        userHistoryLog = [];
        localStorage.removeItem(`historyLog_${currentUserEmail}`);
        renderHistory();
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
        historyLog = []; // ✅ Clear the array
        localStorage.removeItem("historyLog"); // ✅ Remove from storage
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
