from flask import Flask, render_template, request, redirect
import pymysql
import random
import threading
import time

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host="localhost", user="root", password="",
        database="SmartTrafficDB", cursorclass=pymysql.cursors.DictCursor
    )

# --- BACKGROUND AUTO-SIMULATOR ---
def auto_simulate():
    while True:
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                s_id = random.choice([1, 2, 3, 4]) # Now picks from 4 junctions
                v_id = random.randint(100, 800)
                cursor.execute("INSERT INTO trafficlogs (signal_id, vehicle_id) VALUES (%s, %s)", (s_id, v_id))
                conn.commit()
            conn.close()
        except: pass
        time.sleep(random.randint(2, 5))

threading.Thread(target=auto_simulate, daemon=True).start()

@app.route('/')
def index():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM traffic_dashboard")
        traffic_data = cursor.fetchall()
        cursor.execute("SELECT * FROM emergency_logs")
        history_data = cursor.fetchall()
    conn.close()
    return render_template('index.html', traffic_data=traffic_data, history_data=history_data)

@app.route('/simulate', methods=['POST'])
def simulate():
    s_id = request.form['s_id']
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.callproc('ForceEmergencyGreen', [s_id])
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)