from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
# from kivy.uix.label import Label
# from kivy.uix.button import Button
# from kivy_garden.zbarcam import ZBarCam

class QRScanner(BoxLayout):
    def __init__(self, **kwargs):
        super(QRScanner, self).__init__(**kwargs)
        self.orientation = 'vertical'
        # ZBarCam widget to scan QR codes
        # self.zbarcam = ZBarCam()
        # self.add_widget(self.zbarcam)
        
        # Label to display scanned QR code
        # self.qr_label = Label(text="Scanned QR code will appear here")
        # self.add_widget(self.qr_label)
        
        # Button to rescan QR code
        # self.rescan_button = Button(text="Scan Again")
        # self.rescan_button.bind(on_press=self.rescan)
        # self.add_widget(self.rescan_button)
        
        # Schedule a method to check for QR codes
        Clock.schedule_interval(self.check_qr_code, 1)

    def check_qr_code(self, dt):
        if self.zbarcam.symbols:
            qr_code_data = self.zbarcam.symbols[0].data.decode('utf-8')
            self.qr_label.text = f"QR code detected: {qr_code_data}"
            self.zbarcam.play = False  # Stop the camera after detecting a QR code

    def rescan(self, instance):
        self.zbarcam.play = True
        self.qr_label.text = "Scanned QR code will appear here"

class QRScannerApp(App):
    def build(self):
        return QRScanner()

if __name__ == '__main__':
    QRScannerApp().run()
