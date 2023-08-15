import os
from flask import Flask, request, jsonify
import gradio as gr
import sqlite3
import argparse
from datetime import datetime

from matplotlib import pyplot as plt

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
    # Fetch data from form
    humidity = request.form.get("humidity")
    temperature = request.form.get("temperature")

    # Validate the input data
    if not humidity or not temperature:
        return jsonify({"message": "Invalid data"}), 400

    try:
        humidity = float(humidity)
        temperature = float(temperature)
    except ValueError:
        return (
            jsonify({"message": "Invalid data values. Ensure they are numbers."}),
            400,
        )

    # Get current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert data into the database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sensor_data (date, humidity, temperature) VALUES (?, ?, ?)",
        (current_time, humidity, temperature),
    )
    conn.commit()

    return jsonify({"message": "Data added successfully"}), 201


@app.route("/data", methods=["GET"])
def get_data():
    # Fetch data from database
    data = get_all_data()

    # Convert data to JSON
    data_json = []
    for row in data:
        data_json.append(
            {
                "date": row[0],
                "humidity": row[1],
                "temperature": row[2],
            }
        )

    return jsonify(data_json), 200


@app.route("/data" + "/<start_date>" + "/<end_date>", methods=["GET"])
def data_by_range(start_date, end_date):
    # Fetch data from database
    data = get_data_by_range(start_date, end_date)

    # Convert data to JSON
    data_json = []
    for row in data:
        data_json.append(
            {
                "date": row[0],
                "humidity": row[1],
                "temperature": row[2],
            }
        )

    return jsonify(data_json), 200


def get_all_data():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT date, humidity, temperature FROM sensor_data")
    return cursor.fetchall()


def get_data_by_range(start_date, end_date):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT date, humidity, temperature FROM sensor_data WHERE date BETWEEN ? AND ?",
        (start_date, end_date),
    )
    return cursor.fetchall()


if __name__ == "__main__":
    # argparse with host, port, debug:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--online", action="store_true")
    parser.add_argument("--debug", type=bool, default=False)
    args = parser.parse_args()
    host = "0.0.0.0" if args.online else args.host
    app.run(host=host, port=args.port, debug=args.debug)
