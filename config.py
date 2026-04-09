import os
from dotenv import load_dotenv

load_dotenv()

FIREFLIES_API_KEY = os.getenv("FIREFLIES_API_KEY")
FIREFLIES_API_URL = "https://api.fireflies.ai/graphql"
