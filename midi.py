import numpy as np
import pyaudio

from vco import VCO
from amplifier import Amplifier
from voltage import Voltage   
from mixer import Mixer
from rack import Rack
from adsr import ADSR
from lpfilter import Filter

import mido

rack = Rack()
fs = 48000 # Hz

# Low Frequency Oscillators
lfo_frequency = Voltage(value = 10)
lfo_amp = Voltage(value = 3)
lfo_vibrato = VCO(frequency = lfo_frequency, fs = fs, shape = 'sine')
lfo_vibrato_amp = Amplifier(value=lfo_vibrato, gain = lfo_amp)

# Voltage Controlled Oscillators
vco_frequency = Voltage(value = 110)
lfo_vco_mixer = Mixer(inputs = [vco_frequency, lfo_vibrato_amp])
vco_0 = VCO(frequency = lfo_vco_mixer, fs = fs, shape = 'square')

## Envelope generators

env_trigger = Voltage(value = 0)

env_amp_a = Voltage(value = 5)
env_amp_d = Voltage(value = 50)
env_amp_s = Voltage(value = 0.9)
env_amp_r = Voltage(value = 200)

envelope_amplitude = ADSR(
    trigger = env_trigger,
    attack = env_amp_a, 
    delay = env_amp_d, 
    sustain = env_amp_s, 
    release = env_amp_r)

env_filter_a = Voltage(value = 5)
env_filter_d = Voltage(value = 50)
env_filter_s = Voltage(value = 0.8)
env_filter_r = Voltage(value = 50)

envelope_filter = ADSR(
    trigger = env_trigger,
    attack = env_filter_a, 
    delay = env_filter_d, 
    sustain = env_filter_s, 
    release = env_filter_r)

# Filter

filter_frequency = Voltage(value = 0.2)
filter_resonance = Voltage(value = 0.0)
filter_env_amount = Voltage(value = 0.2)

filter_offset = Voltage(value = 0.1)
filter_env_offset = Mixer(inputs = [filter_offset, envelope_filter])
filter_env_ampl = Amplifier(value = filter_env_offset, gain = filter_env_amount)

filter_0 = Filter(
    value = vco_0, 
    frequency = filter_env_ampl, 
    resonance = filter_resonance)

# Amplitude
output = Amplifier(value = filter_0, gain = envelope_amplitude)


modules = [lfo_frequency,
           lfo_amp,
           lfo_vibrato,
           lfo_vibrato_amp,
           vco_frequency, 
           lfo_vco_mixer,
           vco_0,
           env_trigger, 
           env_amp_a, 
           env_amp_d, 
           env_amp_s, 
           env_amp_r, 
           envelope_amplitude, 
           env_filter_a, 
           env_filter_d, 
           env_filter_s, 
           env_filter_r, 
           envelope_filter, 
           filter_frequency,
           filter_resonance,
           filter_env_amount,
           filter_offset,
           filter_env_offset,
           filter_env_ampl,
           filter_0,
           output]

for module in modules:
    rack.add_object(module)

p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(2),
            channels=1,
            rate=fs,
            output=True)

buffer_size = 512
buffer_id = 0
iteration = 0
notes_on = 0
with mido.open_input('Arturia KeyStep 32') as inport:
    while True:
        buffer_int = np.zeros(buffer_size, dtype=np.int16)
        buffer_float = np.zeros(buffer_size, dtype=np.float32)   

        for sample_id in range(buffer_size):  
            if sample_id % 256 == 0:
                for msg in inport.iter_pending():
                    if msg.type == 'control_change':
                        value = msg.value / 128.
                        lfo_amp.outputs[0] = value * 6
                    if msg.type == 'note_on':
                        notes_on += 1
                        env_trigger.outputs[0] = 1
                        note = msg.note
                        hz = 440*2**((note-69)/12)
                        vco_frequency.outputs[0] = hz
                    elif msg.type == 'note_off':
                        notes_on -= 1
                    if notes_on == 0:
                        env_trigger.outputs[0] = 0

            rack.step()
            sample = output.outputs[0] * 0.5 # Volume
            sample *= 2**16/2 # Int range normalization
            buffer_int[sample_id] = sample
        stream.write(buffer_int.tobytes()) 
        iteration += 1
        
    stream.close()

