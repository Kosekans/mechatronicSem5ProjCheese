import serial 
chaesAntrieb = serial.Serial(port='COM2', baudrate=9600, timeout=.1) 
chaesZielsyste, = serial.Serial(port='COM2', baudrate=9600, timeout=.1)

def main():
    return

def writeSerial(x: str, arduino: serial):
    arduino.write(bytes(x, 'utf-8'))

def readSerialLine(arduino: serial):
    data: str = arduino.readLine()
    return data

if __name__ == "__main__":
    main()