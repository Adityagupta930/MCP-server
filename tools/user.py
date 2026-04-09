from client import query_fireflies


def register(mcp):

    @mcp.tool()
    def get_user_info() -> dict:
        """Get current Fireflies account/user information."""
        data = query_fireflies("""
            query {
                user {
                    user_id email name
                    num_transcripts minutes_consumed is_admin
                }
            }
        """)
        return data["user"]

    @mcp.tool()
    def add_bot_to_meeting(meeting_url: str, title: str = "My Meeting") -> dict:
        """Add Fireflies bot to a live Google Meet so it can record and transcribe."""
        data = query_fireflies("""
            mutation AddToLiveMeeting($url: String!, $title: String) {
                addToLiveMeeting(meeting_url: $url, title: $title) {
                    success
                    message
                }
            }
        """, {"url": meeting_url, "title": title})
        return data["addToLiveMeeting"]
