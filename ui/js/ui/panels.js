/* ------------------ PANEL SELL ------------------ */
function openSellPanel(item) {
    panelMode = "SELL";          // <-- DODANE
    selectedItemId = item.id;

    pTitle.textContent = item.title;
    pType.textContent = item.media_type;
    pYear.textContent = item.release_year;
    pPublisher.textContent = item.publisher;
    pQuantity.textContent = item.quantity;
    pPrice.textContent = item.price;

    sellAmountInput.value = 1;
    sellAmountInput.max = item.quantity;

    // <-- DODANE: ukryj UPDATE, pokaz SELL
    updateFields.style.display = "none";
    sendSaleBtn.style.display = "inline-block";
    sellAmountInput.parentElement.style.display = "block";

    updatePanel.classList.add("open");

    closePanelBtn.onclick = () => {
        updatePanel.classList.remove("open");
    };
}

/* ------------------ PANEL UPDATE ------------------ */
function openUpdatePanel(item) {
    panelMode = "UPDATE";        // <-- DODANE
    selectedItemId = item.id;

    editTitle.value = item.title;
    editType.value = item.media_type;
    editYear.value = item.release_year;
    editPublisher.value = item.publisher;
    editQuantity.value = item.quantity;
    editPrice.value = item.price;

    // <-- DODANE: pokaz UPDATE, ukryj SELL
    updateFields.style.display = "block";
    sendSaleBtn.style.display = "none";
    sellAmountInput.parentElement.style.display = "none";

    updatePanel.classList.add("open");

    saveUpdateBtn.onclick = () => {
        updatePanel.classList.remove("open");
    };
}