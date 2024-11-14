import serial

class Com:
    def __init__(self, prt: str, brate: int, tout, arduino: serial):
        self.arduino = serial.Serial(port=prt, baudrate=brate, timeout=tout)
    
    def writeSerial(self, x: str):
        self.arduino.write(bytes(x, 'utf-8'))

    def readSerialLine(self):
        data: str = self.arduino.readLine()#.decode('utf-8').strip()
        return data