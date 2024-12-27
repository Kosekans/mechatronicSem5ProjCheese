import board
import neopixel
pixels = neopixel.NeoPixel(board.D18, 4)

pixels[0] = (255, 0, 0)