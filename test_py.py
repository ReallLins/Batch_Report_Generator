import time
from datetime import datetime

stamp = time.time()
print(stamp)
now = datetime.fromtimestamp(stamp)
now_time = now.strftime("%Y-%m-%d %H:%M:%S")
a = now_time
print(now)
print(now_time)
print(type(now))
print(type(now_time))
print(type(a))
print(a == now_time)