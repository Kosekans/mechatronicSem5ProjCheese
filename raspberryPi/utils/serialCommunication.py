import serial
import serial.tools.list_ports

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
                    connectedPorts.append(port.device)
                except serial.SerialException:
                    continue
            return connectedPorts
    
    @staticmethod
    def testComunication(port: str, baudRate: int, timeout: int, bytesize: serial, characterEncoding: str, message: str):
        testConnection = None
        try:
            testConnection = serial.Serial(port, baudRate, timeout=timeout, bytesize=bytesize)
            # Add small delay for Arduino to reset
            import time
            time.sleep(2)
            
            testConnection.write(bytes(message + '\n', characterEncoding))
            testConnection.flush()
            answer = testConnection.readline()
            if not answer:  # If no response received before timeout
                return "No response"
            return answer.decode(characterEncoding).strip()
        except serial.SerialException as e:
            return f"Communication Error: {str(e)}"
        finally:
            if testConnection:
                testConnection.close()