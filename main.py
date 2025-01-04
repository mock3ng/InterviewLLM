# main.py
import threading
import queue
import time
from pynput import keyboard
from flask import Flask, render_template_string
from flask_socketio import SocketIO
from audiotracker.desktopaudio import RecordVoice
from audiotracker.speechtotext import SpeechRecognition
from llmResp.createresp import LlmResp
import webbrowser

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Yanıtları</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            background-color: #1e1e1e;
            color: #fff;
            font-family: 'Consolas', monospace;
            overflow: hidden;
        }

        #container {
            width: 30%;
            padding: 20px;
            height: 100vh;
            overflow-y: auto;
            box-sizing: border-box;
        }

        .user-input {
            color: #64b5f6;
            margin: 10px 0;
            padding: 10px;
            border-left: 3px solid #64b5f6;
            background-color: rgba(100, 181, 246, 0.1);
        }

        .llm-response {
            color: #81c784;
            margin: 10px 0;
            padding: 10px;
            border-left: 3px solid #81c784;
            background-color: rgba(129, 199, 132, 0.1);
            opacity: 0;
            animation: fadeIn 0.5s ease forwards;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
    </style>
</head>
<body>
    <div id="container"></div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        const container = document.getElementById('container');
        const socket = io();

        socket.on('user_input', function(data) {
            const userDiv = document.createElement('div');
            userDiv.className = 'user-input';
            userDiv.textContent = `Ques: ${data.text}`;
            container.appendChild(userDiv);
            container.scrollTop = container.scrollHeight;
        });

        socket.on('llm_response', function(data) {
            const responseDiv = document.createElement('div');
            responseDiv.className = 'llm-response';
            responseDiv.textContent = `LLM: ${data.text}`;
            container.appendChild(responseDiv);
            container.scrollTop = container.scrollHeight;
        });
    </script>
</body>
</html>
'''

class SpaceBarControl:
    def __init__(self, producer):
        self.producer = producer
        self.is_recording = False
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        if key == keyboard.Key.space and not self.is_recording:
            print("Recording started...")
            self.is_recording = True
            self.producer.start_recording()

    def on_release(self, key):
        if key == keyboard.Key.space and self.is_recording:
            print("Recording stopped...")
            self.is_recording = False
            self.producer.stop_recording()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

def run_flask():
    socketio.run(app, host='127.0.0.1', port=5000)

def open_browser():
    time.sleep(1.5)  # Flask sunucusunun başlaması için bekle
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == "__main__":
    sharedQ = queue.Queue()
    responseQ = queue.Queue()

    producer = RecordVoice(sharedQ)
    consumer = SpeechRecognition(sharedQ, responseQ)
    responser = LlmResp(responseQ, socketio)  
   

    producer_thread = threading.Thread(target=producer.record, daemon=True)
    consumer_thread = threading.Thread(target=consumer.transcribe, daemon=True)
    responser_thread = threading.Thread(target=responser.response, daemon=True)
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    browser_thread = threading.Thread(target=open_browser, daemon=True)

    producer_thread.start()
    consumer_thread.start()
    responser_thread.start()
    flask_thread.start()
    browser_thread.start()

    
    space_control = SpaceBarControl(producer)

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nProgram sonlandırıldı.")