# Metro Tracking App 

A real-time metro tracking application with a Flask backend and Vue.js frontend kiosk interface.
---
# Root refers to fare_calculation in the documentation below
```
cd fare_calculation
```
to reach root
---
# Setup Instructions
1. Backend dependencies

Install required Python packages:

```
pip install -r requirement.txt 
```

The requirement.txt is located at the root of the project. 
(or manually if needed: pip install geopy Flask Flask-Cors Flask-SocketIO eventlet)

2. Database (SQLite)  
- The app uses **SQLite**.  
- A `database.sqlite3` file is already included under:  
src/components/backend/Flask/db_scripts/

- No manual setup is required — the backend will detect and use it automatically.  

   #### Reinitialize database (optional) 
   ---
   If you want to reset or reseed the database:  
   1. Go to the same folder:
   2. 
    ```bash
    cd src/components/backend/Flask/db_scripts
   ```
   Open db.py and run the seed_db() function.
   
   ```
   python db.py
   ```
   
   Make sure the CSV files remain in their original location — they are required for seeding.
   ---

3. Run backend (Flask + Data Generator)

From the backend folder:

```
cd src/components/backend/Flask
python app.py
```

This starts the Flask server and the data generator together (via Blueprints).

4. Frontend (Vue kiosk interface)

From the root folder:
```
npm install
npm run dev
```

Then open the displayed localhost URL in your browser to access the kiosk interface.

---
# Project Structure
```
project-root/
├── frontend/                 # Vue.js kiosk interface
│   ├── package.json
│   └── ...
├── src/
│   └── components/
│       └── backend/
│           └── Flask/
│               ├── app.py    # Main Flask app entry point
│               ├── db_scripts/
│               │   ├── database.sqlite3
│               │   ├── db.py
│               │   └── *.csv (for seeding)
│               └── ...
└── requirements.txt
```
---
# Accessing the Kiosk

Run both backend and frontend as described above.
Open the frontend’s local dev server URL (usually http://localhost:5173 for Vite-based Vue apps).
The kiosk will connect to the Flask backend in real-time.
---
