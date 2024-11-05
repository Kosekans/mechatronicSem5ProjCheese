import array


def main():
    print(calculateCoords(35, 30, 40))
    return


def calculateCoords(distance: float, left: float, right: float):
    angle: float = (left * distance) / (left * left + right * right)
    x: float = left * angle
    y: float = right * angle
    coords = array.array('f', [x, y])
    return coords


def boxCoords(x: float, y: float, leftBorder: float, rightBorder: float, lowerBorder: float, upperBorder: float):
    if x < leftBorder:
        x = lowerBorder
    if x > rightBorder:
        x = rightBorder
    if y < lowerBorder:
        y = lowerBorder
    if y > upperBorder:
        y = upperBorder
    coords = array.array('f', [x, y])
    return coords


def mapFloat(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


if __name__ == "__main__":
    main()
