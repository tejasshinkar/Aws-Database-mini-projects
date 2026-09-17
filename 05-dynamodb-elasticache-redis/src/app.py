from cache_service import get_user_with_cache
from dynamodb_client import put_user


def main():
    put_user(
        user_id="user-1",
        name="Tejas Updated",
        email="updated@example.com",
    )
    print("User inserted successfully")

    user = get_user_with_cache("user-1")
    print(f"Result: {user}")


if __name__ == "__main__":
    main()
