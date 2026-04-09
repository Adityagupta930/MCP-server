# Fireflies MCP Server

An MCP (Model Context Protocol) server that connects AI assistants to the [Fireflies.ai](https://fireflies.ai) API, enabling them to access meeting transcripts, summaries, analytics, and more.

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   Add your Fireflies API key to `.env`:
   ```
   FIREFLIES_API_KEY=your_fireflies_api_key_here
   ```
   Get your API key from [Fireflies Settings](https://app.fireflies.ai/integrations/custom/fireflies).

3. **Run the server**
   ```bash
   python server.py
   ```

## Tools

### Meetings
| Tool | Description |
|------|-------------|
| `list_meetings(limit)` | List recent recorded meetings |
| `search_meetings(query_text)` | Search meetings by keyword |
| `get_meetings_by_date(start_date, end_date)` | Filter meetings by date range (`YYYY-MM-DD`) |

### Transcripts
| Tool | Description |
|------|-------------|
| `get_meeting_notes(transcript_id)` | Get full transcript and action items |
| `get_meeting_summary(transcript_id)` | Get AI-generated summary, keywords, and action items |
| `export_transcript_markdown(transcript_id)` | Export transcript as formatted Markdown |

### Analytics
| Tool | Description |
|------|-------------|
| `get_speakers(transcript_id)` | Get speakers with word and sentence counts |
| `get_meeting_analytics(transcript_id)` | Get talk-time, participation %, and word counts per speaker |
| `get_all_action_items(limit)` | Aggregate action items from recent meetings |

### User
| Tool | Description |
|------|-------------|
| `get_user_info()` | Get Fireflies account info |
| `add_bot_to_meeting(meeting_url, title)` | Add Fireflies bot to a live meeting |

## Project Structure

```
├── server.py         # MCP server entry point
├── client.py         # Fireflies GraphQL client
├── config.py         # Environment config
├── tools/
│   ├── meetings.py   # Meeting listing and search tools
│   ├── transcript.py # Transcript and summary tools
│   ├── analytics.py  # Speaker analytics tools
│   └── user.py       # User and bot management tools
└── requirements.txt
```

## License

See [LICENSE](LICENSE).
