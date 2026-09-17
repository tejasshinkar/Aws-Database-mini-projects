from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from cache_service import build_cache_key, get_user_with_cache, invalidate_user_cache
from redis_client import get_value

USER_ID = "user-1"
CACHE_KEY = build_cache_key(USER_ID)

user = get_user_with_cache(USER_ID)
print(f"Before invalidation: {user}")

invalidate_user_cache(USER_ID)

remaining_value = get_value(CACHE_KEY)
print(f"After invalidation: {remaining_value}")
