# import numpy as np
# import sounddevice as sd  # Biblioteka do odtwarzania d?wi?ku
# from TTS.api import TTS
#
# # Inicjalizacja modelu
# tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
#
# # Tekst do wypowiedzenia
# tekst = "To jest testowy tekst, kt�ry nie b?dzie zapisywany."
#
# # Generowanie d?wi?ku jako tablicy numpy
# audio_data = tts.synth(text=tekst)
#
# # Odtwarzanie d?wi?ku za pomoc? sounddevice
# print("Odtwarzanie mowy...")
from playsound import playsound

playsound("nagranie_wzmocnione.mp3")
