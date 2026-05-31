from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Update with your MySQL password
    'database': 'bcombydk'
}

def create_connection():
    """Create a database connection"""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("Successfully connected to the database")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def create_database():
    """Create database if it doesn't exist"""
    connection = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS bcombydk")
    connection.close()

def create_tables():
    """Create tables if they don't exist"""
    connection = create_connection()
    if connection is None:
        return
    
    cursor = connection.cursor()
    create_inquiries_table = """
    CREATE TABLE IF NOT EXISTS inquiries (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        email VARCHAR(255),
        class VARCHAR(50),
        course VARCHAR(50),
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cursor.execute(create_inquiries_table)
    connection.commit()
    connection.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-inquiry', methods=['POST'])
def submit_inquiry():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form.get('email', '')
        class_name = request.form.get('class', '')
        course = request.form.get('course', '')
        message = request.form.get('message', '')

        connection = create_connection()
        if connection is not None:
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO inquiries (name, phone, email, class, course, message)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (name, phone, email, class_name, course, message))
            connection.commit()
            connection.close()
            print("Inquiry saved successfully")

    return redirect(url_for('index'))

if __name__ == '__main__':
    # Create database and tables if they don't exist
    create_database()
    create_tables()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
