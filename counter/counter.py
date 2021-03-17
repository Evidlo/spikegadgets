from nmigen import *
from nmigen.sim import *
import typer
import os
import math

app = typer.Typer(add_completion=False)

# A simple counter, which increments at every clock cycle.
class Counter(Elaboratable):
    def __init__(self, divide, led_out):
        self.led_out = led_out

        # clock divide
        counter_width = math.ceil(math.log2(divide))
        print(f'{counter_width=}')
        self.counter = Signal(counter_width)
        self.divide = divide

    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.counter.eq(self.counter + 1)
        #
        # divide clock
        with m.If(self.counter == self.divide - 1):
            m.d.sync += self.counter.eq(0)
            m.d.sync += self.led_out.eq(self.led_out + 1)

        return m



@app.command()
def sim(ticks: int = 20, divide: int = 1):
    """Simulate and print results to console"""

    led_out = Signal(4)
    counter = Counter(divide, led_out)
    
    s = Simulator(counter)
    def process():
        for i in range(ticks):
            print("count =", (yield counter.led_out))
            yield Tick()
    s.add_clock(1e-6)
    s.add_sync_process(process)
    with s.write_vcd('dump.vcd', 'dump.gtkw'):
        s.run()


@app.command()
def build(divide: int = 1):
    """Upload to board"""

    # get dev board LEDs
    from nmigen_boards.ecpix5 import ECPIX585Platform
    ecpix = ECPIX585Platform()
    led_out = Cat(
        ecpix.request('rgb_led', 0)[0],
        ecpix.request('rgb_led', 1)[0],
        ecpix.request('rgb_led', 2)[0],
        ecpix.request('rgb_led', 3)[0],
    )

    counter = Counter(divide, led_out)

    # use the build tools from pypi
    os.environ['YOSYS'] = 'yowasp-yosys'
    os.environ['ECPPACK'] = 'yowasp-ecppack'
    os.environ['NEXTPNR_ECP5'] = 'yowasp-nextpnr-ecp5'

    ecpix.build(counter, do_program=True)


if __name__ == '__main__':
    app()
