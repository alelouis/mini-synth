from synth.vco import VCO
from synth.amplifier import Amplifier
from synth.voltage import Voltage
from synth.mixer import Mixer
from synth.rack import Rack

rack = Rack()

voltage_0 = Voltage(value=10)
voltage_1 = Voltage(value=1000)
vco_0 = VCO(frequency=voltage_0, fs=rack.fs)
amp_0 = Amplifier(value=vco_0, gain=voltage_1)
vco_1 = VCO(frequency=amp_0, fs=rack.fs)
mixer_0 = Mixer(inputs=[vco_0, vco_1])
amp_1 = Amplifier(value=mixer_0, gain=voltage_1)
vco_2 = VCO(frequency=amp_1, fs=rack.fs)

modules = [voltage_0, voltage_1, vco_0, amp_0, vco_1, mixer_0, amp_1, vco_2]
for module in modules:
    rack.add_object(module)

n_ite = 10000
for iteration in range(n_ite):
    rack.step()
