import os
from dotenv import load_dotenv

load_dotenv()

MIMO_API_KEY = os.getenv("MIMO_API_KEY", "")
MIMO_BASE_URL = os.getenv("MIMO_BASE_URL", "https://token-plan-cn.xiaomimimo.com/v1")
MIMO_MODEL = os.getenv("MIMO_MODEL", "mimo-v2.5")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/silverage.db")
