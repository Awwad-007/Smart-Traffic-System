from flask import Flask, render_template, request, redirect
import pymysql
import random
import threading
import time

app = Flask(__name__)
last_override_time = 0 

def get_db_connection():
    return pymysql.connect(host="localhost", user="root", password="", database="SmartTrafficDB", cursorclass=pymysql.cursors.DictCursor)

# --- BACKGROUND: RANDOM TRAFFIC GENERATOR ---
def auto_simulate():
    while True:
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO trafficlogs (signal_id, vehicle_id) VALUES (%s, %s)", (random.choice([1,2,3,4]), random.randint(100,800)))
                conn.commit()
            conn.close()
        except: pass
        time.sleep(random.randint(2, 4))

# --- BACKGROUND: 10s CYCLE & 15s RECOVERY ---
def auto_cycle_signals():
    global last_override_time
    curr = 1
    while True:
        # If Override active (<15s ago), pause normal cycle
        if time.time() - last_override_time < 15:
            time.sleep(1)
            continue
            
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("UPDATE signals SET current_state = 'RED'")
                cursor.execute("UPDATE signals SET current_state = 'GREEN' WHERE signal_id = %s", (curr,))
                conn.commit()
            conn.close()
            curr = (curr % 4) + 1
        except: pass
        time.sleep(10) # Normal 10s Interval

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
    last_override_time = time.time() # Mark the 15s Emergency Window
    s_id = request.form['s_id']
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.callproc('ForceEmergencyGreen', [s_id])
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)