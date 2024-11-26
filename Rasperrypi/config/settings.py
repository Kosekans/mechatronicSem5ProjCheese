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

RASPBERRY_PI_SETTINGS = {
    'GPIO_PINS': {
        'START_BUTTON_PIN': 17, # GPIO17 physical pin 11
        'LIGHT_BARRIER_PIN': 18 # GPIO18 physical pin 12
    },
    'OS_USERNAME': 'raspberrypi'
}

QML_SETTINGS = {
    'TITLE': 'chäääääs'
}

GAME_SETTINGS = {
    'ZIELSYSTEM_VELOCITY': [10, 100, 300]
}