import { fetchSales } from "../api/salesApi.js";
import { renderTable } from "../ui/table.js";
import { state } from "../state.js";

/**
 * Główny entrypoint widoku SALES
 * - pobiera sprzedaże
 * - mapuje title z media_id
 * - renderuje tabelę
 */
export async function loadSalesView() {
    state.currentView = "sales";

    try {
        const data = await fetchSales();

        const sales = data.items ?? [];

        state.allSales = sales.map(sale => ({
            ...sale,
            title: state.mediaTitleMap[sale.media_id] ?? "(unknown title)"
        }));

        renderTable({
            view: "sales",
            rows: state.allSales
        });

    } catch (err) {
        console.error("Błąd ładowania sales:", err);
    }
}
