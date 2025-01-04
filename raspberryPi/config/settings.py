import serial

ARDUINO_SETTINGS = {
    'chaesAntrieb': {
        'ID': 'chaesAntrieb',
        'BAUD_RATE': 9600,
        'TIMEOUT': 1,  # Increased to 1 second
        'BYTESIZE': serial.EIGHTBITS,
        'CHARACTER_ENCODING': 'utf-8'
    },
    'chaesZielsystem': {
        'ID': 'chaesZielsystem',
        'BAUD_RATE': 9600,
        'TIMEOUT': 1,  # Increased to 1 second
        'BYTESIZE': serial.EIGHTBITS,
        'CHARACTER_ENCODING': 'utf-8'
    }
}

RASPBERRY_PI_SETTINGS = {
    'GPIO_PINS': {
        'START_BUTTON_PIN': 17, # GPIO17 physical pin 11
        'BALL_FALLING_PIN': 18, # GPIO18 physical pin 12
        'BALL_EJECT_PIN': 27, # GPIO27 physical pin 13
        'START_BUTTON_LED_PIN': 22 # GPIO22 physical pin 15
    },
    'OS_USERNAME': 'chaes'
}

QML_SETTINGS = {
    'TITLE': 'chäääääs'
}

GAME_SETTINGS = {
    'GAME_MODES': {
        'follow': 'follow',
        'goal': 'goal',
        'infinity': 'infinity',
        'inverseFollow': 'inverseFollow'
    },
    'GAME_BOOLS_DEFAULT': {
        'inverseSticksDefault': False,
        'randomInverseSticksDefault': False,
        'randomRocketVelocityDefault': False,
        'randomLatencyDefault': False
    },
    'GAME_VALUES_DEFAULT': {
        'rocketVelocityDefault': 1, #[0,1]
        'latencyDefault': 0 #ms
    }
}

ERROR_MESSAGES = {
    'NO_GAME_MODE_SELECTED': 'Please select Game Mode first',
    'HARDWARE_NOT_INITIALIZED': 'Comunication with Arduinos not initialized, go to settings and initialize hardware',
    'HARDWARE_INITIALIZATION_FAILED': 'Hardware initialization failed, try updating the port in settings or check the connection',
    'PORT_UPDATE_FAILED': 'Port update failed, check the connection and try again',
    'NO_PORTS_FOUND': 'No connected ports found, update the ports in settings',
    'NO_INTERNET_CONNECTION': 'No internet connection found, could not update repository. Check the connection and retart to update',
    'UPDATE_FAILED': 'Failed to update repository',
    'SUCCESS': 'passt scho, het klappt'
}