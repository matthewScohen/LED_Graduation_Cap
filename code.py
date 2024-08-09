import time
import sys
import board # type: ignore
import neopixel
import nunchuck
import snake
from animations import *

MAX_ANIMATION = 10
JOYSTICK_THRESHOLD      = 60
JOYSTICK_MIDDLE         = 130

# Snake game variables
snake_parts, fruit = snake.reset_game()
# Ball Bounce Variables
ball_col = 9
ball_row = 8
ball_vel_row = 2
ball_vel_col = 1

slide_length = 3
def main():
    # Set up LEDs
    num_pixels = 256
    pixels = neopixel.NeoPixel(board.GP19, num_pixels, auto_write=False)
    pixels.brightness = 0.05

    current_animation = 0
    current_frame = 0
    # Snake variables
    # Set up nunchuck
    while True:
        current_frame = increment_animation(current_animation, current_frame, pixels, frame_rate=0.1)
        nc, i2c, nunchuck_ready = nunchuck.setup_nunchuck()
        while nunchuck_ready:
                try:
                    # Get nunchuck inputs
                    x, y = nc.joystick
                    ax, ay, az = nc.acceleration
                    c_pressed = nc.buttons.C
                    z_pressed = nc.buttons.Z
                    print(f"joystick={x},{y} c={c_pressed} z={z_pressed} accceleration {ax=}, {ay=}, {az=}")
                    # Update brightness
                    if current_animation == 0 and z_pressed:
                        pixels.brightness = pixels.brightness + 0.1 if pixels.brightness < 0.7 else 0.1
                    # Update state
                    if c_pressed:
                        current_animation = current_animation + 1 if current_animation < MAX_ANIMATION else 0
                        clear_pixels(pixels)
                        time.sleep(0.1) # Debounce button press
                except Exception as e:
                    print(e)
                    i2c.deinit()
                    nunchuck_ready = False
                current_frame = increment_animation(current_animation, current_frame, pixels, frame_rate=0.1, joystick_x=x, joystick_y=y)

def show_current_animation(current_animation, pixels, current_frame, joystick_x=JOYSTICK_MIDDLE, joystick_y=JOYSTICK_MIDDLE):
    print(f"{current_animation=}")
    global snake_parts, fruit, ball_row, ball_col, ball_vel_row, ball_vel_col, slide_length
    if current_animation == 0:
        draw_UF_2024(pixels) 
    elif current_animation == 1:
        draw_ECE(pixels)
    elif current_animation == 2:
        draw_thanks(pixels, current_frame)
    elif current_animation == 3:
        snake_parts, fruit = snake.tick(joystick_x, joystick_y, snake_parts, fruit)
        clear_pixels(pixels, blue)
        draw_snake_game(pixels, snake_parts, fruit)
        time.sleep(0.1)
    elif current_animation == 4:
        draw_random_colors(pixels)
    elif current_animation == 5:
        clear_pixels(pixels)
        draw_spinning_square(pixels, current_frame)
    elif current_animation == 6:
        clear_pixels(pixels)
        draw_spinning_filled_square(pixels, current_frame)
    elif current_animation == 7:
        clear_pixels(pixels)
        ball_row, ball_col, ball_vel_row, ball_vel_col = update_ball_bounce(ball_row, ball_col, ball_vel_row, ball_vel_col)
        draw_ball_bounce(pixels, ball_row, ball_col)
    elif current_animation == 8:
        draw_gator_head(pixels)
    elif current_animation == 9:
        clear_pixels(pixels)
        draw_expanding_cube(pixels, current_frame)
        slide_length = 3
    elif current_animation == 10:
        clear_pixels(pixels)
        incremenet_length = draw_slide_along(pixels, current_frame, length=slide_length)
        if incremenet_length:
            slide_length += 1
    else:
        print("invalid animation index")
    pixels.show() 

def increment_animation(current_animation, current_frame, pixels, frame_rate=0.1, joystick_x=JOYSTICK_MIDDLE, joystick_y=JOYSTICK_MIDDLE):
    show_current_animation(current_animation, pixels, current_frame, joystick_x=joystick_x, joystick_y=joystick_y)
    new_frame = current_frame + 1 if current_frame + 1 < sys.maxsize else 0
    time.sleep(frame_rate)
    return new_frame

def draw_snake_game(pixels, snake_parts, fruit):
    for snake_part in snake_parts:
        pixels[grid_to_serial(snake_part[0], snake_part[1])] = orange
    pixels[grid_to_serial(fruit[0], fruit[1])] = red

if __name__ == "__main__":
    main()