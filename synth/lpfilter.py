from synth.node import Node

class Filter(Node):
    """ Moog 24 dB/oct resonant lowpass VCF
    
    References: CSound source code, Stilson/Smith CCRMA paper.
    Modified by paul.kellett@maxim.abel.co.uk July 2000
    """
    def __init__(self, value, frequency, resonance):
        super().__init__([value, frequency, resonance])
        # Inputs
        self.value = value
        self.frequency = frequency
        self.resonance = resonance
        # Outputs
        self.outputs = [0]
        # State
        self.b0 = 0
        self.b1 = 0
        self.b2 = 0
        self.b3 = 0
        self.b4 = 0

    def update(self):
        frequency = self.frequency.outputs[0]
        resonance = self.resonance.outputs[0]
        inp = self.value.outputs[0]

        q = 1 - frequency
        p = frequency + 0.8 * frequency * q
        f = p + p - 1
        q = resonance * (1 + 0.5*q*(1-q+5.6*q*q))

        inp -= q * self.b4
        t1 = self.b1
        self.b1 = (inp + self.b0) * p - self.b1 * f
        t2 = self.b2
        self.b2 = (self.b1 + t1) * p - self.b2 * f
        t1 = self.b3
        self.b3 = (self.b2 + t2) * p - self.b3 * f
        self.b4 = (self.b3 + t1) * p - self.b4 * f
        self.b4 = self.b4 - self.b4 * self.b4 * self.b4 * 0.166667
        self.b0 = inp
        
        self.outputs[0] = self.b4
