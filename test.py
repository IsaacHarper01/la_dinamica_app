from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy_garden.zbarcam import ZBarCam
from kivy_garden.xcamera import XCamera
import sqlite3
import os 
import sys 

Builder.load_file('qrapp.kv')

class scanner(Screen):

    def on_enter(self):
    
        self.cam = ZBarCam()
        self.ids.qrcodecam.add_widget(self.cam)
        Clock.schedule_interval(self.scan_qr, 1)
        self.cam.start()

    def on_leave(self):
        self.cam.stop()
        self.ids.qrcodecam.remove_widget(self.cam)
        self.cam.ids.xcamera._camera.stopped = True
        
        mod_path = os.path.dirname(sys.modules['kivy_garden.zbarcam'].__file__)
        zbar_kv_path = os.path.join(mod_path, 'zbarcam.kv')           
        Builder.unload_file(zbar_kv_path) 

        mod_path = os.path.dirname(sys.modules['kivy_garden.xcamera'].__file__)
        xcam_kv_path = os.path.join(mod_path, 'xcamera.kv')
        Builder.unload_file(xcam_kv_path)
        
    def stop_camera(self):
        try:
            self.cam.play = False
            Clock.unschedule(self.scan_qr) 
        except Exception as e:
            print(f"Error stopping camera {e}")

    def scan_qr(self,dt):
        self.cam.play = True
        if len(self.cam.symbols)>0:
            decoded_data = str(self.cam.symbols[0].data)
            self.ids.qr_label.text = decoded_data
            self.stop_camera()
    
    def scan_again(self):
        self.cam.play= True
        Clock.schedule_interval(self.scan_qr, 1)
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

# cam = ZBarCam()
# print(dir(cam.ids.xcamera._camera))

# source_code = inspect.getsource(device.release)
# print(source_code)

# import sqlite3
# from datetime import datetime
# import os 
# from plyer import storagepath
# import csv
# from fpdf import FPDF
# import qrcode

# documents_folder = storagepath.get_documents_dir()
# general_path = os.path.dirname(os.path.abspath(__file__).replace('\\','/'))

# def get_csv(s_day,s_month,s_year,e_day,e_month,e_year):
#     file_name = f"Report_{s_day}_{s_month}_{s_year}--{e_day}_{e_month}_{e_year}.csv"
#     conn = sqlite3.connect(f"{general_path}/data/alumnos.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM attendance LIMIT 1")
#     columns_selected = [datetime.strptime(col[0],"%d-%m-%Y") for col in cursor.description[4:]]
    
#     start = datetime.strptime(f"{str(s_day)}-{str(s_month)}-{str(s_year)}","%d-%m-%Y")
#     end = datetime.strptime(f"{str(e_day)}-{str(e_month)}-{str(e_year)}","%d-%m-%Y")

#     period_columns = [date1.strftime("%d-%m-%Y") for date1 in columns_selected if start<=date1<=end]
#     data_columns = ["name","age","address"]
#     complete_data = data_columns+period_columns
#     columns_str = ", ".join([f'"{column}"' for column in complete_data])
    
#     cursor.execute(f'SELECT {columns_str} FROM attendance')
#     data_rows = cursor.fetchall()
#     if len(period_columns)>0:
#         with open(f'{documents_folder}/{file_name}', 'w', newline='') as csvfile:
#             csvwriter = csv.writer(csvfile)
#             csvwriter.writerow(complete_data)
#             csvwriter.writerows(data_rows)
#     else:
#         print("No data in database")
#     conn.close()

# def edit_register():
#     conn = sqlite3.connect(f"{general_path}/data/alumnos.db")
#     cursor = conn.cursor()
#     query = 'UPDATE registros SET'

# def generate_QR(name,id,age,address,phone):
#     text = f'nombre:{name},id:{id},Edad:{age},localidad:{address},telefono:{phone}'
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(text)
#     qr.make(fit=True)
#     qr_img = qr.make_image(fill_color="black", back_color="white")
#     file_name = f"QR_{name}.png"
#     path = f"{general_path}/data/{file_name}"
#     qr_img.save(path)
#     return file_name

# def generate_pdf(QR_name,name,id,phone):
#     logo_path = f"{general_path}/data/f=ma11.png"
#     QR_path = f"{general_path}/data/{QR_name}"
#     responsiva_path = f"{general_path}/data/responsiva.jpg"
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Times","B",11)
#     pdf.multi_cell(58,12,f"Nombre:{name} \nNúmero de alumno: {id} \nTelefono: {phone}",0,align='L')
#     pdf.rect(10,10,58,48)#data rectangle
#     pdf.rect(68,10,43,48)#QR rectangle
#     pdf.rect(111,10,90,48)#logo rectangle
#     pdf.dashed_line(0,70,212,70,2,1)
#     pdf.line(60,280,160,280)
#     pdf.text(95,285,"Firma del tutor")
#     pdf.image(QR_path,68,13,42,42)
#     pdf.image(logo_path,132,13,50,45)#credential
#     pdf.image(logo_path,160,65,43,55)#responsive
#     pdf.image(responsiva_path,20,100,180,160)
#     pdf.output(f"{documents_folder}/{name}.pdf","F")
#     os.remove(QR_path)

#get_csv(1,7,2024,30,7,2024)
# name = "Derek Adrian Ortega Rivera"
# phone = "5516489139"
# qr_name = generate_QR(name,8,11,"Santa Teresa 3",phone)
# generate_pdf(qr_name,name,8,phone)