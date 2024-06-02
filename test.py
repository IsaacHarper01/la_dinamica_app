# from pyzxing import BarCodeReader
# import os

# general_path = os.path.dirname(os.path.abspath(__file__).replace('\\','/'))
# file = general_path + "/2024-05-28 13.45.46.jpg"
# print(file)
# reader = BarCodeReader()
# decoded_objects = reader.decode(file)

# if decoded_objects:
#             qr_code_data = decoded_objects[0].parsed
#             print(qr_code_data)

import sqlite3
import os
from datetime import date

general_path = os.path.dirname(os.path.abspath(__file__).replace('\\','/'))
present_date = date.today().strftime("%d-%m-%Y")

conn = sqlite3.connect(f"{general_path}/data/alumnos.db")
c = conn.cursor()
query2 = 'SELECT "%s" FROM payments'%present_date
c.execute(query2)
data = c.fetchall()

total = sum(num[0] for num in data)
print(total)
    