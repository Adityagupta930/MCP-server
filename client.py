import httpx
from config import FIREFLIES_API_KEY, FIREFLIES_API_URL


def query_fireflies(query: str, variables: dict = None) -> dict:
    headers = {
        "Authorization": f"Bearer {FIREFLIES_API_KEY}",
        "Content-Type": "application/json",
    }
    response = httpx.post(
        FIREFLIES_API_URL,
        json={"query": query, "variables": variables or {}},
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    if "errors" in data:
        raise ValueError(f"Fireflies API error: {data['errors']}")
    return data["data"]
