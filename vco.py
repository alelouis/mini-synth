import math

class VCO():
    """Voltage Controlled Oscillator"""
    def __init__(self, v_in, fs):
        self.v_in = v_in
        self.v_out = 0
        self.fs = fs
        self.t = 0
        self.phi = 0

    def update(self):
        self.t += 1/self.fs
        f = self.v_in.v_out    
        self.phi += 2*math.pi*f/self.fs
        self.v_out = math.cos(self.phi)