import os
import json
import uuid
import numpy as np
import torch
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from generate import MusicLSTM, generate_notes, create_midi

app = Flask(__name__)
CORS(app)

# Load global resources
print("Loading model and resources...")
network_input = np.load('network_input.npy')
with open('note_to_int.json', 'r') as f:
    note_to_int = json.load(f)
int_to_note = {str(v): k for k, v in note_to_int.items()}
n_vocab = len(note_to_int)

# Initialize and load the trained weights
model = MusicLSTM(n_vocab)
model.load_state_dict(torch.load('weights.pth', map_location=torch.device('cpu')))
model.eval()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        midi_urls = []
        count = 3
        print(f"Generating {count} new music sequences...")
        
        for i in range(count):
            # Generate a unique filename for concurrent requests
            filename = f"{uuid.uuid4().hex}.mid"
            filepath = os.path.join('static', 'midi', filename)
            
            print(f"Generating track {i+1}/{count} ({filename})...")
            # Generate 100 notes
            prediction_output = generate_notes(model, network_input, int_to_note, n_vocab, num_generate=100)
            
            # Create midi file
            create_midi(prediction_output, filepath)
            
            midi_urls.append(f"/static/midi/{filename}")
            
        return jsonify({
            "status": "success",
            "midi_urls": midi_urls
        })
    except Exception as e:
        print("Error during generation:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
