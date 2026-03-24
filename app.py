from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host="localhost", user="root", password="",
        database="SmartTrafficDB", cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        # Fetch Junctions
        cursor.execute("SELECT * FROM traffic_dashboard")
        traffic_data = cursor.fetchall()
        # Fetch History
        cursor.execute("SELECT * FROM emergency_logs")
        history_data = cursor.fetchall()
    conn.close()
    return render_template('index.html', traffic_data=traffic_data, history_data=history_data)

@app.route('/simulate', methods=['POST'])
def simulate():
    s_id = request.form['s_id']
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('ForceEmergencyGreen', [s_id])
        conn.commit()
    finally:
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)