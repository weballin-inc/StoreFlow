import { state } from "../state.js";
import { sendSale } from "../api/salesApi.js";
import { updateMedia } from "../api/mediaApi.js";
import { loadItemsView } from "../views/itemsView.js";
import { showError } from "./toast.js";

/* ================== DOM ================== */

const updatePanel = document.getElementById("updatePanel");
const closePanelBtn = document.getElementById("closePanel");
const sendSaleBtn = document.getElementById("sendSale");
const sellAmountInput = document.getElementById("sellAmount");

const pTitle = document.getElementById("p_title");
const pType = document.getElementById("p_type");
const pYear = document.getElementById("p_year");
const pPublisher = document.getElementById("p_publisher");
const pQuantity = document.getElementById("p_quantity");
const pPrice = document.getElementById("p_price");

const updateFields = document.getElementById("updateFields");

const editTitle = document.getElementById("edit_title");
const editType = document.getElementById("edit_type");
const editYear = document.getElementById("edit_year");
const editPublisher = document.getElementById("edit_publisher");
const editQuantity = document.getElementById("edit_quantity");
const editPrice = document.getElementById("edit_price");

const saveUpdateBtn = document.getElementById("saveUpdate");

/* ================== HELPERS ================== */

function openPanel() {
    updatePanel.classList.add("open");
}

function closePanel() {
    updatePanel.classList.remove("open");
    state.panelMode = null;
    state.selectedItemId = null;
}

/* ================== SELL ================== */

export function openSellPanel(item) {
    state.panelMode = "SELL";
    state.selectedItemId = item.id;

    pTitle.textContent = item.title;
    pType.textContent = item.media_type;
    pYear.textContent = item.release_year;
    pPublisher.textContent = item.publisher;
    pQuantity.textContent = item.quantity;
    pPrice.textContent = item.price;

    sellAmountInput.value = 1;
    sellAmountInput.max = item.quantity;

    updateFields.style.display = "none";
    sendSaleBtn.style.display = "block";
    sellAmountInput.parentElement.style.display = "block";

    openPanel();
}

/* ================== UPDATE ================== */

export function openUpdatePanel(item) {
    state.panelMode = "UPDATE";
    state.selectedItemId = item.id;

    editTitle.value = item.title;
    editType.value = item.media_type;
    editYear.value = item.release_year;
    editPublisher.value = item.publisher;
    editQuantity.value = item.quantity;
    editPrice.value = item.price;

    updateFields.style.display = "block";
    sendSaleBtn.style.display = "none";
    sellAmountInput.parentElement.style.display = "none";

    openPanel();
}

/* ================== ACTIONS ================== */

sendSaleBtn.addEventListener("click", async () => {
    if (state.panelMode !== "SELL") return;

    const amount = Number(sellAmountInput.value);
    if (!amount || amount < 1) return;

    try {
        await sendSale(state.selectedItemId, amount);
        closePanel();
        await loadItemsView();
    } catch (err) {
        console.error("Błąd sprzedaży:", err);
        showError("Nie udało się zapisać zmian");
    }
});

saveUpdateBtn.addEventListener("click", async () => {
    if (state.panelMode !== "UPDATE") return;

    const payload = {
        title: editTitle.value,
        media_type: editType.value,
        release_year: Number(editYear.value),
        publisher: editPublisher.value,
        quantity: Number(editQuantity.value),
        price: Number(editPrice.value)
    };

    try {
        await updateMedia(state.selectedItemId, payload);
        closePanel();
        await loadItemsView();
    } catch (err) {
        console.error("Błąd aktualizacji:", err);
        showError("Nie udało się zapisać zmian");
    }
});

/* ================== CLOSE ================== */

closePanelBtn.addEventListener("click", closePanel);
