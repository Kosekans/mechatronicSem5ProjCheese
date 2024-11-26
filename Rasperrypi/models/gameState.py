from typing import List

class GameState:
    def __init__(self):
        self.started: bool = False
        self.chaesAntriebCoords: str = None
        self.chaesAntriebModus: str = None
        self.goalCoords: List[int] = None
        self.goalCoordsVelo: int = None
        self.gameMode: str = None

    def goalCoordsToString(self):
        return "{}/{}/{}".format(self.goalCoords[0], self.goalCoords[1], self.goalCoordsVelo)
