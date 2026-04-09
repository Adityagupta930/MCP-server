from client import query_fireflies


def register(mcp):

    @mcp.tool()
    def get_speakers(transcript_id: str) -> list[dict]:
        """Get all speakers in a meeting with their word count and sentence count."""
        data = query_fireflies("""
            query Transcript($id: String!) {
                transcript(id: $id) {
                    sentences { speaker_name text }
                }
            }
        """, {"id": transcript_id})

        stats: dict[str, dict] = {}
        for s in data["transcript"].get("sentences", []):
            name = s["speaker_name"] or "Unknown"
            stats.setdefault(name, {"speaker": name, "word_count": 0, "sentence_count": 0})
            stats[name]["word_count"] += len(s["text"].split())
            stats[name]["sentence_count"] += 1
        return list(stats.values())

    @mcp.tool()
    def get_meeting_analytics(transcript_id: str) -> dict:
        """Get talk-time analytics: who spoke the most, word counts, and participation %."""
        data = query_fireflies("""
            query Transcript($id: String!) {
                transcript(id: $id) {
                    title duration
                    sentences { speaker_name text start_time end_time }
                }
            }
        """, {"id": transcript_id})
        t = data["transcript"]

        stats: dict[str, dict] = {}
        total_words = 0
        for s in t.get("sentences", []):
            name = s["speaker_name"] or "Unknown"
            words = len(s["text"].split())
            talk_time = (s.get("end_time", 0) - s.get("start_time", 0)) / 1000
            stats.setdefault(name, {"speaker": name, "word_count": 0, "talk_time_seconds": 0, "sentence_count": 0})
            stats[name]["word_count"] += words
            stats[name]["talk_time_seconds"] += talk_time
            stats[name]["sentence_count"] += 1
            total_words += words

        for v in stats.values():
            v["participation_pct"] = round((v["word_count"] / total_words * 100) if total_words else 0, 1)
            v["talk_time_seconds"] = round(v["talk_time_seconds"], 1)

        return {
            "meeting_title": t["title"],
            "total_duration_mins": round(t.get("duration", 0) / 60, 1),
            "total_words": total_words,
            "speakers": sorted(stats.values(), key=lambda x: x["word_count"], reverse=True),
        }

    @mcp.tool()
    def get_all_action_items(limit: int = 20) -> list[dict]:
        """Get action items from all recent meetings in one place."""
        data = query_fireflies("""
            query Transcripts($limit: Int) {
                transcripts(limit: $limit) {
                    id title date
                    action_items { text speaker_name }
                }
            }
        """, {"limit": limit})
        return [
            {"meeting_id": t["id"], "meeting_title": t["title"], "date": t["date"], "action_items": t["action_items"]}
            for t in data["transcripts"] if t.get("action_items")
        ]
