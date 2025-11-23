# Airport Landing Slot Scheduler

## ✈️ Overview
This project is an Airport Runway Scheduler that optimizes the landing times of aircraft to minimize penalty costs associated with early or late landings. It uses a greedy algorithm to assign landing slots based on safety separation constraints and time windows.

The application features a Flask backend for processing the scheduling logic and a responsive HTML/JavaScript frontend to visualize the results, including the final schedule, diverted flights, and total deviation costs.

## ✨ Features
Greedy Scheduling Algorithm: Automatically sorts and schedules flights based on their Latest Landing Time (LLT).

Constraint Handling: Respects specific separation times required between different aircraft to ensure safety.

Cost Calculation: Calculates penalties for landing earlier or later than the Target Landing Time (TLT).

Diverted Flights Detection: Identifies flights that cannot land within their allowed window (ELT to LLT) and marks them as diverted.

Automatic Dataset Retrieval: Fetches the benchmark dataset (alp_10_1.txt) directly from the OR-Library if not present locally.

Web Interface: A clean UI to trigger the scheduler and view detailed tables of the results.

## 🛠️ Tech Stack
Language: Python 3.x

Backend Framework: Flask

Data Processing: Pandas

Frontend: HTML, CSS, Vanilla JavaScript

## 📂 Project Structure
Plaintext
.
├── app.py                # Flask entry point; serves the web UI and API
├── scheduler_logic.py    # Core logic: downloads data, parses it, and runs the algorithm
├── alp_10_1.txt          # Benchmark dataset (downloaded automatically)
├── templates/
│   └── index.html        # Frontend user interface
└── README.md             # Project documentation
🚀 Installation & Usage

### 1. Prerequisites

Ensure you have Python installed. You will need to install the required libraries:

_```Bash```_\
```pip install flask pandas requests```

### 2. Run the Application

Start the Flask server:

_```Bash```_\
```python app.py```

### 3. Access the Scheduler

Open your web browser and navigate to: http://127.0.0.1:5000

Click the "Run Greedy Scheduler" button to execute the algorithm. The results (Total Cost, Scheduled Flights, Diverted Flights) will appear instantly.

🧠 How the Algorithm Works
The core logic resides in scheduler_logic.py and follows these steps:

Data Loading: Reads alp_10_1.txt (sourced from the OR-Library), which contains flight details (Earliest, Target, and Latest Landing Times) and a separation matrix.

Sorting: Flights are sorted by their Latest Landing Time (LLT). This is a greedy heuristic to prioritize planes that have tighter deadlines.

Scheduling:

The algorithm iterates through the sorted list.

It calculates the earliest possible landing time based on the separation required from the previously landed plane.

The actual landing time is max(Earliest Landing Time (ELT), Separation Time).

Validation:

If the actual time is within the allowed window (<= LLT), the flight is scheduled, and the cost (early/late penalty) is calculated.

If the actual time exceeds the LLT, the flight is diverted.

📊 Dataset
The project uses the alp_10_1.txt dataset from the OR-Library (Aircraft Landing Problem).

Source: OR-Library

Format: Contains the number of planes, separation times, and for each plane: Appearance time, Earliest/Target/Latest landing times, and cost penalties.AirportLandingSlotScheduler
