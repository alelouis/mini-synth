import pyaudio
import numpy as np

from voltage import Voltage
from vco import VCO
from rack import Rack
from mixer import Mixer
from amplifier import Amplifier

if __name__ == '__main__':
    fs = 48000 # Hz

    # Modules
    lfo = VCO(Voltage(5), fs)       # LFO (but its just slow VCO)
    amp = Amplifier(lfo, 10)        # Linear gain amp
    mix = Mixer()                   # Used to add signals
    mix.add(*[amp, Voltage(440)])   # Register modules
    vco = VCO(mix, fs)              # Voltage Controlled Oscillator

    # Rack
    my_rack = Rack()                # Modules container
    modules = [amp, lfo, mix, vco]  # Modules to track
    my_rack.add(*modules)           # Register modules

    # Stream
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(2),
                channels=1,
                rate=fs,
                output=True)
        
    buffer_size, n_buffers = 512, 1000
    history_buffer = np.zeros((n_buffers, buffer_size))

    output_port = vco # Which module output is streamed
    for buffer_id in range(n_buffers):
        buffer_int = np.zeros(buffer_size, dtype=np.int16)
        buffer_float = np.zeros(buffer_size, dtype=np.float32)
        for sample_id in range(buffer_size):
            my_rack.update()
            sample = output_port.v_out * 0.5 # Volume
            sample *= 2**16/2 # Int range normalization
            buffer_int[sample_id] = sample
        history_buffer[buffer_id, :] = buffer_int
        stream.write(buffer_int.tobytes())