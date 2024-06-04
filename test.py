from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

Builder.load_file('qrapp.kv')

class scanner(Screen):

    def start(self):
        try:
            Clock.schedule_interval(self.scan_qr, 1.0 / 5.0)
        except Exception as e:
            print(f"Error starting camera: {e}")

    def stop_camera(self):
        try:
            self.ids.camera.play = False
            Clock.unschedule(self.scan_qr)
        except Exception as e:
            print(f"Error stopping camera {e}")

    def scan_qr(self,dt):
        self.ids.qrcodecam.play = True
        if len(self.ids.qrcodecam.symbols)>0:
            decoded_data = str(self.ids.qrcodecam.symbols[0].data)
            self.ids.qr_label.text = decoded_data
            self.ids.qrcodecam.play=False
            Clock.unschedule(self.scan_qr)
        
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
        



