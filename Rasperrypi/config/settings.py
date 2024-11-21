import serial

ARDUINO_SETTINGS = {
    'chaesAntrieb': {
        'PORT': 'COM5',#to do: find the correct port on raspy
        'BAUD_RATE': 9600,
        'TIMEOUT': 1,
        'BYTESIZE':serial.EIGHTBITS
    },
    'chaesZielsystem': {
        'PORT': 'COM6',
        'BAUD_RATE': 9600,
        'TIMEOUT': 1,
        'BYTESIZE':serial.EIGHTBITS
    }
}


QML_SETTINGS = {
    'WINDOW_WIDTH': 800,
    'WINDOW_HEIGHT': 600,
    'TITLE': 'chääääääääääääääääääääääääs',
    'QML_MAIN_FILE': 'views/qml/main.qml'
}

GAME_SETTINGS = {
    'ZIELSYSTEM_VELOCITY': [10, 100, 300]
}