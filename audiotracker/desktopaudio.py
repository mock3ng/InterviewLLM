# RecordVoice sınıfı
import pyaudio
import wave
import threading
import queue
import time

# RecordVoice sınıfı
class RecordVoice:
    def __init__(self, VQ=queue.Queue()):
        self.queue = VQ
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.recording = False
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.ready_to_record = True  # Yeni kayıt için hazır olma durumu

    def start_recording(self):
        if self.ready_to_record and not self.recording:
            self.recording = True
            self.frames = []
            if self.stream is None:
                self.stream = self.audio.open(
                    format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    frames_per_buffer=self.CHUNK
                )

    def stop_recording(self):
        if self.recording:
            self.recording = False
            if self.stream and self.frames:
                print("Sending frames to queue...")
                self.queue.put(self.frames.copy())  # frames'in kopyasını gönder
                self.frames = []  # frames'i temizle
                self.ready_to_record = True  # Yeni kayıt için hazır

    def record(self):
        while True:
            if self.recording:
                try:
                    data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                    self.frames.append(data)
                except Exception as e:
                    print(f"Recording error: {e}")
                    self.stop_recording()
            else:
                time.sleep(0.1)