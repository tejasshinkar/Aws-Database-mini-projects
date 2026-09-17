from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from cache_service import get_user_with_cache, invalidate_user_cache
from dynamodb_client import delete_user

USER_ID = "user-1"

before_deletion = get_user_with_cache(USER_ID)
print(f"Before deletion: {before_deletion}")

delete_user(USER_ID)
print("User deleted successfully")

invalidate_user_cache(USER_ID)

after_deletion = get_user_with_cache(USER_ID)
print(f"After deletion: {after_deletion}")
