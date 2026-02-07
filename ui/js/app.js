import { state } from "./state.js";
import { loadItemsView } from "./views/itemsView.js";
import { loadSalesView } from "./views/salesView.js";
import { initToolbar } from "./ui/toolbar.js";
import { renderTable } from "./ui/table.js";
import { openSellPanel, openUpdatePanel, openCreatePanel } from "./ui/panels.js";

document.addEventListener("DOMContentLoaded", () => {

    initToolbar({
        onItems: async () => {
            await loadItemsView();
        },

        onSales: async () => {
            await loadSalesView();
        },

        onAdd: openCreatePanel,

        onSearch: query => {
            state.searchQuery = query;

            if (state.currentView === "items") {
                const filtered = state.allItems.filter(item =>
                    item.title.toLowerCase().includes(query)
                );

                renderTable({
                    view: "items",
                    rows: filtered,
                    onSell: openSellPanel,
                    onUpdate: openUpdatePanel
                });
            }

            if (state.currentView === "sales") {
                const filtered = state.allSales.filter(sale =>
                    sale.title.toLowerCase().includes(query)
                );

                renderTable({
                    view: "sales",
                    rows: filtered
                });
            }
        }
    });

    // start aplikacji
    loadItemsView();
});
