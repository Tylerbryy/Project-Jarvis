import os
import torch
import sounddevice as sd
import pyaudio
import json
import numpy as np
from pathlib import Path

device = torch.device('cuda')
torch.set_num_threads(8)
local_file = 'models\\v3_en.pt'

model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
model.to(device)

example_text = "The Drake equation is a probabilistic argument used to estimate the number of active, communicative extraterrestrial civilizations in the Milky Way galaxy. fifty-seven"
sample_rate = 48000
speaker='en_103'

# Define the PyAudio stream and callback function
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paFloat32,
                 channels=1,
                 rate=sample_rate,
                 output=True)


# Define the cache file path
cache_path = Path('audio_cache.json')

# Define the cache dictionary
audio_cache = {}

# Load the cache from the file or from memory
if cache_path.exists():
    with open(cache_path, 'r') as f:
        for line in f:
            # Parse each line of the JSON file and add it to the cache
            data = json.loads(line)
            audio_cache.update(data)
else:
    audio_cache = {}

# Define the audio generation function
def generate_audio(text):
    if text in audio_cache:
        # Use cached audio if available
        audio = np.array(audio_cache[text], dtype=np.float32)
        
    else:
        # Generate audio using the PyTorch model
        with torch.no_grad():
            audio = model.apply_tts(text=text,
                                    speaker=speaker,
                                    sample_rate=sample_rate,
                                    put_accent=True,
                                    put_yo=True).cpu().numpy()
        # Add generated audio to the cache
        audio_cache[text] = audio.tolist()
        with open(cache_path, 'a') as f:
            # Write the new data to the end of the JSON file
            json.dump({text: audio.tolist()}, f)
            f.write('\n')  # Add a newline character to separate entries

    return audio

# Generate and stream the audio
with torch.no_grad():
    audio = generate_audio(example_text)
stream.start_stream()
stream.write(audio.tobytes())
stream.stop_stream()
stream.close()
pa.terminate()
