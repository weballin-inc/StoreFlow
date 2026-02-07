export async function fetchMedia() {
    const res = await fetch("http://127.0.0.1:8000/media?Order=asc&Limit=100&Offset=0");
    return res.json();
}

export async function updateMedia(id, payload) {
    return fetch(`http://127.0.0.1:8000/media/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
}
