from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture
from pyzbar.pyzbar import decode
from PIL import Image
from kivy.properties import StringProperty, BooleanProperty

class escanear(Screen):

    text_label = StringProperty("QR code info will be shown here")
    buttons_desactived = BooleanProperty(True)
    record = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(escanear, self).__init__(**kwargs)
        self.capture = None
        self.scanning = True

    def on_enter(self):
        try:
            self.ids.camera.play = True
            Clock.schedule_interval(self.scan_for_qr, 1.0 / 5.0)
        except Exception as e:
            print(f"Error starting camera: {e}")

    def on_leave(self):
        try:
            self.ids.camera.play = False
            Clock.unschedule(self.scan_for_qr)
        except Exception as e:
            print(f"Error stopping camera: {e}")

    def scan_for_qr(self, dt):
        texture = self.ids.camera.texture
        if texture:
            size = texture.size
            buffer = texture.pixels
            image = Image.frombytes(mode='RGBA', size=size, data=buffer)
            decoded_objects = decode(image)

            if decoded_objects:
                qr_code_data = decoded_objects[0].data.decode('utf-8')
                self.manager.current = 'result'
                self.manager.get_screen('result').ids.qr_label.text = f"QR code detected: {qr_code_data}"

class ResultScreen(Screen):
    pass

class QRApp(App):
    def build(self):
        Builder.load_file('main.kv')
        sm = ScreenManager()
        sm.add_widget(escanear(name='qr_scanner'))
        sm.add_widget(ResultScreen(name='result'))
        return sm

if __name__ == '__main__':
    QRApp().run()
