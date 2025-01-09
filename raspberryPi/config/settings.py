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
        'START_BUTTON_PIN': 27, # GPIO27 physical pin 13   
        'BALL_FALLING_PIN': 17, # GPIO18 physical pin 12
        'BALL_EJECT_PIN': 12, # GPIO27 physical pin 32
        'START_BUTTON_LED_PIN': 22 # GPIO22 physical pin 15
    }
}

QML_SETTINGS = {
    'TITLE': 'chäääääs'
}

GAME_SETTINGS = {
    'GAME_MODES': {
        'follow': 'follow',
        'goal': 'goal',
        'infinity': 'infinity',
        'inverseFollow': 'inverseFollow',
        'demo': 'demo'
    },
    'GAME_BOOLS_DEFAULT': {
        'inverseSticksDefault': False,
        'randomInverseSticksDefault': False,
        'randomRocketVelocityDefault': False,
        'randomLatencyDefault': False
    },
    'GAME_VALUES_DEFAULT': {
        'rocketVelocityDefault': 1, #[0,1]
        'latencyDefault': 0, #ms,
        'goalCoordsVeloDefault': 300
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
    'RUNNING_GAME': 'Game is already running',
    'ARDUINOS_BUSY': 'Arduinos are not ready, wait a moment',
    'BALL_LOST': 'you lost your bagage, drive your rocket more carefully next time',
    'STAR_AWAY': 'your star run away from you, try to keep catching up next time',
    'STAR_CATCHED_UP': 'the star catched up with you, try avoiding it next time',
}
SUCCESS_MESSAGES = {
    'HARDWARE_INITIALIZED': 'Hardware initialized successfully',
    'PORTS_UPDATED': 'Ports updated successfully',
    'UPDATED': 'Repository updated successfully',
    'NULL_ANTRIEB': 'Nulling motors successfully',
    'GAME_WON': 'you won, congratulations',
    'GAME_ENDED_WITH_TIME': 'congradulations, you lasted ',
    'GAME_ENDED_WITH_NUMBER_OF_GOALS1': 'congradulations, you landed on ',
    'GAME_ENDED_WITH_NUMBER_OF_GOALS1': ' craters on the moon'
}