from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from cache_service import get_user_with_cache, invalidate_user_cache
from dynamodb_client import put_user, update_user

USER_ID = "user-1"

put_user(USER_ID, "Tejas", "tejas@example.com")
print("User inserted successfully")

before_update = get_user_with_cache(USER_ID)
print(f"Before update: {before_update}")

update_user(USER_ID, "Tejas Updated", "updated@example.com")
print("User updated successfully")

invalidate_user_cache(USER_ID)

after_update = get_user_with_cache(USER_ID)
print(f"After update: {after_update}")
