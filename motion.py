import serial
import time
import matplotlib.pyplot as plt


ser = serial.Serial(
    port='/dev/cu.usbmodem145101',\
    baudrate=115200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)
print("connected to: " + ser.portstr)
ser.open()
sleep(5)
ser.reset_input_buffer()

L = []

for i in range (5000):
    time.sleep(0.001)
    L.append(ser.readline())
    print(L[-1])


print(L)
plt.plot(L)
plt.ylabel('angles')
plt.show()

ser.close()