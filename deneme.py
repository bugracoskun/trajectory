from datetime import time
from datetime import datetime

datee='2020-12-10 00:00:00'
b = datetime(2020, 12, 10, 00, 00, 00, 00)

c=b.strftime('%m-%d-%Y %H:%M:%S')
print(c)