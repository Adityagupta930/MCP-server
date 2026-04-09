from tools import meetings, transcript, analytics, user


def register_all(mcp):
    meetings.register(mcp)
    transcript.register(mcp)
    analytics.register(mcp)
    user.register(mcp)
