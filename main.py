from flask import Flask, request, jsonify
import sqlite3
import argparse
from datetime import datetime

app = Flask(__name__)

DATABASE_NAME = "sensor_data.db"


# Create SQLite DB file if not exists and connect:
def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        # Create table if not exists
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            humidity REAL NOT NULL,
            temperature REAL NOT NULL
        )
        """
        )

        db.commit()


# Call the function to ensure the database table is created
init_db()


@app.route("/add_data", methods=["POST"])
def add_data():
    data = request.get_json()

    # Validate the input data
    if not data or "humidity" not in data or "temperature" not in data:
        return jsonify({"message": "Invalid data"}), 400

    # Get current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert data into the database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sensor_data (date, humidity, temperature) VALUES (?, ?, ?)",
        (current_time, data["humidity"], data["temperature"]),
    )
    conn.commit()

    return jsonify({"message": "Data added successfully"}), 201


if __name__ == "__main__":
    # argparse with host, port, debug:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost")  # host "192.168.2.132"
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--online", type=bool, default=False)
    parser.add_argument("--debug", type=bool, default=False)
    args = parser.parse_args()
    host = "0.0.0.0" if args.online else args.host
    app.run(host=host, port=args.port, debug=args.debug)
