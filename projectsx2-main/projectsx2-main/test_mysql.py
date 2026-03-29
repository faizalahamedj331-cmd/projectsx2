import MySQLdb
import sys

print(f"Python version: {sys.version}")
try:
    print("Attempting to import MySQLdb...")
    import MySQLdb
    print("MySQLdb imported successfully.")
except ImportError as e:
    print(f"Failed to import MySQLdb: {e}")
    sys.exit(1)

try:
    print("Attempting to connect to database...")
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', port=3306)
    print("Connected to MySQL server successfully.")
    
    try:
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS project_tracker_db")
        print("Database 'project_tracker_db' checked/created.")
        cursor.close()
    except Exception as e:
        print(f"Failed to create database: {e}")

    conn.select_db('project_tracker_db')
    print("Selected database 'project_tracker_db'.")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
    sys.exit(1)
