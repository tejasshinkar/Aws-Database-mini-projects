import json

from config import CACHE_TTL_SECONDS
from dynamodb_client import get_user
from redis_client import get_value, set_value, delete_value


def build_cache_key(user_id):
    return f"user:{user_id}"


def get_user_with_cache(user_id):
    cache_key = build_cache_key(user_id)

    cached_value = get_value(cache_key)

    if cached_value:
        print("Cache hit")
        return json.loads(cached_value)

    print("Cache miss")

    user = get_user(user_id)

    if user is None:
        return None

    set_value(
        cache_key,
        json.dumps(user),
        CACHE_TTL_SECONDS,
    )

    return user


def invalidate_user_cache(user_id):
    cache_key = build_cache_key(user_id)
    delete_value(cache_key)
    print("Cache invalidated")
