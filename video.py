from kivy.app import App
from kivy.uix.video import Video

class CameraTestApp(App):
    def build(self):
        video = Video(source='v4l2:///dev/video0', play=True)
        return video

if __name__ == "__main__":
    CameraTestApp().run()
