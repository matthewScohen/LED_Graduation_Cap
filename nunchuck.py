import busio
import board
import adafruit_nunchuk

def setup_nunchuck():
    nc = None
    i2c = None
    nunchuck_ready =  False
    try:
        print(f"Setting up nunchuck... {nunchuck_ready=}")
        i2c = busio.I2C(board.GP27, board.GP26) # I2C0 => GP27 = SCL, GP26 = SDA
        nc = adafruit_nunchuk.Nunchuk(i2c)
        nunchuck_ready = True
    except Exception as e:
        # print("No device found, please connect nunchuck")
        i2c.deinit()
    return nc, i2c, nunchuck_ready
    