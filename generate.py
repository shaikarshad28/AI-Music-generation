import numpy as np
import torch
import torch.nn as nn
import json
from music21 import instrument, note, stream, chord

class MusicLSTM(nn.Module):
    def __init__(self, n_vocab, input_size=1, hidden_size=512):
        super(MusicLSTM, self).__init__()
        self.lstm1 = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.lstm2 = nn.LSTM(hidden_size, hidden_size, batch_first=True)
        self.lstm3 = nn.LSTM(hidden_size, hidden_size, batch_first=True)
        self.dense = nn.Linear(hidden_size, 256)
        self.relu = nn.ReLU()
        self.out = nn.Linear(256, n_vocab)
        
    def forward(self, x):
        x, _ = self.lstm1(x)
        x, _ = self.lstm2(x)
        x, _ = self.lstm3(x)
        x = x[:, -1, :] 
        x = self.dense(x)
        x = self.relu(x)
        x = self.out(x)
        return x

def generate_notes(model, network_input, int_to_note, n_vocab, num_generate=100):
    start = np.random.randint(0, len(network_input)-1)
    pattern = list(network_input[start])
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.eval()
    
    prediction_output = []
    
    print("Generating music sequence...")
    with torch.no_grad():
        for note_index in range(num_generate):
            prediction_input = np.reshape(pattern, (1, len(pattern), 1))
            prediction_input = prediction_input / float(n_vocab)
            
            input_tensor = torch.from_numpy(prediction_input).float().to(device)
            prediction = model(input_tensor)
            
            probs = torch.softmax(prediction, dim=1).cpu().numpy()[0]
            temperature = 1.0
            probs = np.log(probs + 1e-7) / temperature
            probs = np.exp(probs) / np.sum(np.exp(probs))
            index = np.random.choice(len(probs), p=probs)
            
            result = int_to_note[str(index)]
            prediction_output.append(result)
            
            pattern.append([index])
            pattern = pattern[1:]
            
    return prediction_output

def create_midi(prediction_output, filename='test_output.mid'):
    offset = 0
    output_notes = []
    
    print("Converting generated sequence to MIDI format...")
    for pattern in prediction_output:
        # Pattern is e.g. '60_1.0' or '60.64_0.5'
        parts = pattern.split('_')
        pitch_part = parts[0]
        
        try:
            duration_val = float(parts[1]) if len(parts) > 1 else 0.5
        except:
            duration_val = 0.5
            
        if ('.' in pitch_part) and not pitch_part.isdigit():
            # It's a chord
            notes_in_chord = pitch_part.split('.')
            notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()
                notes.append(new_note)
            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            new_chord.quarterLength = duration_val
            output_notes.append(new_chord)
        else:
            # It's a note
            new_note = note.Note(pitch_part)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            new_note.quarterLength = duration_val
            output_notes.append(new_note)
            
        offset += duration_val
        
    midi_stream = stream.Stream(output_notes)
    midi_stream.write('midi', fp=filename)
    print(f"Saved generated music to {filename}")

def main():
    print("Loading data for generation...")
    network_input = np.load('network_input.npy')
    
    with open('note_to_int.json', 'r') as f:
        note_to_int = json.load(f)
        
    int_to_note = {str(v): k for k, v in note_to_int.items()}
    n_vocab = len(note_to_int)
    
    print("Loading model weights...")
    model = MusicLSTM(n_vocab)
    model.load_state_dict(torch.load('weights.pth'))
    
    prediction_output = generate_notes(model, network_input, int_to_note, n_vocab, num_generate=100)
    
    create_midi(prediction_output, 'generated_music.mid')

if __name__ == '__main__':
    main()
