from flask import Flask, render_template_string
import sqlite3
import os

app = Flask(__name__)

# File names for our simulated databases
LOCAL_DB = 'local.db'
CLOUD_DB = 'cloud.db'

# Sample dataset for vocational courses
courses_data = [
    (1, "Carpentry Basics", "Learn basic woodworking skills, including safe tool use.", "3 months", 150.00, "Local Workshop"),
    (2, "Electrical Wiring Fundamentals", "Understand safe electrical practices and wiring techniques.", "2 months", 200.00, "Tech Institute")
]

def init_db(db_path):
    """Initialize the SQLite database and create the 'courses' table if it doesn't exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            course_name TEXT NOT NULL,
            description TEXT,
            duration TEXT,
            cost REAL,
            provider TEXT
        )
    """)
    conn.commit()
    return conn

def insert_data(conn, data):
    """Insert sample data into the 'courses' table if it is empty."""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM courses")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.executemany("""
            INSERT INTO courses (id, course_name, description, duration, cost, provider)
            VALUES (?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()

def get_courses(conn):
    """Retrieve all courses from a given database connection."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses ORDER BY id")
    return cursor.fetchall()

# Initialize and populate local database
local_conn = init_db(LOCAL_DB)
insert_data(local_conn, courses_data)
local_conn.close()

# Initialize and populate cloud database
cloud_conn = init_db(CLOUD_DB)
insert_data(cloud_conn, courses_data)  # In a real sync, this would come from local DB changes.
cloud_conn.close()

@app.route('/')
def index():
    # Connect to both databases and retrieve data
    local_conn = sqlite3.connect(LOCAL_DB)
    cloud_conn = sqlite3.connect(CLOUD_DB)
    local_courses = get_courses(local_conn)
    cloud_courses = get_courses(cloud_conn)
    local_conn.close()
    cloud_conn.close()
    
    # A simple HTML template with two side-by-side tables
    html = """
    <!doctype html>
    <html lang="en">
      <head>
        <title>Vocational Courses Data</title>
        <style>
            table, th, td {
              border: 1px solid black;
              border-collapse: collapse;
            }
            th, td {
              padding: 8px;
            }
            .container {
              display: flex;
              justify-content: space-around;
            }
            .table-container {
              margin: 20px;
            }
        </style>
      </head>
      <body>
        <h1>Vocational Courses Data</h1>
        <div class="container">
          <div class="table-container">
            <h2>Local Database</h2>
            <table>
              <tr>
                <th>ID</th>
                <th>Course Name</th>
                <th>Description</th>
                <th>Duration</th>
                <th>Cost</th>
                <th>Provider</th>
              </tr>
              {% for course in local_courses %}
              <tr>
                <td>{{ course[0] }}</td>
                <td>{{ course[1] }}</td>
                <td>{{ course[2] }}</td>
                <td>{{ course[3] }}</td>
                <td>{{ course[4] }}</td>
                <td>{{ course[5] }}</td>
              </tr>
              {% endfor %}
            </table>
          </div>
          <div class="table-container">
            <h2>Cloud Database</h2>
            <table>
              <tr>
                <th>ID</th>
                <th>Course Name</th>
                <th>Description</th>
                <th>Duration</th>
                <th>Cost</th>
                <th>Provider</th>
              </tr>
              {% for course in cloud_courses %}
              <tr>
                <td>{{ course[0] }}</td>
                <td>{{ course[1] }}</td>
                <td>{{ course[2] }}</td>
                <td>{{ course[3] }}</td>
                <td>{{ course[4] }}</td>
                <td>{{ course[5] }}</td>
              </tr>
              {% endfor %}
            </table>
          </div>
        </div>
      </body>
    </html>
    """
    return render_template_string(html, local_courses=local_courses, cloud_courses=cloud_courses)

if __name__ == '__main__':
    app.run(debug=True)
