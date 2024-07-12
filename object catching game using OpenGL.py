from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import sys

# Window dimensions
window_width = 500
window_height = 500

# List to store falling diamonds
falling_diamonds = []

# Bowl parameters
bowl_width = 90
bowl_height = 30
bowl_x = (window_width - bowl_width) // 2
bowl_y = 0

# Button parameters
button_width = 30
button_height = 20
left_button_pos = (10, window_height - 40)
middle_button_pos = (window_width // 2 - button_width // 2, window_height - 40)
right_button_pos = (window_width - 40, window_height - 40)

# Game state
score = 0
diamond_speed = 5
game_paused = False
game_over = False



# Function to draw a diamond at a given position
def draw_diamond(x_center, y_center, length=10):
    x1, y1 = x_center, y_center + length
    x2, y2 = x_center + length, y_center
    x3, y3 = x_center, y_center - length
    x4, y4 = x_center - length, y_center

    midpoint_line_algorithm(x1, y1, x2, y2)
    midpoint_line_algorithm(x2, y2, x3, y3)
    midpoint_line_algorithm(x3, y3, x4, y4)
    midpoint_line_algorithm(x4, y4, x1, y1)


def draw_points(x, y):
    glPointSize(5)  # Pixel size, by default 1
    glBegin(GL_POINTS)
    glVertex2f(x, y)  # Show pixel at (x, y)
    glEnd()


def midpoint_line_algorithm(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    steep = dy > dx

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = abs(y2 - y1)
    error = dx / 2.0
    y = y1

    if y1 < y2:
        ystep = 1
    else:
        ystep = -1

    for x in range(int(x1), int(x2) + 1):
        if steep:
            draw_points(int(y), int(x))
        else:
            draw_points(int(x), int(y))
        error -= dy
        if error < 0:
            y += ystep
            error += dx


def iterate():
    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, window_width, 0.0, window_height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    # Draw buttons
    draw_buttons()

    # Draw bowl
    glColor3f(1.0, 1.0, 1.0)
    draw_rectangular_bowl(bowl_x, bowl_y, bowl_width, bowl_height)

    # Draw all falling diamonds
    for diamond in falling_diamonds:
        x, y, color = diamond
        glColor3f(color[0], color[1], color[2])
        draw_diamond(x, y)

    glutSwapBuffers()


def draw_rectangular_bowl(x, y, width, height):
    x2 = x + width
    y2 = y + height

    midpoint_line_algorithm(x, y, x2, y)
    midpoint_line_algorithm(x2, y, x2, y2)
    midpoint_line_algorithm(x2, y2, x, y2)
    midpoint_line_algorithm(x, y2, x, y)


def draw_buttons():
    # Draw left button (Restart)
    glColor3f(0.0, 1.0, 1.0)  # Bright teal color
    draw_arrow_button(left_button_pos[0], left_button_pos[1], button_width, button_height)

    # Draw middle button (Play/Pause)
    glColor3f(1.0, 0.75, 0.0)  # Amber color
    if game_paused:
        draw_play_button(middle_button_pos[0], middle_button_pos[1], button_width, button_height)
    else:
        draw_pause_button(middle_button_pos[0], middle_button_pos[1], button_width, button_height)

    # Draw right button (Exit)
    glColor3f(1.0, 0.0, 0.0)  # Red color
    draw_cross_button(right_button_pos[0], right_button_pos[1], button_width, button_height)


def draw_arrow_button(x, y, width, height):
    midpoint_line_algorithm(x + width, y, x, y + height // 2)
    midpoint_line_algorithm(x, y + height // 2, x + width, y + height)
    midpoint_line_algorithm(x + width, y + height, x + width, y)


def draw_play_button(x, y, width, height):
    midpoint_line_algorithm(x, y, x + width, y + height // 2)
    midpoint_line_algorithm(x + width, y + height // 2, x, y + height)
    midpoint_line_algorithm(x, y + height, x, y)


def draw_pause_button(x, y, width, height):
    bar_width = width // 3
    midpoint_line_algorithm(x, y, x + bar_width, y)
    midpoint_line_algorithm(x + bar_width, y, x + bar_width, y + height)
    midpoint_line_algorithm(x + bar_width, y + height, x, y + height)
    midpoint_line_algorithm(x, y + height, x, y)

    midpoint_line_algorithm(x + 2 * bar_width, y, x + width, y)
    midpoint_line_algorithm(x + width, y, x + width, y + height)
    midpoint_line_algorithm(x + width, y + height, x + 2 * bar_width, y + height)
    midpoint_line_algorithm(x + 2 * bar_width, y + height, x + 2 * bar_width, y)


def draw_cross_button(x, y, width, height):
    midpoint_line_algorithm(x, y, x + width, y + height)
    midpoint_line_algorithm(x + width, y, x, y + height)


def update(val):
    global falling_diamonds, score, diamond_speed, game_paused, game_over, catcher_color

    if not game_paused and not game_over:
        # Update positions of falling diamonds
        for i in range(len(falling_diamonds)):
            falling_diamonds[i][1] -= diamond_speed

        # Remove diamonds that fall below the screen
        falling_diamonds = [d for d in falling_diamonds if d[1] > -50]

        # Add new diamond if there are no diamonds falling
        if len(falling_diamonds) == 0:
            x = random.randint(50, 450)
            y = window_height + 50
            color = [random.random(), random.random(), random.random()]
            color = [c if c > 0.5 else c + 0.5 for c in color]
            falling_diamonds.append([x, y, color])

        # Check if a diamond is caught
        for diamond in falling_diamonds[:]:
            x, y, _ = diamond
            if bowl_x <= x <= bowl_x + bowl_width and bowl_y <= y <= bowl_y + bowl_height:
                score += 1
                print(f"Score: {score}")
                falling_diamonds.remove(diamond)
                break

        # Increase diamond falling speed gradually
        if diamond_speed < 20:
            diamond_speed += 0.01

    # Check if game is over
    if not game_over and len(falling_diamonds) > 0 and falling_diamonds[0][1] < bowl_height:
        game_over = True
        print(f"Game Over. Final Score: {score}")
        catcher_color = [1.0, 0.0, 0.0]  # Red color for catcher

    # Redraw the screen
    glutPostRedisplay()

    # Call update again after a short delay
    glutTimerFunc(50, update, 0)


def special_keys(key, x, y):
    global bowl_x

    if not game_paused and not game_over:
        if key == GLUT_KEY_LEFT:
            bowl_x -= 10  # Move left by 10 pixels
            if bowl_x < 0:
                bowl_x = 0  # Ensure bowl doesn't go off-screen
        elif key == GLUT_KEY_RIGHT:
            bowl_x += 10  # Move right by 10 pixels
            if bowl_x + bowl_width > window_width:
                bowl_x = window_width - bowl_width  # Ensure bowl doesn't go off-screen

    glutPostRedisplay()


def mouse_click(button, state, x, y):
    global score, diamond_speed, game_paused, game_over, catcher_color, falling_diamonds

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Left button (Restart)
        if (left_button_pos[0] <= x <= left_button_pos[0] + button_width and
                window_height - left_button_pos[1] - button_height <= y <= window_height - left_button_pos[1]):
            print("Starting Over")
            score = 0
            diamond_speed = 5
            game_paused = False
            game_over = False
            catcher_color = [1.0, 1.0, 1.0]
            falling_diamonds = []
            x = random.randint(50, 450)
            y = window_height + 50
            color = [random.random(), random.random(), random.random()]
            color = [c if c > 0.5 else c + 0.5 for c in color]
            falling_diamonds.append([x, y, color])

        # Middle button (Play/Pause)
        elif (middle_button_pos[0] <= x <= middle_button_pos[0] + button_width and
              window_height - middle_button_pos[1] - button_height <= y <= window_height - middle_button_pos[1]):
            game_paused = not game_paused

        # Right button (Exit)
        elif (right_button_pos[0] <= x <= right_button_pos[0] + button_width and
              window_height - right_button_pos[1] - button_height <= y <= window_height - right_button_pos[1]):
            print(f"Goodbye, Score: {score}")
            sys.exit()

    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutSpecialFunc(special_keys)
glutMouseFunc(mouse_click)
glutTimerFunc(50, update, 0)
glutMainLoop()
