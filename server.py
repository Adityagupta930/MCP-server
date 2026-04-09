import os
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

FIREFLIES_API_KEY = os.getenv("FIREFLIES_API_KEY")
FIREFLIES_API_URL = "https://api.fireflies.ai/graphql"

mcp = FastMCP("fireflies-mcp")

def query_fireflies(query: str, variables: dict = None):
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


@mcp.tool()
def list_meetings(limit: int = 10) -> list[dict]:
    """List recent Google Meet meetings recorded by Fireflies."""
    query = """
    query Transcripts($limit: Int) {
        transcripts(limit: $limit) {
            id
            title
            date
            duration
            meeting_link
            organizer_email
        }
    }
    """
    data = query_fireflies(query, {"limit": limit})
    return data["transcripts"]


@mcp.tool()
def get_meeting_notes(transcript_id: str) -> dict:
    """Get full transcript notes and action items for a specific meeting."""
    query = """
    query Transcript($id: String!) {
        transcript(id: $id) {
            id
            title
            date
            duration
            sentences {
                speaker_name
                text
                start_time
            }
            action_items {
                text
                speaker_name
            }
        }
    }
    """
    data = query_fireflies(query, {"id": transcript_id})
    return data["transcript"]


@mcp.tool()
def get_meeting_summary(transcript_id: str) -> dict:
    """Get the AI-generated summary, keywords, and action items for a meeting."""
    query = """
    query Transcript($id: String!) {
        transcript(id: $id) {
            id
            title
            date
            summary {
                keywords
                action_items
                outline
                shorthand_bullet
                overview
                bullet_gist
                gist
                short_summary
            }
        }
    }
    """
    data = query_fireflies(query, {"id": transcript_id})
    return data["transcript"]


@mcp.tool()
def search_meetings(query_text: str) -> list[dict]:
    """Search across all meeting transcripts by keyword."""
    query = """
    query SearchTranscripts($query: String!) {
        transcripts(query: $query) {
            id
            title
            date
            meeting_link
        }
    }
    """
    data = query_fireflies(query, {"query": query_text})
    return data["transcripts"]


if __name__ == "__main__":
    mcp.run()
