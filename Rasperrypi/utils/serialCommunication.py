import serial

class SerialCommunication:
    @staticmethod
    def create_connection(port: str, baud_rate: int, timeout: int, bytesize: serial):
        try:
            return serial.Serial(port, baud_rate, timeout=timeout, bytesize=bytesize)
        except serial.SerialException as e:
            print(f"Error connecting to {port}: {e}")
            return None