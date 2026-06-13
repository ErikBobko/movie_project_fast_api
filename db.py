"""
DATABASE MODULE

Úloha:
- vytvára spojenie so Supabase databázou
- poskytuje jednoduchý prístup k databáze pre celý projekt

Použitie:
- ukladanie filmov do DB
- čítanie filmov z DB
- kontrola existencie záznamov

Prečo existuje:
- aby DB logika nebola v každom súbore
- aby všetky operácie s databázou boli centralizované
- aby sa dal ľahko meniť DB provider (napr. Supabase → iná DB)
"""


from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
