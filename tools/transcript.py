from datetime import datetime
from client import query_fireflies


def register(mcp):

    @mcp.tool()
    def get_meeting_notes(transcript_id: str) -> dict:
        """Get full transcript notes and action items for a specific meeting."""
        data = query_fireflies("""
            query Transcript($id: String!) {
                transcript(id: $id) {
                    id title date duration
                    sentences { speaker_name text start_time }
                    action_items { text speaker_name }
                }
            }
        """, {"id": transcript_id})
        return data["transcript"]

    @mcp.tool()
    def get_meeting_summary(transcript_id: str) -> dict:
        """Get the AI-generated summary, keywords, and action items for a meeting."""
        data = query_fireflies("""
            query Transcript($id: String!) {
                transcript(id: $id) {
                    id title date
                    summary {
                        keywords action_items outline
                        shorthand_bullet overview bullet_gist gist short_summary
                    }
                }
            }
        """, {"id": transcript_id})
        return data["transcript"]

    @mcp.tool()
    def export_transcript_markdown(transcript_id: str) -> str:
        """Export a full meeting transcript as a formatted Markdown string."""
        data = query_fireflies("""
            query Transcript($id: String!) {
                transcript(id: $id) {
                    title date duration
                    summary { short_summary action_items keywords }
                    sentences { speaker_name text start_time }
                }
            }
        """, {"id": transcript_id})
        t = data["transcript"]

        date_str = datetime.fromtimestamp(t["date"] / 1000).strftime("%Y-%m-%d %H:%M") if t.get("date") else "N/A"
        lines = [
            f"# {t['title']}",
            f"**Date:** {date_str}  |  **Duration:** {round(t.get('duration', 0) / 60, 1)} mins",
            "",
        ]

        summary = t.get("summary") or {}
        if summary.get("short_summary"):
            lines += ["## Summary", summary["short_summary"], ""]
        if summary.get("keywords"):
            lines += ["## Keywords", ", ".join(summary["keywords"]), ""]
        if summary.get("action_items"):
            lines += ["## Action Items"] + [f"- {i}" for i in summary["action_items"]] + [""]

        lines.append("## Transcript")
        for s in t.get("sentences", []):
            mins, secs = divmod(round(s.get("start_time", 0) / 1000), 60)
            lines.append(f"**[{mins:02d}:{secs:02d}] {s['speaker_name']}:** {s['text']}")

        return "\n".join(lines)
