from flask import Flask, render_template
from flask_socketio import SocketIO
import random

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

def external_app_logic():
    while True:
        data = {"value": random.randint(1, 100)}
        print("Wysyłam:", data)
        socketio.emit("update_data", data)
        socketio.sleep(1)

if __name__ == "__main__":
    socketio.start_background_task(external_app_logic)
    socketio.run(app, host="0.0.0.0", port=5000)

