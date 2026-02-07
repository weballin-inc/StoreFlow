/**
 * Inicjalizacja toolbaru
 * @param {Object} handlers
 * @param {Function} handlers.onItems
 * @param {Function} handlers.onSales
 * @param {Function} handlers.onSearch
 */
export function initToolbar({ onItems, onSales, onSearch }) {
    const itemsBtn = document.getElementById("items_button");
    const salesBtn = document.getElementById("sales_button");
    const searchInput = document.getElementById("searchInput");

    if (!itemsBtn || !salesBtn || !searchInput) {
        throw new Error("Toolbar DOM elements not found");
    }

    itemsBtn.addEventListener("click", () => {
        onItems();
    });

    salesBtn.addEventListener("click", () => {
        onSales();
    });

    searchInput.addEventListener("input", e => {
        const value = e.target.value.toLowerCase();
        onSearch(value);
    });
}
