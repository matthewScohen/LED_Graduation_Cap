import random
import math
from symbols import *
MATRIX_WIDTH = 16
MATRIX_HEIGHT = 16

def clear_pixels(pixels, color=None):
    if color == None:
        for i in range(MATRIX_HEIGHT * MATRIX_WIDTH):
            pixels[i] = off
    else:
        for i in range(MATRIX_HEIGHT * MATRIX_WIDTH):
            pixels[i] = color

def concat_letters(letters):
    height = len(letters[0])
    word = []
    for i in range(height):
        row = []
        for letter in letters:
            row += letter[i]
            row.append(0)
        word.append(row)
    return word

def set_pixel(row, col, color, pixels):
    pixels[grid_to_serial(row, col)] = color

def grid_to_serial(row, col):
    # return 16 * col + row if col % 2 == 0 else 16 * (col + 1) - (row + 1)
    return 255 - (15 - row) - 16 * col if col % 2 == 0 else 224 - 16 * (col-1) + (15-row)


def draw_letter(row_offset, col_offset, letter, color, pixels):
    for row in range(len(letter)):
        for col in range(len(letter[row])):
            if letter[row][col] == 1:
                pixels[grid_to_serial(row + row_offset, col + col_offset)] = color
            else:
                pixels[grid_to_serial(row + row_offset, col + col_offset)] = (0, 0, 0)

def show_message(message, color, index, pixels):
    message_width = len(message[0])
    message_height = len(message)

    for row in range(message_height):
        for col in range(MATRIX_WIDTH):
                if message[row][(col + index) % message_width] == 1:
                    pixels[grid_to_serial(row, col)] = color
                else:
                    pixels[grid_to_serial(row, col)] = (0, 0, 0)

def draw_UF_2023(pixels):
    draw_letter(1, 2, U, blue, pixels)
    draw_letter(1, 9, F, blue, pixels)
    draw_letter(8, 1, char_2_big, orange, pixels)
    draw_letter(8, 9, char_3_big, orange, pixels)

def draw_UF_2024(pixels):
    draw_letter(1, 2, U, blue, pixels)
    draw_letter(1, 9, F, blue, pixels)
    draw_letter(8, 1, char_2_big, orange, pixels)
    draw_letter(8, 9, char_4_big, orange, pixels)

def draw_ECE(pixels):
    draw_letter(1, 2, U, blue, pixels)
    draw_letter(1, 9, F, blue, pixels)
    
    draw_letter(8, 0, E, orange, pixels)
    draw_letter(8, 6, C_small, orange, pixels)
    draw_letter(8, 11, E, orange, pixels)

def draw_thanks(pixels, current_frame):
    draw_letter(1, 2, T_small, purple, pixels)
    draw_letter(1, 6, H_small, purple, pixels)
    draw_letter(1, 11, X_small, purple, pixels)

    animation_length = 20
    current_frame = current_frame % animation_length
    if current_frame <= animation_length / 2:
        draw_letter(7, 1, M, blue, pixels)
        draw_letter(7, 6, O, blue, pixels)
        draw_letter(7, 11, M, blue, pixels)
    elif current_frame > animation_length / 2: 
        draw_letter(7, 1, D, orange, pixels)
        draw_letter(7, 6, A, orange, pixels)
        draw_letter(7, 11, D, orange, pixels)
    else:
        print("Frame error in draw_thanks animation")

def draw_random_colors(pixels):
    for i in range(len(pixels)):
        pixels[i] = get_random_color()

def draw_spinning_square(pixels, current_frame):
    animation_length = 20
    current_frame = current_frame % animation_length

    angle = current_frame * math.pi / 20   
    for row in range(MATRIX_HEIGHT):
        for col in range(MATRIX_WIDTH):
            if SPIRAL[row][col] == 1:
                new_row, new_col = calc_rotation(row, col, 8, 8, angle)
                if new_row >= 0 and new_row < MATRIX_HEIGHT and new_col >= 0 and new_col < MATRIX_WIDTH:
                    pixels[grid_to_serial(new_row, new_col)] = blue
            if SPIRAL[row][col] == 2:
                new_row, new_col = calc_rotation(row, col, 8, 8, angle)
                if new_row >= 0 and new_row < MATRIX_HEIGHT and new_col >= 0 and new_col < MATRIX_WIDTH:
                    pixels[grid_to_serial(new_row, new_col)] = orange

def draw_spinning_filled_square(pixels, current_frame):
    angle = current_frame * math.pi / 20   
    for row in range(MATRIX_HEIGHT):
        for col in range(MATRIX_WIDTH):
            if row > 3 and row < 12 and col > 3 and col < 12:
                new_row, new_col = calc_rotation(row, col, 7, 7, angle)
                pixels[grid_to_serial(new_row, new_col)] = get_random_color()

def update_ball_bounce(ball_row, ball_col, ball_vel_row, ball_vel_col):
    ball_parts = [
        (ball_row, ball_col),
        (ball_row+1, ball_col),
        (ball_row-1, ball_col),
        (ball_row, ball_col+1),
        (ball_row, ball_col-1),
        (ball_row+1, ball_col+1),
        (ball_row+1, ball_col-1),
        (ball_row-1, ball_col+1),
        (ball_row-1, ball_col-1),
    ]
    for ball_part in ball_parts:
        ball_part_row = ball_part[0]
        ball_part_col = ball_part[1]
        if ball_part_row + ball_vel_row < 0 or ball_part_row + ball_vel_row + 1 > MATRIX_HEIGHT:
            ball_vel_row *= -1
        if ball_part_col + ball_vel_col < 0 or ball_part_col + ball_vel_col + 1 > MATRIX_WIDTH:
            ball_vel_col *= -1
    
    print(f"{ball_vel_row=}, {ball_vel_col=}")
    ball_row += ball_vel_row
    ball_col += ball_vel_col


    return ball_row, ball_col, ball_vel_row, ball_vel_col

def draw_ball_bounce(pixels, ball_row, ball_col):
    print(f"{ball_row=}, {ball_col=}")
    pixels[grid_to_serial(ball_row, ball_col)] = blue
    pixels[grid_to_serial(ball_row+1, ball_col)] = blue
    pixels[grid_to_serial(ball_row-1, ball_col)] = blue
    pixels[grid_to_serial(ball_row, ball_col+1)] = blue
    pixels[grid_to_serial(ball_row, ball_col-1)] = blue
    pixels[grid_to_serial(ball_row+1, ball_col+1)] = blue
    pixels[grid_to_serial(ball_row+1, ball_col-1)] = blue
    pixels[grid_to_serial(ball_row-1, ball_col+1)] = blue
    pixels[grid_to_serial(ball_row-1, ball_col-1)] = blue

def calc_rotation(row, col, shift_row, shift_col, angle):
    cos = math.cos(angle)
    sin = math.sin(angle)
    # Shift to origin
    new_row = row - shift_row
    new_col = col - shift_col
    # Rotate
    new_row = (new_row * cos + new_col * sin)
    new_col = (new_col * cos - new_row * sin) 
    # Shift back
    new_row = new_row + shift_row
    new_col = new_col + shift_col
    # Round
    new_row = round(new_row)
    new_col = round(new_col)

    return new_row, new_col

def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def draw_slide_along(pixels, current_frame, length=5):
    current_frame = current_frame % 255
    for i in range(length):
        pixels[(current_frame + i) % 255] = get_random_color()

    return True if current_frame == 254 else False
    
def draw_gator_head(pixels):
    for row in range(MATRIX_HEIGHT):
        for col in range(MATRIX_WIDTH):
            if GATOR_HEAD[row][col] == 1:
                pixels[grid_to_serial(row, col)] = blue
            elif GATOR_HEAD[row][col] == 2:
                pixels[grid_to_serial(row, col)] = orange
            elif GATOR_HEAD[row][col] == 3:
                pixels[grid_to_serial(row, col)] = white
            elif GATOR_HEAD[row][col] == 4:
                pixels[grid_to_serial(row, col)] = green
            else:
                pixels[grid_to_serial(row, col)] = (0, 0, 0)

def draw_expanding_cube(pixels, current_frame):
    current_frame = current_frame % 16
    for i in range(current_frame):
        for j in range(current_frame):
            if i % 2 and j % 2 == 0:
                pixels[grid_to_serial(i, j)] = blue
            elif i % 2 or j % 2 == 0:
                pixels[grid_to_serial(i, j)] = orange
            else:
                pixels[grid_to_serial(i, j)] = blue
            # pixels[grid_to_serial(i, j)] = get_random_color()