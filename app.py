# ─────────────────────────────────────────────
#  Smart City TMS v6.0 — Hybrid Kinetic Mode
#  PREREQ: ALTER TABLE trafficlogs ADD COLUMN src VARCHAR(20) DEFAULT 'Auto';
# ─────────────────────────────────────────────

from flask import Flask, render_template, request, redirect, jsonify
import pymysql, random, threading, time


app = Flask(__name__)

# ── Globals ───────────────────────────────────
last_ovr   = 0
t_lvl      = {1: 'normal', 2: 'normal', 3: 'normal', 4: 'normal'}  # per-junction level state
lv_veh     = {'low': 45,  'medium': 280, 'high': 620}              # vehicle count per level
lv_dur     = {'low': 8,   'medium': 10,  'high': 20, 'normal': 10} # green duration (seconds)

# ── DB helper ─────────────────────────────────
def db():
    return pymysql.connect(
        host="localhost", user="root", password="",
        database="SmartTrafficDB",
        cursorclass=pymysql.cursors.DictCursor
    )

def run_migrations():
    try:
        c = db()
        with c.cursor() as cur:
            cur.execute("""
                ALTER TABLE trafficlogs 
                ADD COLUMN src VARCHAR(20) DEFAULT 'Auto'
            """)
            c.commit()
            print("[DB] Migration applied: src column added.")
        c.close()
    except Exception as e:
        # Column likely already exists — safe to ignore
        print(f"[DB] Migration skipped: {e}")

run_migrations()  # Call it once before threads start

# ── Background: Auto random traffic logger ────
def auto_sim():
    while True:
        try:
            c = db()
            with c.cursor() as cur:
                cur.execute(
                    "INSERT INTO trafficlogs (signal_id, vehicle_id, src) VALUES (%s, %s, %s)",
                    (random.choice([1,2,3,4]), random.randint(100, 800), 'Auto')
                )
                c.commit()
            c.close()
        except: pass
        time.sleep(random.randint(2, 4))

# ── Background: Adaptive signal cycle ─────────
def auto_cycle():
    global last_ovr, t_lvl
    curr = 1
    while True:
        # Pause cycle during emergency override window (15s)
        if time.time() - last_ovr < 15:
            time.sleep(1)
            continue
        try:
            c = db()
            with c.cursor() as cur:
                cur.execute("UPDATE signals SET current_state = 'RED'")
                cur.execute("UPDATE signals SET current_state = 'GREEN' WHERE signal_id = %s", (curr,))
                c.commit()
            c.close()
        except: pass

        # ── SMART PART: duration is driven by junction's traffic level ──
        g_dur = lv_dur.get(t_lvl.get(curr, 'normal'), 10)
        curr  = (curr % 4) + 1
        time.sleep(g_dur)

threading.Thread(target=auto_sim,   daemon=True).start()
threading.Thread(target=auto_cycle, daemon=True).start()

# ── Routes ────────────────────────────────────
@app.route('/')
def index():
    c = db()
    with c.cursor() as cur:
        cur.execute("SELECT * FROM traffic_dashboard")
        t_data = cur.fetchall()
        cur.execute("SELECT * FROM emergency_logs")
        h_data = cur.fetchall()
    c.close()
    return render_template('index.html', traffic_data=t_data, history_data=h_data, t_lvl=t_lvl)

@app.route('/simulate', methods=['POST'])
def simulate():
    global last_ovr
    last_ovr = time.time()
    s_id = request.form['s_id']
    try:
        c = db()
        with c.cursor() as cur:
            cur.execute("UPDATE signals SET current_state = 'RED'")
            cur.execute("UPDATE signals SET current_state = 'GREEN' WHERE signal_id = %s", (s_id,))
            c.commit()
        c.close()
    except Exception as e:
        print(f"[Override Error] {e}")
    return redirect('/')

# ── NEW: Manual sensor input endpoint ─────────
@app.route('/sensor', methods=['POST'])
def sensor():
    global t_lvl
    data  = request.get_json()
    s_id  = int(data.get('s_id'))
    level = data.get('level', 'normal')   # 'low' | 'medium' | 'high'

    # 1. Update in-memory level state (cycle thread reads this)
    t_lvl[s_id] = level

    # 2. Compute vehicle count for this level
    v_cnt = lv_veh.get(level, random.randint(100, 400))

    # 3. Log to DB with 'Manual_Input' flag
    try:
        c = db()
        with c.cursor() as cur:
            cur.execute(
                "INSERT INTO trafficlogs (signal_id, vehicle_id, src) VALUES (%s, %s, %s)",
                (s_id, v_cnt, 'Manual_Input')
            )
            c.commit()
        c.close()
        return jsonify({
            'ok':      True,
            'junc':    s_id,
            'level':   level,
            'vehicles': v_cnt,
            'green_s': lv_dur.get(level, 10)
        })
    except Exception as e:
        return jsonify({'ok': False, 'err': str(e)}), 500

# ── NEW: Live level state for JS polling ──────
@app.route('/levels')
def levels():
    return jsonify(t_lvl)

if __name__ == '__main__':
    app.run(debug=True)