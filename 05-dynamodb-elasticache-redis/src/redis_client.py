import redis

from config import VALKEY_HOST, VALKEY_PORT


redis_client = redis.Redis(
    host=VALKEY_HOST,
    port=VALKEY_PORT,
    ssl=True,
    decode_responses=True,
)


def ping_cache():
    return redis_client.ping()


def get_value(key):
    return redis_client.get(key)


def set_value(key, value, ttl_seconds):
    return redis_client.setex(key, ttl_seconds, value)


def delete_value(key):
    return redis_client.delete(key)


if __name__ == "__main__":
    print(ping_cache())
