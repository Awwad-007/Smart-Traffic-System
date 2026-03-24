# 🚦 Smart City Traffic Management System (TMS) v5.0

A professional-grade Database Management System (DBMS) project built for the **VTU 2022 Scheme**. This system simulates a real-world traffic control center with autonomous signal cycling and emergency overrides.

## 🚀 Key Features
* **Autonomous 4-Node Simulation:** Real-time traffic flow across 4 major junctions (Silk Board, Indiranagar, Koramangala, MG Road).
* **10s Round-Robin Cycling:** Automatic signal rotation every 10 seconds managed by a Python background thread.
* **15s Emergency Override:** Manual "Override" button triggers a MySQL Stored Procedure that pauses the cycle for 15 seconds to clear emergency lanes.
* **Live Analytics:** Real-time bar charts using **Chart.js** to visualize vehicle density.
* **System Audit Log:** Persistent tracking of all emergency events within the MySQL database.

## 🛠️ Tech Stack
* **Backend:** Python 3.x (Flask)
* **Database:** MySQL (MariaDB via XAMPP)
* **Frontend:** HTML5, CSS3 (Glassmorphism UI), JavaScript
* **Visualization:** Chart.js

## 📂 Database Schema
The system relies on the following relational structures:
* `signals`: Stores junction names and current light states (RED/GREEN).
* `trafficlogs`: Stores every vehicle entry and emergency event.
* `traffic_dashboard`: A SQL View for real-time frontend syncing.
* `ForceEmergencyGreen`: A Stored Procedure for atomic state changes.

## ⚙️ Installation & Setup
1.  **Start XAMPP:** Open XAMPP Control Panel and start **Apache** and **MySQL**.
2.  **Setup Database:** * Go to `localhost/phpmyadmin`.
    * Create a database named `SmartTrafficDB`.
    * Import or run the code in `views.sql`.
3.  **Install Dependencies:**
    ```bash
    pip install flask pymysql
    ```
4.  **Run the App:**
    ```bash
    python app.py
    ```
5.  **Access UI:** Open `http://127.0.0.1:5000` in your browser.

---
*Developed as part of the BCS403: Database Management System course.*