from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock

from PIL import Image
from pyzbar.pyzbar import decode

Builder.load_file('qrapp.kv')

class scanner(Screen):

    def on_enter(self):
        try:
            self.ids.camera.play= True
            Clock.schedule_interval(self.scan_qr, 1.0 / 10.0)
        except Exception as e:
            print(f"Error starting camera: {e}")

    def stop_camera(self):
        try:
            self.ids.camera.play = False
            Clock.unschedule(self.scan_qr)
        except Exception as e:
            print(f"Error stopping camera {e}")

    def scan_qr(self,dt):
        texture = self.ids.camera.texture
        if texture:
            size = texture.size
            buffer = texture.pixels
            image = Image.frombytes(mode='RGBA',size=size,data=buffer)
            decoded_image = decode(image)
            if decoded_image:
                self.stop_camera()
                qr_data = str(decoded_image[0].data.decode('utf-8'))
                self.ids.qr_label.text = qr_data
class home(Screen):
    pass
class Navegar(ScreenManager):
    pass

class Application(App):
    
    def build(self):
        kv = ScreenManager()
        kv.add_widget(home(name='1'))
        kv.add_widget(scanner(name='2'))
        return kv
    
if __name__ == '__main__':
    Application().run()     
        



