from pyzxing import BarCodeReader
import os

general_path = os.path.dirname(os.path.abspath(__file__).replace('\\','/'))
file = general_path + "/2024-05-28 13.45.46.jpg"
print(file)
reader = BarCodeReader()
decoded_objects = reader.decode(file)

if decoded_objects:
            qr_code_data = decoded_objects[0].parsed
            print(qr_code_data) 