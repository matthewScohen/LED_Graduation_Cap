import time
import board
import busio
import adafruit_nunchuk

def main():
    device_is_setup = False
    while True:
        while not device_is_setup:
            try:
                print("Setting up nunchuck")
                i2c = busio.I2C(board.GP27, board.GP26) # I2C0 => GP27 = SCL, GP26 = SDA
                nc = adafruit_nunchuk.Nunchuk(i2c)
                device_is_setup = True
            except Exception as e:
                # print("No device found, please connect nunchuck")
                print(e)
                i2c.deinit()
        while device_is_setup:
            try:
                x, y = nc.joystick
                ax, ay, az = nc.acceleration
                c_pressed = nc.buttons.C
                z_pressed = nc.buttons.Z
                print(f"joystick={x},{y} c={c_pressed} z={z_pressed} accceleration {ax=}, {ay=}, {az=}")
            except Exception as e:
                print(e)
                i2c.deinit()
                device_is_setup = False
        # time.sleep(0.5)   

if __name__ == "__main__":
    main()