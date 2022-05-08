from enum import Enum
from node import Node
import copy

class Event(Enum):
    OFF = 0
    ON = 1

class Status(Enum):
    IDLE = 0
    ATTACK = 1
    DELAY = 2
    SUSTAIN = 3
    RELEASE = 4

class ADSR(Node):
    def __init__(self, trigger, attack, delay, sustain, release):
        super().__init__([trigger, attack, delay, sustain, release])
        self.trigger = trigger
        self.last_trigger = copy.deepcopy(self.trigger)
        self.attack = attack
        self.delay = delay
        self.sustain = sustain
        self.release = release
        self.status = Status.IDLE
        self.state = 0
        self.outputs = [0]
        self.scale = 100
        self.last_attack = 0

    def update(self):
        event = None
        if self.trigger.outputs[0] != self.last_trigger.outputs[0]:
            event = Event.OFF if self.trigger.outputs[0] == 0 else Event.ON
            self.last_trigger = copy.deepcopy(self.trigger)
        if event == Event.ON:
            self.last_attack = self.outputs[0]
            self.state = 0
            self.status = Status.ATTACK
        elif event == Event.OFF:
            self.state = 0
            self.release_value = self.outputs[0]
            self.status = Status.RELEASE
        else:
            if self.status == Status.ATTACK:
                self.state += 1
                self.outputs[0] += ((1-self.last_attack)/self.attack.outputs[0]) / self.scale
                if self.state > self.attack.outputs[0] * self.scale:
                    self.state = 0
                    self.status = Status.DELAY

            if self.status == Status.DELAY:
                self.state += 1
                self.outputs[0] -= ((1-self.sustain.outputs[0])/self.delay.outputs[0]) / self.scale
                if self.state > self.delay.outputs[0] * self.scale:
                    self.status = Status.SUSTAIN
                    self.state = 0

            if self.status == Status.SUSTAIN:
                self.outputs[0] = self.sustain.outputs[0]

            if self.status == Status.RELEASE:
                self.state += 1
                self.outputs[0] -= (self.release_value/self.release.outputs[0]) / self.scale
                if self.state > self.release.outputs[0] * self.scale:
                    self.status = Status.IDLE
                    self.state = 0