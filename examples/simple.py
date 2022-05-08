from synth.rack import Rack
from synth.vco import VCO
from synth.voltage import Voltage

# Create a new rack
rack = Rack()

# Create control voltages for VCO frequency
vco_freq = Voltage(220)

# Create a VCO modulated with LFO
vco = VCO(vco_freq, fs = rack.fs) 

# Register modules in declared order
for module in [vco_freq, vco]:
    rack.add_object(module)

# Run steps
for _ in range(1000):
    rack.step()

rack.plot()