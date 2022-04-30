class Amplifier():
    """Applies linear gain to module"""
    def __init__(self, v_in, gain):
        self.v_in = v_in
        self.gain = gain
        self.v_out = 0

    def update(self):
        self.v_out = self.v_in.v_out * self.gain
