# app.py
from flask import Flask, render_template, jsonify
import scheduler_logic  # Imports your modified scheduler code

app = Flask(__name__)

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/run-schedule')
def run_schedule():
    """
    Runs the scheduler logic and returns the results as JSON.
    This is what your JavaScript will call.
    """
    try:
        # Call the main function from your scheduler script
        schedule, diverted, total_cost = scheduler_logic.run_scheduler()
        
        # Return the data in a structured JSON format
        return jsonify({
            'schedule': schedule,
            'diverted': diverted,
            'total_cost': total_cost,
            'total_scheduled': len(schedule),
            'total_diverted': len(diverted)
        })

    except Exception as e:
        # Handle any errors
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    # Runs the web server
    app.run(debug=True, port=5000)