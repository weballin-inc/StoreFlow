export async function fetchSales() {
    const res = await fetch("http://127.0.0.1:8000/sales?Sort_by=SaleID&Order=desc&Limit=100&Offset=0");
    return res.json();
}

export async function sendSale(id, amount) {
    return fetch(`http://127.0.0.1:8000/sales/${id}`, {
        method: "POST",
        headers: {
            "accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ amount_sold: amount })
    });
}
