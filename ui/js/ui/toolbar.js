export function initToolbar({ onItems, onSales, onSearch }) {
    itemsBtn.onclick = onItems;
    salesBtn.onclick = onSales;
    searchInput.oninput = e => onSearch(e.target.value);
}
