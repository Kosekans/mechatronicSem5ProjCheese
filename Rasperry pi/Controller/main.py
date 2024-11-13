import array


def main():
    return

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
