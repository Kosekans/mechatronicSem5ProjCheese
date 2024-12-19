import serial
import serial.tools.list_ports
import time

class SerialCommunication:
    @staticmethod
    def create_connection(port: str, baudRate: int, timeout: int, bytesize: serial):
        try:
            return serial.Serial(port, baudRate, timeout=timeout, bytesize=bytesize)
        except serial.SerialException as e:
            print(f"Error connecting to {port}: {e}")
            return None

    @staticmethod
    def findConnectedPorts(baudRate: int, timeout: int, bytesize: serial):
            connectedPorts: list[str] = []
            availablePorts = serial.tools.list_ports.comports()
            for port in availablePorts:
                try:
                    # Test connection
                    testConnection = serial.Serial(port.device, baudRate, timeout=timeout, bytesize=bytesize)
                    testConnection.close()
                     # Only add ports that are actually USB devices
                    if port.vid is not None:  # Check if vendor ID exists
                        connectedPorts.append(port.device)
                except serial.SerialException:
                    continue
            return connectedPorts
    
    @staticmethod
    def testComunication(port: str, baudRate: int, timeout: int, bytesize: serial, characterEncoding: str, message: str):
        testConnection = None
        try:
            testConnection = serial.Serial(port, baudRate, timeout=timeout, bytesize=bytesize)
            if testConnection:
                print("created serial test connection succsesfully")
                # Add small delay for Arduino to reset
                time.sleep(0.5)
                testConnection.write(bytes(message + '\n', characterEncoding))
                print("write done")
                testConnection.flush()
                print("flush done")
                testConnection.timeout = 0.5
                answer = testConnection.readline()
                print("read done")
                if not answer:  # If no response received before timeout
                    return "no response"
                return answer.decode(characterEncoding).strip()
            else:
                return "could not create serial test connection"
        except serial.SerialException as e:
            print(f"Communication Error: {str(e)}")
            return f"Communication Error: {str(e)}"
        finally:
            if testConnection:
                testConnection.close()
                print("closed serial test connection")