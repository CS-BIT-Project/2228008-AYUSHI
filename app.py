from flask import Flask, render_template, request
import subprocess
import os
import signal

app = Flask(__name__)
process = None  # Global for the painter subprocess

@app.route('/', methods=['GET'])  # Only GET here
def home():
    return render_template('index.html')

@app.route('/start', methods=['GET'])
def start_painter():
    global process
    if not process or process.poll() is not None:
        process = subprocess.Popen(["python", "virtualpainter.py"])
        return "🎨 AI Virtual Painter Started!"
    return "⚠️ Virtual Painter is already running!"

@app.route('/stop', methods=['GET'])
def stop_painter():
    global process
    if process and process.poll() is None:
        process.terminate()
        process.wait()
        process = None
        return "🛑 Virtual Painter Stopped!"
    return "⚠️ No active Virtual Painter process!"

@app.route('/exit', methods=['GET'])
def exit_painter():
    global process
    if process and process.poll() is None:
        process.terminate()
        process.wait()
    os.kill(os.getpid(), signal.SIGTERM)
    return "❌ Exiting Virtual Painter..."

if __name__ == '__main__':
    app.run(debug=True, port=5001)
