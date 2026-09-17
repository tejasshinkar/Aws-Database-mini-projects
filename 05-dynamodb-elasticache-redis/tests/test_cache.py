from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

import json

from cache_service import build_cache_key, get_user_with_cache
from redis_client import get_value, delete_value


USER_ID = "user-1"
CACHE_KEY = build_cache_key(USER_ID)

delete_value(CACHE_KEY)

user = get_user_with_cache(USER_ID)
print(f"First read result: {user}")

cached_value = get_value(CACHE_KEY)

if cached_value:
    print("Cache populated successfully")
    print(f"Cached JSON: {json.loads(cached_value)}")
else:
    print("Cache was not populated")
