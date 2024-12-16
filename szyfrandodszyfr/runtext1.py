#!/usr/bin/env python
# Display a runtext with double-buffering.
from samples.samplebase import SampleBase
from rgbmatrix import graphics
import time


class RunText(SampleBase):
    def __init__(self, *args, text="", **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.text = text
        self.parser.add_argument("--led-no-hardware-pulse", action="store", help="Don't use hardware pin-pulse generation")
        
    def run(self):
        """
        Uruchamia tekst przewijaj�cy si� na macierzy LED.
        """
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/10x20.bdf")
        textColor = graphics.Color(255, 0, 0)
        pos = offscreen_canvas.width
        my_text = self.text

        while True:
            offscreen_canvas.Clear()
            text_length = graphics.DrawText(offscreen_canvas, font, pos, 20, textColor, my_text)
            pos -= 1
            if pos + text_length < 0:
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


def display_text_on_matrix(text):
    run_text = RunText(text=text)
    if not run_text.process():
        run_text.print_help()
