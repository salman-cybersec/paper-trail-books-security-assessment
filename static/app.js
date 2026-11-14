
document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search");
    const cartItemsElement = document.getElementById("cart-items");
    const cartTotalElement = document.getElementById("cart-total");
    const checkoutForm = document.getElementById("checkout-form");
    const checkoutMessage = document.getElementById("checkout-message");

    const cart = new Map();

    const books = Array.from(document.querySelectorAll(".book-card")).map(card => {
        const button = card.querySelector(".add-cart");

        return {
            id: button.dataset.id,
            title: card.querySelector("h3").textContent,
            price: Number(card.querySelector("p:nth-of-type(3)").textContent.replace("Price: PKR ", "")),
            stock: Number(card.querySelector("p:nth-of-type(4)").textContent.replace("Available: ", ""))
        };
    });

    function renderCart() {
        cartItemsElement.replaceChildren();
        let total = 0;

        if (cart.size === 0) {
            cartItemsElement.textContent = "Your cart is empty.";
        }

        cart.forEach((quantity, id) => {
            const book = books.find(item => item.id === id);
            if (!book) return;

            const subtotal = book.price * quantity;
            total += subtotal;

            const row = document.createElement("p");
            row.textContent = `${book.title} x ${quantity} = PKR ${subtotal} `;

            const removeButton = document.createElement("button");
            removeButton.type = "button";
            removeButton.textContent = "Remove";
            removeButton.addEventListener("click", () => {
                cart.delete(id);
                renderCart();
            });

            row.appendChild(removeButton);
            cartItemsElement.appendChild(row);
        });

        cartTotalElement.textContent = `Total: PKR ${total}`;
    }

    document.querySelectorAll(".add-cart").forEach(button => {
        button.addEventListener("click", () => {
            const id = button.dataset.id;
            const book = books.find(item => item.id === id);
            const quantityInput = document.getElementById(`qty-${id}`);
            const quantity = Number(quantityInput.value);
            const currentQuantity = cart.get(id) || 0;

            if (!Number.isInteger(quantity) || quantity < 1) {
                alert("Please enter a valid quantity.");
                return;
            }

            if (currentQuantity + quantity > book.stock) {
                alert("Requested quantity exceeds available stock.");
                return;
            }

            cart.set(id, currentQuantity + quantity);
            renderCart();
        });
    });

    if (searchInput) {
        searchInput.addEventListener("input", () => {
            const term = searchInput.value.toLowerCase().trim();

            document.querySelectorAll(".book-card").forEach(card => {
                card.style.display = card.textContent.toLowerCase().includes(term)
                    ? ""
                    : "none";
            });
        });
    }

    checkoutForm.addEventListener("submit", async event => {
        event.preventDefault();
        checkoutMessage.textContent = "";

        if (cart.size === 0) {
            checkoutMessage.textContent = "Please add a book to your cart first.";
            return;
        }

        const formData = new FormData(checkoutForm);

        const order = {
            name: formData.get("name").trim(),
            email: formData.get("email").trim(),
            phone: formData.get("phone").trim(),
            items: Array.from(cart, ([id, quantity]) => ({ id, quantity }))
        };

        const submitButton = checkoutForm.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        submitButton.textContent = "Processing...";

        try {
            const response = await fetch("/order", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: new URLSearchParams({
                    name: order.name,
                    email: order.email,
                    phone: order.phone,
                    items: JSON.stringify(order.items)
                })
            });

            const result = await response.json();

            if (!response.ok || !result.success) {
                throw new Error(result.message || "Order could not be placed.");
            }

            checkoutMessage.textContent =
                `${result.message} Total: PKR ${result.total}`;

            cart.clear();
            checkoutForm.reset();
            renderCart();

            document.querySelectorAll(".book-card").forEach(card => {
                const id = card.querySelector(".add-cart").dataset.id;
                const book = books.find(item => item.id === id);
                const stockText = card.querySelector("p:nth-of-type(4)");
                const quantityInput = document.getElementById(`qty-${id}`);

                book.stock = Math.max(0, book.stock -
                    (order.items.find(item => item.id === id)?.quantity || 0));

                stockText.textContent = `Available: ${book.stock}`;
                quantityInput.max = book.stock;
                quantityInput.value = book.stock > 0 ? 1 : 0;

                card.querySelector(".add-cart").disabled = book.stock === 0;
            });

        } catch (error) {
            checkoutMessage.textContent = error.message;
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = "Place Order";
        }
    });

    renderCart();
});
