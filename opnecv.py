from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2

class CameraApp(App):
    def build(self):
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
