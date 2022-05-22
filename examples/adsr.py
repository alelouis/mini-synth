from synth.vco import VCO
from synth.amplifier import Amplifier
from synth.voltage import Voltage
from synth.rack import Rack
from synth.adsr import ADSR
from synth.rack import Rack

rack = Rack()

trigger = Voltage(value=0)
attack = Voltage(value=1)
delay = Voltage(value=0.5)
sustain = Voltage(value=0.5)
release = Voltage(value=3)

adsr = ADSR(
    trigger=trigger, attack=attack, delay=delay, sustain=sustain, release=release
)

voltage_f = Voltage(value=880)
vco_0 = VCO(frequency=voltage_f, fs=rack.fs, shape="square")
amp_adsr = Amplifier(value=vco_0, gain=adsr)

modules = [trigger, attack, delay, sustain, release, adsr, voltage_f, vco_0, amp_adsr]

for module in modules:
    rack.add_object(module)

n_ite = 3300
for iteration in range(n_ite):
    if iteration == 0:
        trigger.outputs[0] = 0
    if iteration == 1000:
        trigger.outputs[0] = 1
    if iteration == 2000:
        trigger.outputs[0] = 0
    rack.step()
