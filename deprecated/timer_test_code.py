import threading
import datetime

count = 0
def funcTimer():
  global count
  print("timer!")
  print(str(count) + " " + str(datetime.datetime.now()))

  count += 1
  timer = threading.Timer(1, funcTimer)

  if count < 5:
    timer.start()
  else: 
    timer.cancel()
flag = True
while flag:
  if flag:
    flag = False
    funcTimer()
