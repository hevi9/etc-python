import bluetooth
lso = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
print(lso.getsockname())
lso.close()