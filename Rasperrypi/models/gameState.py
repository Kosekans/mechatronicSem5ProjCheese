from typing import List

class GameState:
    chaesAntriebCoords: str
    chaesAntriebModus: str
    goalCoords: List[int]
    goalCoordsVelo: int

    def __init__(self, started: bool = None):
        self.started: bool = False

    def goalCoordsToString(self):
        return "{}/{}/{}".format(self.goalCoords[0], self.goalCoords[1], self.goalCoordsVelo)
