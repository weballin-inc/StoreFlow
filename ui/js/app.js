import { loadItemsView } from "./views/itemsView.js";
import { loadSalesView } from "./views/salesView.js";
import { initToolbar } from "./ui/toolbar.js";

document.addEventListener("DOMContentLoaded", () => {
    initToolbar({
        onItems: loadItemsView,
        onSales: loadSalesView,
        onSearch: q => { /* update state + render */ }
    });

    loadItemsView();
});
