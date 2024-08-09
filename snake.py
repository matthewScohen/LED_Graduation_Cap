import random

JOYSTICK_THRESHOLD      = 20
JOYSTICK_MIDDLE         = 130
last_input = "down"

def tick(joystick_x, joystick_y, snake_parts, fruit):
    global last_input
    if joystick_x == None or joystick_y == None:
        print("snake.tick called with no input")
    elif joystick_x < JOYSTICK_MIDDLE - JOYSTICK_THRESHOLD:
        # prevent moving into self
        if last_input == "right":
            return update_game(last_input, snake_parts, fruit)
        else:
            last_input = "left"
            return update_game("left", snake_parts, fruit)
    elif joystick_x > JOYSTICK_MIDDLE + JOYSTICK_THRESHOLD:
        # prevent moving into self
        if last_input == "left":
            return update_game(last_input, snake_parts, fruit)
        else:
            last_input = "right"
            return update_game("right", snake_parts, fruit)
    elif joystick_y > JOYSTICK_MIDDLE + JOYSTICK_THRESHOLD:
        if last_input == "down":
            return update_game(last_input, snake_parts, fruit)
        else:
            last_input = "up"
            return update_game("up", snake_parts, fruit)
    elif joystick_y < JOYSTICK_MIDDLE - JOYSTICK_THRESHOLD:
        if last_input == "up":
            return update_game(last_input, snake_parts, fruit)
        else:
            last_input = "down"
            return update_game("down", snake_parts, fruit)
    else:
        return update_game(last_input, snake_parts, fruit)

def update_game(input, snake_parts, fruit):
    global last_input
    snake_head = snake_parts[0]
    if input == "left":
        new_head = (snake_head[0], snake_head[1] - 1)
    elif input == "right":
        new_head = (snake_head[0], snake_head[1] + 1)
    elif input == "down":
        new_head = (snake_head[0] + 1, snake_head[1])
    elif input == "up":
        new_head = (snake_head[0] - 1, snake_head[1])
    else:
        new_head = snake_head
    # Check out of bounds
    if new_head[0] > 15 or new_head[0] < 0 or new_head[1] > 15 or new_head[1] < 0:
        return reset_game()

    # Check moving into self
    if new_head in snake_parts[1:]:
        return reset_game()

    if new_head[0] == fruit[0] and new_head[1] == fruit[1]:
        # Extend snake
        snake_parts.insert(0, new_head)
        fruit = [random.randint(0, 15), random.randint(0, 15)]
    else:
        # Move snake
        for i in range(len(snake_parts)-1, 0, -1):
            snake_parts[i] = snake_parts[i-1]
        snake_parts[0] = new_head
    
    print(snake_parts, fruit)
    return snake_parts, fruit

def reset_game():
    print("resetting snake game")
    snake_parts = [(5,5)] # List of snake positions as tuples (row, col)
    fruit = [5, 10]
    return snake_parts, fruit