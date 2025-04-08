from flask import Flask, render_template
import subprocess
import os
import signal

app = Flask(__name__)
process = None  # Store the Virtual Painter process globally

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start')
def start_painter():
    global process
    if not process or process.poll() is not None:  # Check if process is not running
        process = subprocess.Popen(["python", "virtualpainter.py"])
        return "🎨 AI Virtual Painter Started!"
    return "⚠️ Virtual Painter is already running!"

@app.route('/stop')
def stop_painter():
    global process
    if process and process.poll() is None:  # Check if process is running
        process.terminate()  # Send termination signal
        process.wait()  # Wait until process exits
        process = None
        return "🛑 Virtual Painter Stopped!"
    return "⚠️ No active Virtual Painter process!"

@app.route('/exit')
def exit_painter():
    global process
    if process and process.poll() is None:
        process.terminate()  # Kill the painter process first
        process.wait()
    os.kill(os.getpid(), signal.SIGTERM)  # Then terminate Flask
    return "❌ Exiting Virtual Painter..."

if __name__ == '__main__':
    app.run(debug=True, port=5001)