AI Music Generator 🎵🤖

Welcome to the **AI Music Generator**, a full-stack deep learning application that composes original music sequences using Artificial Intelligence! 

This project leverages a Long Short-Term Memory (LSTM) neural network built with PyTorch to understand musical patterns and generate expressive MIDI tracks. It features a sleek web interface powered by Flask, allowing users to generate and listen to multiple AI-composed tracks simultaneously.

Features

- **Deep Learning Model:** Powered by a robust 3-layer LSTM network with 512 hidden units, trained to generate complex and rhythmic musical compositions.
- **Concurrent Generation:** The Flask backend is optimized to generate multiple unique MIDI tracks (up to 3 variations) in a single request.
- **Interactive Web Interface:** A modern frontend built with HTML, CSS, and JavaScript for seamless interaction and playback.
- **Robust MIDI Processing:** Utilizes the `music21` library to process chords, notes, and durations, ensuring musically coherent outputs.
- **Temperature Sampling:** Employs probabilistic sampling to ensure each generated sequence is unique and creative.

Technologies Used

- **Deep Learning:** PyTorch, NumPy
- **Backend:** Python, Flask, Flask-CORS
- **Frontend:** HTML5, Vanilla CSS, JavaScript
- **Audio Processing:** `music21` (for MIDI generation and parsing)

Getting Started

Follow these steps to run the project locally on your machine:

1. Clone the Repository
bash
git clone <your-repo-link>
cd "MUSIC GENERATION AG"


2. Set Up a Virtual Environment (Optional but recommended)
bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate


3. Install Dependencies
Make sure you have the required Python packages installed. You can install them using pip:
bash
pip install torch numpy flask flask-cors music21

*(Note: If you have a CUDA-enabled GPU, install the appropriate PyTorch version for hardware acceleration).*

4. Run the Application
Start the Flask backend server:
bash
python app.py


5. Access the Web Interface
Open your web browser and navigate to:

http://localhost:5000

Click the "Generate" button on the web page to start composing AI music!

How It Works

1. **Model Architecture:** The neural network (`MusicLSTM` in `generate.py`) consists of three LSTM layers followed by dense layers. It takes a sequence of musical notes as input and predicts the most probable next note.
2. **Generation Process:** The script picks a random starting pattern from the pre-processed data (`network_input.npy`) and iteratively predicts the next 100 notes or chords.
3. **MIDI Creation:** The predictions, mapped through `note_to_int.json`, are converted back into `music21` Note and Chord objects and saved as `.mid` files.

