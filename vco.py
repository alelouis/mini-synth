import numpy as np
from node import Node
        
class VCO(Node):
    """Voltage Controlled Oscillator"""
    def __init__(self, frequency, fs, shape = 'sine'):
        super().__init__([frequency])
        # Inputs
        self.frequency = frequency
        self.shape = shape
        # Outputs
        self.outputs = [0]
        # State
        self.fs = fs
        self.t = 0
        self.phi = 0
        
    def update(self):
        self.t += 1/self.fs
        f = self.frequency.outputs[0]  
        self.phi += 2*np.pi*f/self.fs
        output = np.cos(self.phi)
        if self.shape == 'sine':
            self.outputs[0] = output
        elif self.shape == 'square':
            self.outputs[0] = np.sign(output)