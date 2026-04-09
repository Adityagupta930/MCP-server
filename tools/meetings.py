from datetime import datetime
from client import query_fireflies


def register(mcp):

    @mcp.tool()
    def list_meetings(limit: int = 10) -> list[dict]:
        """List recent Google Meet meetings recorded by Fireflies."""
        data = query_fireflies("""
            query Transcripts($limit: Int) {
                transcripts(limit: $limit) {
                    id title date duration meeting_link organizer_email
                }
            }
        """, {"limit": limit})
        return data["transcripts"]

    @mcp.tool()
    def search_meetings(query_text: str) -> list[dict]:
        """Search across all meeting transcripts by keyword."""
        data = query_fireflies("""
            query SearchTranscripts($query: String!) {
                transcripts(query: $query) {
                    id title date meeting_link
                }
            }
        """, {"query": query_text})
        return data["transcripts"]

    @mcp.tool()
    def get_meetings_by_date(start_date: str, end_date: str) -> list[dict]:
        """
        Filter meetings between a date range.
        Date format: YYYY-MM-DD  e.g. start_date='2024-01-01', end_date='2024-12-31'
        """
        start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)
        end_ts = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000)
        data = query_fireflies("""
            query Transcripts($fromDate: Float, $toDate: Float) {
                transcripts(fromDate: $fromDate, toDate: $toDate) {
                    id title date duration meeting_link organizer_email
                }
            }
        """, {"fromDate": start_ts, "toDate": end_ts})
        return data["transcripts"]
