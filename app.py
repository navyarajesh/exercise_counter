# from flask import Flask, render_template, redirect, url_for
# import subprocess

# app = Flask(__name__)

# # Define current_process globally
# current_process = None

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/start_exercise')
# def start_exercise():
#     global current_process  # declare current_process as global so we can modify it here

#     if current_process and current_process.poll() is None:
#         # Process is already running, you might want to handle this case
#         return "Exercise is already running!"

#     # Start a new process
#     current_process = subprocess.Popen(["python", "exercise_script.py"])
#     return "Exercise started!"

# @app.route('/stop_exercise')
# def stop_exercise():
#     global current_process

#     if current_process and current_process.poll() is None:
#         current_process.terminate()
#         current_process = None  # reset the variable after termination
#         return "Exercise stopped!"
#     else:
#         return "No exercise is currently running."

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, jsonify
import subprocess

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to start a specific exercise
@app.route('/start/<exercise_name>')
def start_exercise(exercise_name):
    # Map exercises to Python scripts
    script_mapping = {
        'bicep_curl': 'bicep_curl.py',  # Script name should match the Python file
        'shoulder_press': 'shoulder_press.py',
    }
    script = script_mapping.get(exercise_name)

    if script:
        subprocess.Popen(['python', script])  # Start the exercise script
        return jsonify({"status": "started", "exercise": exercise_name})
    else:
        return jsonify({"error": "Exercise not found"}), 404

# Route to stop the exercise (this will simulate stopping the video feed)
@app.route('/stop')
def stop_exercise():
    return jsonify({"status": "stopped"})

if __name__ == '__main__':
    app.run(debug=True)