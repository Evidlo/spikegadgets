#!/usr/bin/env python

from nmigen import Elaboratable, Signal, Module, Array
from nmigen.back.pysim import Simulator, Delay

class SevenSegment(Elaboratable):

    def __init__(self):
        self.val = Signal(4)
        self.leds = Signal(7)

    def elaborate(self, platform):
        m = Module()

        table = Array([
            0b0111111, # 0
            0b0000110, # 1
            0b1011011, # 2
            0b1001111, # 3
            0b1100110, # 4
            0b1101101, # 5
            0b1111101, # 6
            0b0000111, # 7
            0b1111111, # 8
            0b1101111, # 9
            0b1110111, # A
            0b1111100, # B
            0b0111001, # C
            0b1011110, # D
            0b1111001, # E
            0b1110001  # F
        ])

        m.d.comb += self.leds.eq(table[self.val])

        return m

class SevenSegController(Elaboratable):
    def __init__(self):
        self.val  = Signal(4)
        self.leds = Signal(7)

    def elaborate(self, platform):
        m = Module()

        table = Array([
            0b0111111, # 0
            0b0000110, # 1
            0b1011011, # 2
            0b1001111, # 3
            0b1100110, # 4
            0b1101101, # 5
            0b1111101, # 6
            0b0000111, # 7
            0b1111111, # 8
            0b1101111, # 9
            0b1110111, # A
            0b1111100, # B
            0b0111001, # C
            0b1011110, # D
            0b1111001, # E
            0b1110001  # F
        ])

        m.d.comb += self.leds.eq(table[self.val])

        return m


def print_leds(leds):
    line_top = ["   ", " _ "]
    line_mid = ["   ", "  │", " _ ", " _│", "│  ", "│ │", "│_ ", "│_│"]
    line_bot = line_mid

    a = leds & 1
    fgb = ((leds >> 1) & 1) | ((leds >> 5) & 2) | ((leds >> 3) & 4)
    edc = ((leds >> 2) & 1) | ((leds >> 2) & 2) | ((leds >> 2) & 4)

    print(line_top[a])
    print(line_mid[fgb])
    print(line_bot[edc])


if __name__ == '__main__':
    # seg = SevenSegment()
    seg = SevenSegController()
    sim = Simulator(seg)

    def process():
        for i in range(16):
            yield seg.val.eq(i)
            yield Delay()
            result = yield seg.leds
            print_leds(result)

    sim.add_process(process)
    with sim.write_vcd('output.vcd'):
        sim.run()
