#!/usr/bin/env python
# Display a runtext with double-buffering.
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time


class RunText:
    def __init__(self, text):
        self.text = text

        # Konfiguracja macierzy LED
        self.options = RGBMatrixOptions()
        self.options.rows = 32  # Liczba rz�d�w macierzy
        self.options.cols = 64  # Liczba kolumn macierzy
        self.options.chain_length = 1  # Liczba po��czonych macierzy
        self.options.parallel = 1  # Liczba r�wnoleg�ych �a�cuch�w
        self.options.hardware_mapping = 'adafruit-hat'  # Mapowanie GPIO dla Adafruit HAT
        self.options.brightness = 100  # Jasno�� (1-100)
        self.options.gpio_slowdown = 4  # Spowolnienie GPIO (2 zalecane dla Adafruit HAT)

        # Inicjalizacja macierzy
        self.matrix = RGBMatrix(options=self.options)

    def run(self):
        """
        Uruchamia tekst przewijaj�cy si� na macierzy LED.
        """
        # Konfiguracja czcionki i koloru tekstu
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("./fonts/10x20.bdf")
        text_color = graphics.Color(255, 0, 0)  # Czerwony tekst

        # Pozycja startowa tekstu
        pos = offscreen_canvas.width

        while True:
            offscreen_canvas.Clear()
            text_length = graphics.DrawText(offscreen_canvas, font, pos, 20, text_color, self.text)
            pos -= 1
            if pos + text_length < 0:
                pos = offscreen_canvas.width

            time.sleep(0.05)  # Op�nienie
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


def display_text_on_matrix(text):
    """
    Funkcja pomocnicza do uruchomienia przewijaj�cego si� tekstu na macierzy.
    """
    try:
        run_text = RunText(text=text)
        run_text.run()
    except KeyboardInterrupt:
        print("Zamykanie programu.")