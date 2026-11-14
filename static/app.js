document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search");
    const bookCards = document.querySelectorAll(".book-card");

    if (searchInput) {
        searchInput.addEventListener("input", () => {
            const searchTerm = searchInput.value.toLowerCase().trim();

            bookCards.forEach((card) => {
                const bookDetails = card.textContent.toLowerCase();
                card.style.display = bookDetails.includes(searchTerm)
                    ? ""
                    : "none";
            });
        });
    }
});
