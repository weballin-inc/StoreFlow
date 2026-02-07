export const state = {
    // aktualny widok
    currentView: "items",

    // dane
    allItems: [],
    allSales: [],
    mediaTitleMap: {},

    // UI / interakcje
    searchQuery: "",

    // panele
    selectedItemId: null,
    panelMode: null // "SELL" | "UPDATE"
};
