import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

# Create a Supabase client
if not SUPABASE_URL or not SUPABASE_KEY:
    # App can still run without Supabase for local testing,
    # but saving scores will no-op.
    supabase = None
else:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
