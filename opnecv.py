from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
# noinspection PyInterpreter
class CameraApp(App):
    def build(self):
        # Ustawienia okna
        Window.size = (1200, 800)

        screen_w = Window.system_size[0]
        screen_h = Window.system_size[1]

        window_x = (screen_w - Window.size[0]) // 2
        window_y = (screen_h - Window.size[1]) // 2
        Window.top = window_y
        Window.left = window_x

        root = BoxLayout(orientation='vertical',spacing=10, padding=10)

        self.img_widget = Image()
        self.capture = cv2.VideoCapture(0)  # 0 oznacza pierwszą kamerę podłączoną do systemu
        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)  # 30 FPS

        return self.img_widget

    def update_frame(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Konwersja obrazu z BGR (OpenCV) na RGB (Kivy)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            buf = frame.tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.img_widget.texture = texture

    def on_stop(self):
        # Zwolnij kamerę, gdy aplikacja zostanie zamknięta
        self.capture.release()

if __name__ == "__main__":
    CameraApp().run()
