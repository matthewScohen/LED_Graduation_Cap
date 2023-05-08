import time
import board
import busio
import adafruit_nunchuk
import neopixel

def main():
    num_pixels = 256

    pixels = neopixel.NeoPixel(board.GP19, num_pixels)
    pixels.brightness = 0.1

    while True:
        pixels.fill((255, 0, 0))

if __name__ == "__main__":
    main()