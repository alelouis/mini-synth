import numpy as np
import pyaudio
import mido
from synth.minisynth import Minisynth

synth = Minisynth()
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(2),
            channels=1,
            rate=synth.fs,
            output=True)

buffer_size = 512
buffer_int = np.zeros(buffer_size, dtype=np.int16) 
with mido.open_input('Arturia KeyStep 32') as port:
    while True:
        for sample_id in range(buffer_size):  
            synth.input(port.iter_pending())
            synth.step()
            buffer_int[sample_id] = synth.out
        stream.write(buffer_int.tobytes()) 