const BASE_URL = "http://127.0.0.1:8000";

/**
 * GET /sales
 * Zwraca listę sprzedaży
 */
export async function fetchSales() {
    const res = await fetch(
        `${BASE_URL}/sales?Sort_by=SaleID&Order=desc&Limit=100&Offset=0`,
        { method: "GET" }
    );

    if (!res.ok) {
        throw new Error(`fetchSales failed: ${res.status}`);
    }

    return res.json();
}

/**
 * POST /sales/{media_id}
 * Rejestruje sprzedaż określonej ilości danego medium
 */
export async function sendSale(mediaId, amount) {
    if (!mediaId) {
        throw new Error("sendSale: missing mediaId");
    }
    if (!amount || amount < 1) {
        throw new Error("sendSale: invalid amount");
    }

    const res = await fetch(`${BASE_URL}/sales/${mediaId}`, {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            amount_sold: amount
        })
    });

    if (!res.ok) {
        throw new Error(`sendSale failed: ${res.status}`);
    }

    return res.json();
}
