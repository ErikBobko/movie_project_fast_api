"""
CONFIG MODULE

Úloha:
- načítava konfiguráciu z .env súboru
- poskytuje nastavenia pre celý projekt

Obsahuje:
- TMDB API kľúč
- Supabase URL
- Supabase API kľúč

Dôležité:
- neobsahuje business logiku
- nekomunikuje s externými službami
- neobsahuje databázové operácie

Prečo existuje:
- všetky konfigurácie sú na jednom mieste
- citlivé údaje nie sú natvrdo v kóde
"""



import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")