"""
press left and right to move the cursor
press up and down to increase/decrease the bightness
"""
import gamezip

joypad = gamezip.GAMEZIP()

LIGHTS = ((5, 0, 0), (5, 5, 0), (0, 5, 0), (0, 5, 5),
          (0, 0, 5), (5, 0, 5), (5, 0, 0), (5, 5, 5))

scalar = [4, 4, 4, 4, 4, 4, 4, 4]

cursor = 0

while True:
    joypad.clear_screen()

    for i in range(len(LIGHTS)):
        color = LIGHTS[i]
        r, g, b = color
        s = scalar[i]
        color = [r * s,g * s,b * s]
        joypad.plot(i, 0, color)
    joypad.plot(cursor, 1, [50, 50, 50])

    joypad.show_screen()
    joypad.sleep(100)

    if joypad.button_left.is_pressed():
        cursor -= 1
    if joypad.button_right.is_pressed():
        cursor += 1

    if cursor < 0:
        cursor = 0
        joypad.vibrate(50)
    elif cursor >= len(LIGHTS):
        cursor = len(LIGHTS) - 1
        joypad.vibrate(50)

    if joypad.button_up.is_pressed():
        scalar[cursor] += 1
    if joypad.button_down.is_pressed():
        scalar[cursor] -= 1

    if scalar[cursor] < 1:
        scalar[cursor] = 1
        joypad.vibrate(50)
    elif scalar[cursor] > 51:
        scalar[cursor] = 51
        joypad.vibrate(50)
        
