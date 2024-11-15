from typing import List

class gameState:
    chaesAntriebCoords: str

    def __init__(self, chaesAntriebModus: str, goalCoords: List[int] = None, goalCoordsVelo: int = None):
        self.chaesAntriebModus = chaesAntriebModus
        self.goalCoords = goalCoords
        self.goalCoordsVelo = goalCoordsVelo
        self.chaesZielsystemModus = self.goalCoordsToString(goalCoords, goalCoordsVelo)

    def goalCoordsToString(self, goalCoords: List[int], velocity: int):
        return "{}/{}/{}".format(goalCoords[0], goalCoords[1], velocity)
