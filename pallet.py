#
# pallet.py - Adjust the RGB value with the cursor keys and see the result
# Author - Phil Hall, November 2018
"""
press left and right to move the cursor
press up and down to increase/decrease the bightness
"""
import gamezip
from microbit import display

joypad = gamezip.GAMEZIP()

red = 4
green = 4
blue = 4

cursor = 0
save = 0
shown = False

while True:
    #joypad.clear_screen()

    for l in range(2):
        joypad.plot(0 + l, 0, (5 * red, 0, 0))
        joypad.plot(3 + l, 0, (0, 5 * green, 0))
        joypad.plot(6 + l, 0, (0, 0, 5 * blue))

    joypad.plot(save, 1, [0, 0, 0])
    joypad.plot(save + 1, 1, [0, 0, 0])

    joypad.plot(cursor, 1, [50, 50, 50])
    joypad.plot(cursor + 1, 1, [50, 50, 50])

    color = (5 * red, 5 * green, 5 * blue)
    for x in range(1,7):
        for y in range(3,7):
            joypad.plot(x, y, color)
            
    joypad.show_screen()
    joypad.sleep(100)

    save = cursor
    if joypad.button_1.is_pressed() or joypad.button_2.is_pressed():
        display.scroll("(" + str(red * 5) + ", " + str(green * 5) + ", " + \
                       str(blue * 5) + ")", wait = False)

    if joypad.button_left.is_pressed():
        cursor -= 3
    if joypad.button_right.is_pressed():
        cursor += 3

    if cursor < 0:
        cursor = 0
        joypad.vibrate(50)
    elif cursor > 6:
        cursor = 6
        joypad.vibrate(50)

    if joypad.button_up.is_pressed():
        if cursor == 0:
            red += 1
        elif cursor == 3:
            green += 1
        else:
            blue += 1
    if joypad.button_down.is_pressed():
        if cursor == 0:
            red -= 1
        elif cursor == 3:
            green -= 1
        else:
            blue -= 1

    vibrate = False
    if red < 0:
        red = 0
        vibrate = True
    if red > 51:
        red = 51
        vibrate = True
    if green < 0:
        green = 0
        vibrate = True
    if green > 51:
        green = 51
        vibrate = True
    if blue < 0:
        blue = 0
        vibrate = True
    if blue > 51:
        blue = 51
        vibrate = True

    if vibrate:
        joypad.vibrate(50)

