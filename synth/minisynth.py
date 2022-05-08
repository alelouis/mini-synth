from synth.vco import VCO
from synth.amplifier import Amplifier
from synth.voltage import Voltage   
from synth.mixer import Mixer
from synth.rack import Rack
from synth.adsr import ADSR
from synth.lpfilter import Filter

class Minisynth():
    def __init__(self):
        self.rack = Rack()
        self.fs = 48000 # Hz
        self.notes_on = 0
        self.volume = 0.5

        # Low Frequency Oscillators
        self.lfo_frequency = Voltage(value = 10)
        self.lfo_amp = Voltage(value = 3)
        self.lfo_vibrato = VCO(frequency = self.lfo_frequency, fs = self.fs, shape = 'sine')
        self.lfo_vibrato_amp = Amplifier(value=self.lfo_vibrato, gain = self.lfo_amp)

        # Voltage Controlled Oscillators
        self.vco_frequency = Voltage(value = 110)
        self.lfo_vco_mixer = Mixer(inputs = [self.vco_frequency, self.lfo_vibrato_amp])
        self.vco_0 = VCO(frequency = self.lfo_vco_mixer, fs = self.fs, shape = 'square')

        # Envelope generators
        self.env_trigger = Voltage(value = 0)

        self.env_amp_a = Voltage(value = 5)
        self.env_amp_d = Voltage(value = 50)
        self.env_amp_s = Voltage(value = 0.9)
        self.env_amp_r = Voltage(value = 200)

        self.envelope_amplitude = ADSR(
            trigger = self.env_trigger,
            attack = self.env_amp_a, 
            delay = self.env_amp_d, 
            sustain = self.env_amp_s, 
            release = self.env_amp_r)

        self.env_filter_a = Voltage(value = 5)
        self.env_filter_d = Voltage(value = 50)
        self.env_filter_s = Voltage(value = 0.8)
        self.env_filter_r = Voltage(value = 50)

        self.envelope_filter = ADSR(
            trigger = self.env_trigger,
            attack = self.env_filter_a, 
            delay = self.env_filter_d, 
            sustain = self.env_filter_s, 
            release = self.env_filter_r)

        # Filter
        self.filter_frequency = Voltage(value = 0.2)
        self.filter_resonance = Voltage(value = 0.0)
        self.filter_env_amount = Voltage(value = 0.2)

        self.filter_offset = Voltage(value = 0.1)
        self.filter_env_offset = Mixer(inputs = [self.filter_offset, self.envelope_filter])
        self.filter_env_ampl = Amplifier(value = self.filter_env_offset, gain = self.filter_env_amount)

        self.filter_0 = Filter(
            value = self.vco_0, 
            frequency = self.filter_env_ampl, 
            resonance = self.filter_resonance)

        # Amplitude
        self.output = Amplifier(value = self.filter_0, gain = self.envelope_amplitude)


        modules = [self.lfo_frequency,
                self.lfo_amp,
                self.lfo_vibrato,
                self.lfo_vibrato_amp,
                self.vco_frequency, 
                self.lfo_vco_mixer,
                self.vco_0,
                self.env_trigger, 
                self.env_amp_a, 
                self.env_amp_d, 
                self.env_amp_s, 
                self.env_amp_r, 
                self.envelope_amplitude, 
                self.env_filter_a, 
                self.env_filter_d, 
                self.env_filter_s, 
                self.env_filter_r, 
                self.envelope_filter, 
                self.filter_frequency,
                self.filter_resonance,
                self.filter_env_amount,
                self.filter_offset,
                self.filter_env_offset,
                self.filter_env_ampl,
                self.filter_0,
                self.output]

        for module in modules:
            self.rack.add_object(module)

    def step(self):
        self.rack.step()

    @property
    def out(self):
        out = self.output.outputs[0] * self.volume * 2**16/2
        return out
    
    def midi_note_to_hz(self, note):
        return 440*2**((note-69)/12)

    def input(self, messages):
        for msg in messages:
            if msg.type == 'control_change':
                value = msg.value / 128.
                self.lfo_amp.outputs[0] = value * 6
            if msg.type == 'note_on':
                self.notes_on += 1
                self.env_trigger.outputs[0] = 1
                self.vco_frequency.outputs[0] = self.midi_note_to_hz(msg.note)
            elif msg.type == 'note_off':
                self.notes_on -= 1
            if self.notes_on == 0:
                self.env_trigger.outputs[0] = 0