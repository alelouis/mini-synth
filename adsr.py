from enum import Enum
import copy

class Event(Enum):
    ON = 1
    OFF = 2

class Status(Enum):
    ATTACK = 1
    DELAY = 2
    SUSTAIN = 3
    RELEASE = 4
    IDLE = 5

class ADSR():
    def __init__(self, v_in, v_attack, v_delay, v_sustain, v_release):
        self.v_attack = v_attack
        self.v_delay = v_delay
        self.v_sustain = v_sustain
        self.v_release = v_release
        self.v_in = v_in
        self.last_v_in = copy.copy(self.v_in.v_out)
        self.status = Status.IDLE
        self.state = 0
        self.v_out = 0
        self.scale = 1/3000

    def update(self):
        # Checking events
        event = None
        if self.v_in.v_out != self.last_v_in:
            event = Event.OFF if self.v_in.v_out == 0 else Event.ON
        self.last_v_in = copy.copy(self.v_in.v_out)

        if self.status == Status.IDLE and event == Event.ON:
                self.status = Status.ATTACK

        if self.status == Status.ATTACK:
            self.state += self.scale
            self.v_out += self.v_attack.v_out/10000
            if self.state > self.v_attack.v_out:
                self.state = 0
                self.status = Status.DELAY

        if self.status == Status.DELAY:
            self.state += self.scale
            self.v_out -= self.v_delay.v_out/10000
            if self.state > self.v_delay.v_out:
                self.status = Status.SUSTAIN
                self.state = 0

        if self.status == Status.SUSTAIN:
            self.v_out = self.v_out

        if self.status == Status.RELEASE:
            self.state += self.scale
            self.v_out -= self.v_release.v_out/10000
            if self.state > self.v_release.v_out:
                self.status = Status.IDLE
                self.state = 0

        if event == Event.OFF:
            self.status = Status.RELEASE
            