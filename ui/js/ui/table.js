const tableHead = document.getElementById("table_head");
const tbody = document.querySelector("#items tbody");

/* ================== PUBLIC API ================== */

export function renderTable({ view, rows, onSell, onUpdate }) {
    renderHeader(view);
    renderBody(view, rows, onSell, onUpdate);
}

/* ================== HEADERS ================== */

function renderHeader(view) {
    if (view === "items") {
        tableHead.innerHTML = `
            <tr>
                <th>Title</th>
                <th>Type</th>
                <th>Year</th>
                <th>Publisher</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Edit</th>
            </tr>
        `;
    }

    if (view === "sales") {
        tableHead.innerHTML = `
            <tr>
                <th>Title</th>
                <th>Price</th>
                <th>Date</th>
            </tr>
        `;
    }
}

/* ================== BODY ================== */

function renderBody(view, rows, onSell, onUpdate) {
    tbody.innerHTML = "";

    if (view === "items") {
        rows.forEach(item => {
            const tr = document.createElement("tr");

            tr.innerHTML = `
                <td>${item.title}</td>
                <td>${item.media_type}</td>
                <td>${item.release_year}</td>
                <td>${item.publisher}</td>
                <td>${item.quantity}</td>
                <td>${item.price}</td>
                <td>
                    <button class="sell-btn">Sell</button>
                    <button class="update-btn">Update</button>
                </td>
            `;

            tr.querySelector(".sell-btn")
                .addEventListener("click", () => onSell(item));

            tr.querySelector(".update-btn")
                .addEventListener("click", () => onUpdate(item));

            tbody.appendChild(tr);
        });
    }

    if (view === "sales") {
        rows.forEach(sale => {
            const tr = document.createElement("tr");

            tr.innerHTML = `
                <td>${sale.title}</td>
                <td>${sale.price}</td>
                <td>${formatDate(sale.date)}</td>
            `;

            tbody.appendChild(tr);
        });
    }
}

/* ================== HELPERS ================== */

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleString("sv-SE", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false
    });
}
