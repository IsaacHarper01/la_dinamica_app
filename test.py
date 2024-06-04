# from kivy.app import App
# from kivy.lang.builder import Builder
# from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.clock import Clock

# Builder.load_file('qrapp.kv')

# class scanner(Screen):

#     def on_enter(self):
#         try:
#             Clock.schedule_interval(self.scan_qr, 1.0 / 5.0)
#         except Exception as e:
#             print(f"Error starting camera: {e}")

#     def stop_camera(self):
#         try:
#             self.ids.qrcodecam.play = False
#             Clock.unschedule(self.scan_qr)
#         except Exception as e:
#             print(f"Error stopping camera {e}")

#     def scan_qr(self,dt):
#         self.ids.qrcodecam.play = True
#         if len(self.ids.qrcodecam.symbols)>0:
#             decoded_data = str(self.ids.qrcodecam.symbols[0].data)
#             self.ids.qr_label.text = decoded_data
#             self.stop_camera()
    
#     def scan_again(self):
#         self.on_enter()
# class home(Screen):
#     pass
# class Navegar(ScreenManager):
#     pass

# class Application(App):
    
#     def build(self):
#         kv = ScreenManager()
#         kv.add_widget(home(name='1'))
#         kv.add_widget(scanner(name='2'))
#         return kv
    
# if __name__ == '__main__':
#     Application().run()     
        
import sqlite3
from datetime import datetime
import os 
from plyer import storagepath
import csv


documents_folder = storagepath.get_documents_dir()
general_path = os.path.dirname(os.path.abspath(__file__).replace('\\','/'))

def get_csv(s_day,s_month,s_year,e_day,e_month,e_year):
    file_name = f"Report_{s_day}_{s_month}_{s_year}--{e_day}_{e_month}_{e_year}.csv"
    conn = sqlite3.connect(f"{general_path}/data/alumnos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance LIMIT 1")
    columns_selected = [datetime.strptime(col[0],"%d-%m-%Y") for col in cursor.description[4:]]
    
    start = datetime.strptime(f"{str(s_day)}-{str(s_month)}-{str(s_year)}","%d-%m-%Y")
    end = datetime.strptime(f"{str(e_day)}-{str(e_month)}-{str(e_year)}","%d-%m-%Y")

    period_columns = [date1.strftime("%d-%m-%Y") for date1 in columns_selected if start<=date1<=end]
    data_columns = ["name","age","address"]
    complete_data = data_columns+period_columns
    columns_str = ", ".join([f'"{column}"' for column in complete_data])
    
    cursor.execute(f'SELECT {columns_str} FROM attendance')
    data_rows = cursor.fetchall()
    if len(period_columns)>0:
        with open(f'{documents_folder}/{file_name}', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(complete_data)
            csvwriter.writerows(data_rows)
    else:
        print("No data in database")
    conn.close()


get_csv(1,7,2024,30,7,2024)

