# Flask SQLite3 Sensor Data Application

This Flask application receives sensor data (**humidity and temperature**) through an API endpoint and stores it in an SQLite3 database.

## Setup & Installation

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-dir>
```

### 2. Set up a Virtual Environment

To isolate your project and its dependencies, it's recommended to use a virtual environment. Here's how you can set it up:

```bash
# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS and Linux:
source venv/bin/activate
```

### 3. Install Dependencies

Install the required packages using pip:

```bash
pip install Flask
```

### 4. Run the Application

With the virtual environment activated:

```bash
python app.py
```

Your Flask application should now be running on `http://127.0.0.1:5000/`.

## API Endpoints

### Add Sensor Data

- **Endpoint:** `/add_data`
- **Method:** `POST`
- **Data:** JSON with fields `humidity` and `temperature`.
  Example:
  ```json
  {
    "humidity": 54,
    "temperature": 28
  }
  ```

## Contributing

If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcomed.

---

You can adapt the README to fit any other specific instructions or details you'd like to include.
