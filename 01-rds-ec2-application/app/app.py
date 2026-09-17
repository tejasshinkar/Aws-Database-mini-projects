import os
import re

import pymysql
from dotenv import load_dotenv
from flask import Flask, request, render_template

load_dotenv()

app = Flask(__name__)


def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.Cursor
    )


def is_valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    users = []
    connection = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        if not name or not email:
            message = "Name and email are required."

        elif len(name) > 100:
            message = "Name must be 100 characters or fewer."

        elif len(email) > 150 or not is_valid_email(email):
            message = "Please enter a valid email address."

        else:
            try:
                connection = get_db_connection()

                with connection.cursor() as cursor:
                    sql = """
                        INSERT INTO users (name, email)
                        VALUES (%s, %s)
                    """
                    cursor.execute(sql, (name, email))

                connection.commit()
                message = "User saved successfully!"

            except Exception:
                if connection:
                    connection.rollback()

                app.logger.exception("Database operation failed")
                message = "Unable to save user. Please try again."

            finally:
                if connection:
                    connection.close()

    connection = None

    try:
        connection = get_db_connection()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, email, created_at
                FROM users
                ORDER BY id DESC
            """)
            users = cursor.fetchall()

    except Exception:
        app.logger.exception("Failed to retrieve users")
        if not message:
            message = "Unable to retrieve users."

    finally:
        if connection:
            connection.close()

    return render_template(
        "index.html",
        message=message,
        users=users
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
