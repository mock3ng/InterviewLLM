# SpeechRecognition sınıfı
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import queue
import wave
import os

class SpeechRecognition:
    def __init__(self, VQ=queue.Queue(), RQ=queue.Queue()):
        self.rq = RQ
        self.queue = VQ
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.backends.mps.is_available() else torch.float32
        
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            "openai/whisper-large-v3-turbo", torch_dtype=self.torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        self.model.to(self.device)
        
        self.processor = AutoProcessor.from_pretrained("openai/whisper-large-v3-turbo")
        
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            torch_dtype=self.torch_dtype,
            device=self.device 
        )
        print("Model ve pipeline başarıyla yüklendi.")

    def transcribe(self):
        while True:
            try:
                frames = self.queue.get(timeout=1)  # 1 saniye timeout
                if not frames:
                    continue
                    
                filename = "output.wav"
                wf = wave.open(filename, 'wb')
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(44100)
                wf.writeframes(b''.join(frames))
                wf.close()
                
                if os.path.exists(filename):
                    print(f"Processing audio file: {filename}")
                    result = self.pipe(filename)
                    text = result["text"].strip()
                    if text:
                        print(f"Transcribed text: {text}")
                        self.rq.put(result)
                        os.remove(filename)  # İşlem bittikten sonra dosyayı sil
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Transcription error: {e}")
                continue