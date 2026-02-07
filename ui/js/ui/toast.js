let timeoutId = null;

export function showError(message) {
    const toast = document.getElementById("toast");
    if (!toast) return;

    toast.textContent = message;
    toast.hidden = false;
    toast.classList.add("show");

    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
        toast.classList.remove("show");
        toast.hidden = true;
    }, 3000);
}
