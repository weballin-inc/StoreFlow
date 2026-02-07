/* ------------------ NAGLOWKI ------------------ */
function renderItemsHeader() {
    tableHead.innerHTML = `
            <tr>
                <th>Title</th>
                <th>
                    Type
                    <select id="typeFilter">
                        <option value="ALL">ALL</option>
                        <option value="GAME">GAME</option>
                        <option value="BOOK">BOOK</option>
                    </select>
                </th>
                <th>Release Year</th>
                <th>Publisher</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Edit record</th>
            </tr>
        `;

    const select = document.getElementById("typeFilter");
    select.value = typeFilter;

    select.onchange = e => {
        typeFilter = e.target.value;
        renderFilteredTable();
    };
}

function renderSalesHeader() {
    tableHead.innerHTML = `
            <tr>
                <th>Title</th>
                <th>Price</th>
                <th id="dateSort" style="cursor:pointer">
                    Date ${dateSortOrder === "asc" ? "▲" : "▼"}
                </th>
            </tr>
        `;

    document.getElementById("dateSort").onclick = () => {
        dateSortOrder = dateSortOrder === "asc" ? "desc" : "asc";
        renderFilteredTable();
    };
}

/* ------------------ RENDER Z FILTREM ------------------ */
function renderFilteredTable() {
    tbody.innerHTML = "";

    if (currentView === "items") {
        let rows = allItems;

        if (typeFilter !== "ALL") {
            rows = rows.filter(item => item.media_type === typeFilter);
        }

        if (searchQuery) {
            rows = rows.filter(item =>
                item.title.toLowerCase().includes(searchQuery)
            );
        }

        rows.forEach(item => {
            tbody.insertAdjacentHTML("beforeend", `
                    <tr>
                        <td>${item.title}</td>
                        <td>${item.media_type}</td>
                        <td>${item.release_year}</td>
                        <td>${item.publisher}</td>
                        <td>${item.quantity}</td>
                        <td>${item.price}</td>
                        <td>
                            <button onclick='openSellPanel(${JSON.stringify(item)})'>
                                Sell
                            </button>
                            <button onclick='openUpdatePanel(${JSON.stringify(item)})'>
                                Update
                            </button>
                        </td>
                    </tr>
                `);
        });
    }

    if (currentView === "sales") {
        let rows = allSales;

        if (searchQuery) {
            rows = rows.filter(sale =>
                sale.date.toLowerCase().includes(searchQuery)
            );
        }

        rows.sort((a, b) => {
            const A = new Date(a.date);
            const B = new Date(b.date);
            return dateSortOrder === "asc" ? A - B : B - A;
        });

        rows.forEach(sale => {
            tbody.insertAdjacentHTML("beforeend", `
                    <tr>
                        <td>${sale.title}</td>
                        <td>${sale.price}</td>
                        <td>${new Date(sale.date).toLocaleString("sv-SE", {
                year: "numeric",
                month: "2-digit",
                day: "2-digit",
                hour: "2-digit",
                minute: "2-digit",
                hour12: false
            })}</td>
                    </tr>
                `);
        });
    }
}