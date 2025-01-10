# mechatronicSem5ProjCheese
# Cheese Robot Project

A mechatronics project combining Arduino-controlled motors with a Raspberry Pi user interface for an interactive robotic game system.

## System Overview

The project consists of two main components:

### Hardware Components
- 2 Arduino Mega boards:
  - chaesAntrieb: Controls motor movements and LED displays
  - chaesZielsystem: Manages servo positioning system
- Raspberry Pi: Runs the main control interface and game logic
- Motors, servos, and LED strips for visual feedback
- Custom PCB and mechanical assembly

### Software Components
- Arduino firmware for motor and servo control
- Python-based GUI application using PyQt5/QML
- Serial communication interface between Raspberry Pi and Arduinos
- Game modes and interactive features

## Features

- Multiple game modes:
  - Follow mode
  - Goal mode
  - Infinity mode
  - Inverse Follow mode
  - Demo mode
- Configurable settings:
  - Adjustable rocket velocity
  - Inverse stick controls
  - Randomization options
  - Input latency simulation
- LED feedback system
- Hardware fail-safes and safety limits

## Installation

### Prerequisites
- Python 3.x
- Arduino IDE or PlatformIO
- Required Python packages listed in `raspberryPi/config/requirementsPython.txt`
- System packages listed in `raspberryPi/config/requirementsSystem.txt`

### Setup Instructions

1. Clone the repository:

git clone https://github.com/Kosekans/mechatronicSem5ProjCheese.git

2. Install system dependencies (Raspberry Pi):

cd raspberryPi/utils
python3 setup.py

3. Upload Arduino firmware:
    Open chaesAntrieb and chaesZielsystem in PlatformIO/Arduino IDE
    Upload to respective Arduino boards
4. Start the application:

cd raspberryPi
python3 main.py

## Project Structure
.
├── Arduinos/
│   ├── chaesAntrieb/      # Motor control Arduino
│   └── chaesZielsystem/    # Servo system Arduino
├── raspberryPi/
│   ├── config/            # Configuration files
│   ├── controllers/       # Python controllers
│   ├── models/           # Data models
│   ├── utils/            # Utility functions
│   ├── views/            # QML UI files
│   └── main.py           # Application entry point

## Development
Use PlatformIO for Arduino development
Python virtual environment recommended for Raspberry Pi development
Follow existing code style and documentation patterns
Test hardware functions carefully before deployment
License

## Acknowledgments
This project was developed as part of the mechatronics semester 5 project.