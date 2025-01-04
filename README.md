


# Hack the Interview

**Hack the Interview** is an innovative Python program designed to assist in online interviews by listening to audio and providing instant answers. The answers are displayed on the left side of the screen, creating an efficient and seamless interaction between the interviewer and the interviewee.

## Features

- **Real-Time Voice Recognition**: The program listens to the interviewer’s speech and responds with a detailed answer, displayed on the left side of the screen.
- **Fast Processing**: The system prioritizes speed by using a "Push-to-Talk" approach. This minimizes the load on the system, ensuring quick and responsive answers.
- **Llama 8B Model**: The program utilizes the advanced Llama 8B model for accurate and contextually relevant responses.
- **Multilingual Support**: Supports 17 different languages, enabling the program to adapt to various linguistic needs during interviews.
- **Web Application**: Hack the Interview operates as a web application, allowing multiple devices to connect and interact with the program online.

## System Requirements

- Python 3.8 or higher
- **Ollama**: Download Ollama from [here](https://ollama.com/) to access the Llama model.
- Virtual environment setup is required for installation.

## Installation

1. **Download Ollama**:  
   Visit [Ollama](https://ollama.com/) and download the Ollama software. It’s essential for accessing the Llama 8B model.

2. **Create a Virtual Environment**:  
   It's recommended to use a virtual environment for managing dependencies. To create one, use the following commands:
   
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies**:  
   Next, install the required packages listed in `requirements.txt` by running:
   
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:  
   To start the application, simply run:
   
   ```bash
   python app.py
   ```

   This will start a Flask-based server. You can now access the application from any device connected to the same network.

## How it Works

The program operates as a web application, enabling users to access the service remotely from any device. This ensures that even if the interviewer and interviewee are on different devices, the system can still function smoothly.

1. **Voice Input Capture**:  
   The program listens for input via a microphone using the "Push-to-Talk" mechanism. This ensures that the system doesn’t consume unnecessary resources while waiting for speech input.

2. **Speech-to-Text**:  
   After capturing the speech, the program converts the audio to text. This is achieved using advanced speech-to-text models integrated into the application.

3. **Llama 8B Model**:  
   Once the speech is converted to text, the program sends the input to the Llama 8B model for processing. The Llama model generates an accurate, contextually appropriate response.

4. **Displaying the Response**:  
   The generated response is then displayed on the left side of the screen in real time, making the interaction smoother and more efficient.

## Flask Web Application

- The use of Flask ensures that this application can be accessed over a network, making it a web-based solution.
- This allows you to run the program on a single machine and access it from multiple devices, ideal for interview settings or group collaborations.

## Screenshot

Here’s a screenshot of how the interface looks:

![Screenshot](path/to/screenshot.png)

## Why This Approach?

Using Flask for the web interface ensures that the program can be controlled remotely, which is critical for online interviews where physical presence may be limited or not possible. The system uses efficient speech recognition to transcribe and generate responses quickly, making it suitable for real-time interactions during interviews. The program also avoids audio recording to maintain privacy and focuses solely on text output during the interview process.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

