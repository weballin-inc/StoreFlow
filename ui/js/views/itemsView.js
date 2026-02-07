import { fetchMedia } from "../api/mediaApi.js";
import { renderTable } from "../ui/table.js";
import { openSellPanel, openUpdatePanel } from "../ui/panels.js";
import { state } from "../state.js";

/**
 * Główny entrypoint widoku ITEMS
 * - pobiera dane
 * - aktualizuje stan
 * - renderuje tabelę
 */
export async function loadItemsView() {
    state.currentView = "items";

    try {
        const data = await fetchMedia();

        state.allItems = data.items ?? [];

        // pomocnicza mapa id -> title (używana później w salesView)
        state.mediaTitleMap = {};
        state.allItems.forEach(item => {
            state.mediaTitleMap[item.id] = item.title;
        });

        renderTable({
            view: "items",
            rows: state.allItems,
            onSell: handleSell,
            onUpdate: handleUpdate
        });

    } catch (err) {
        console.error("Błąd ładowania items:", err);
        showError("Nie udało się pobrać listy items");
    }
}

/* ================== HANDLERS ================== */

function handleSell(item) {
    openSellPanel(item);
}

function handleUpdate(item) {
    openUpdatePanel(item);
}
