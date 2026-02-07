const BASE_URL = "http://127.0.0.1:8000";

/**
 * GET /media
 * Zwraca listę wszystkich materiałów
 */
export async function fetchMedia() {
    const res = await fetch(
        `${BASE_URL}/media?Sort_by=MediaID&Order=desc&Limit=20&Offset=0`,
        { method: "GET" }
    );

    if (!res.ok) {
        throw new Error(`fetchMedia failed: ${res.status}`);
    }

    return res.json();
}

/**
 * PUT /media/{id}
 * Aktualizuje pojedynczy rekord
 */
export async function updateMedia(id, payload) {
    if (!id) {
        throw new Error("updateMedia: missing id");
    }

    const res = await fetch(`${BASE_URL}/media/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    if (!res.ok) {
        throw new Error(`updateMedia failed: ${res.status}`);
    }

    return res.json();
}

/**
 * POST /media
 * Tworzy nowy rekord dla Items
 */
export async function createMedia(payload) {
    const res = await fetch(`${BASE_URL}/media`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify([payload])
    });

    if (!res.ok) {
        await handleErrorResponse(res);
    }

    return res.json();
}
