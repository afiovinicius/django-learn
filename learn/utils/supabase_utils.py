# Imports Python
import os
from dotenv import load_dotenv


load_dotenv()

# Import Supabase
from supabase.client import create_client


def supabase_connect():
    url: str = os.getenv("SUPABASE_URL", default="SUPABASE_URL")

    key: str = os.getenv("SUPABASE_KEY", default="SUPABASE_KEY")
    create_client(url, key)

    return create_client(url, key)
