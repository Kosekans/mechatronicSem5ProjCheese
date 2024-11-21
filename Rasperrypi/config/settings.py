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
    'TITLE': 'chäääääs',
    'QML_MAIN_FILE': 'views/qml/main.qml',
    'BUTTON_LAYOUT': {
        'COLUMNS': 3,
        'ROWS': 2,
        'BUTTON_LABELS': [
            'Mode 1', 'Mode 2', 'Mode 3', 
            'Coords 1', 'Coords 2', 'Coords 3'
        ]
    }
}

GAME_SETTINGS = {
    'ZIELSYSTEM_VELOCITY': [10, 100, 300]
}