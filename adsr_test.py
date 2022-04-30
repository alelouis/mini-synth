import pyaudio
import numpy as np
import matplotlib.pyplot as plt

from voltage import Voltage
from vco import VCO
from rack import Rack
from mixer import Mixer
from amplifier import Amplifier
from adsr import ADSR

if __name__ == '__main__':
    fs = 48000 # Hz

    # Modules
    adsr = ADSR(
        v_in = Voltage(0), 
        v_attack = Voltage(1),
        v_delay = Voltage(0.5),
        v_sustain = Voltage(1),
        v_release = Voltage(1))

    # Rack
    my_rack = Rack()                # Modules container
    modules = [adsr]  # Modules to track
    my_rack.add(*modules)           # Register modules

    # Stream
    buffer_size, n_buffers = 512, 100
    history_buffer = np.zeros((n_buffers, buffer_size))

    output_port = adsr # Which module output is streamed
    for buffer_id in range(n_buffers):
        if buffer_id == 20:
            adsr.v_in = Voltage(1)
        if buffer_id == 50:
            adsr.v_in = Voltage(0)
        buffer_int = np.zeros(buffer_size, dtype=np.int16)
        buffer_float = np.zeros(buffer_size, dtype=np.float32)
        for sample_id in range(buffer_size):
            my_rack.update()
            sample = output_port.v_out * 0.5 # Volume
            sample *= 2**16/2 # Int range normalization
            buffer_int[sample_id] = sample
        history_buffer[buffer_id, :] = buffer_int

    plt.plot(history_buffer.flatten())
    plt.show()