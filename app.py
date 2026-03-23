from flask import Flask, render_template
import pymysql

app = Flask(__name__)

# Updated connection using PyMySQL
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="SmartTrafficDB",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Using the VIEW we created
            cursor.execute("SELECT * FROM traffic_dashboard")
            data = cursor.fetchall()
        conn.close()
        return render_template('index.html', traffic_data=data)
    except Exception as e:
        return f"Database Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)