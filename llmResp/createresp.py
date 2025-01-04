# llmResp/createresp.py
from langchain_ollama import OllamaLLM
import queue
import time

class LlmResp:
    def __init__(self, RQ=queue.Queue(), socketio=None):
        self.llm = OllamaLLM(model="llama3.1:8b")
        self.rq = RQ
        self.last_input = None
        self.socketio = socketio

    def response(self):
        while True:
            try:
                result = self.rq.get(timeout=1)
                user_input = result["text"].strip()
                
                if user_input and user_input != self.last_input:
                    print(f"\nKullanıcı Girdisi: {user_input}")
                    
                    # Kullanıcı girdisini web arayüzüne gönder
                    if self.socketio:
                        self.socketio.emit('user_input', {'text': user_input})
                    
                    response = self.llm.invoke(user_input)
                    print("\nLLM Yanıtı:")
                    print(response)
                    
                    # LLM yanıtını web arayüzüne gönder
                    if self.socketio:
                        self.socketio.emit('llm_response', {'text': response})
                    
                    self.last_input = user_input
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"LLM Response error: {e}")
                continue
            
            time.sleep(0.1)