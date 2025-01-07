import sys
import os

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to the system path
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from config.settings import GAME_SETTINGS

class GameState:
    def __init__(self):
        self.portsFound: bool = False
        self.hardwareInitialized: bool = False
        self.active: bool = False
        self.chaesAntriebCoords: str = None
        self.chaesAntriebModus: str = None
        self.goalCoords: list[int] = None
        self.goalCoordsVelo: int = None
        self.gameMode: str = None
        self.inverseSticks: bool =  GAME_SETTINGS['GAME_BOOLS_DEFAULT']['inverseSticksDefault']
        self.rocketVelocity: float = GAME_SETTINGS['GAME_VALUES_DEFAULT']['rocketVelocityDefault'] #[0,1]
        self.latency: int = GAME_SETTINGS['GAME_VALUES_DEFAULT']['latencyDefault']  #ms
        self.randomInverseSticks: bool = GAME_SETTINGS['GAME_BOOLS_DEFAULT']['randomInverseSticksDefault']
        self.randomRocketVelocity: bool = GAME_SETTINGS['GAME_BOOLS_DEFAULT']['randomRocketVelocityDefault']
        self.randomLatency: bool = GAME_SETTINGS['GAME_BOOLS_DEFAULT']['randomLatencyDefault']
        self.ballInRocket: bool = False
        self.arduinoBusy: bool = False
        
    def reset(self):
        self.portsFound: bool = False
        self.hardwareInitialized: bool = False
        self.active: bool = False
        self.chaesAntriebCoords: str = None
        self.chaesAntriebModus: str = None
        self.goalCoords: list[int] = None
        self.goalCoordsVelo: int = None
        self.gameMode: str = None
        self.inverseSticks: bool =  GAME_SETTINGS['GAME_BOOLS_DEFAULT']['inverseSticksDefault']
        self.rocketVelocity: float = GAME_SETTINGS['GAME_VALUES_DEFAULT']['rocketVelocityDefault'] #[0,1]
        self.latency: int = GAME_SETTINGS['GAME_VALUES_DEFAULT']['latencyDefault']  #ms
        self.randomInverseSticks: bool = GAME_SETTINGS['GAME_BOOLS_DEFAULT']['randomInverseSticksDefault']
        self.randomRocketVelocity: bool = GAME_SETTINGS['GAME_BOOLS_DEFAULT']['randomRocketVelocityDefault']
        self.randomLatency: bool = GAME_SETTINGS['GAME_BOOLS_DEFAULT']['randomLatencyDefault']
        self.ballInRocket: bool = False
        self.arduinoBusy: bool = False

    def goalCoordsToString(self):
        return "{}/{}/{}".format(self.goalCoords[0], self.goalCoords[1], self.goalCoordsVelo)
    
    def getInfoForAntrieb(self):
        return (
            "{}/{}/{}/{}/{}/{}".format(
            int(self.inverseSticks),
            self.rocketVelocity,
            self.latency,
            int(self.randomInverseSticks),
            int(self.randomRocketVelocity),
            int(self.randomLatency)
            )
        )