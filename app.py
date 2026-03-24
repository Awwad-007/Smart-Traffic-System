from flask import Flask, render_template, request, redirect
import pymysql
import random
import threading
import time

app = Flask(__name__)
last_override_time = 0  # Global tracker for emergency overrides

def get_db_connection():
    return pymysql.connect(
        host="localhost", user="root", password="",
        database="SmartTrafficDB", cursorclass=pymysql.cursors.DictCursor
    )

# --- BACKGROUND: AUTO-SIMULATE VEHICLES ---
def auto_simulate():
    while True:
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                s_id = random.choice([1, 2, 3, 4])
                cursor.execute("INSERT INTO trafficlogs (signal_id, vehicle_id) VALUES (%s, %s)", (s_id, random.randint(100,800)))
                conn.commit()
            conn.close()
        except: pass
        time.sleep(random.randint(2, 4))

# --- BACKGROUND: 10s AUTO-CYCLE & 15s OVERRIDE RECOVERY ---
def auto_cycle_signals():
    global last_override_time
    current_green = 1
    while True:
        # If an override happened < 15s ago, PAUSE the normal cycle
        if time.time() - last_override_time < 15:
            time.sleep(1)
            continue
            
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("UPDATE signals SET current_state = 'RED'")
                cursor.execute("UPDATE signals SET current_state = 'GREEN' WHERE signal_id = %s", (current_green,))
                conn.commit()
            conn.close()
            current_green = (current_green % 4) + 1
        except: pass
        
        time.sleep(10) # Your 10-second normal cycle

threading.Thread(target=auto_simulate, daemon=True).start()
threading.Thread(target=auto_cycle_signals, daemon=True).start()

@app.route('/')
def index():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM traffic_dashboard")
        t_data = cursor.fetchall()
        cursor.execute("SELECT * FROM emergency_logs")
        h_data = cursor.fetchall()
    conn.close()
    return render_template('index.html', traffic_data=t_data, history_data=h_data)

@app.route('/simulate', methods=['POST'])
def simulate():
    global last_override_time
    s_id = request.form['s_id']
    last_override_time = time.time() # Start 15s override window
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.callproc('ForceEmergencyGreen', [s_id])
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)