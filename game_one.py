"""
This is a re-write of the Kitronic program supplied in the datasheet
5612-kitronik-game-zip-64-microbit-datasheet.pdf

press up, down, left, right to move the sprite
press fire 1 & 2 to change the sprite colour
"""
import gamezip
import music

def hit_edge():
    joypad.play_tune(music.BA_DING)
    joypad.vibrate(500)

joypad = gamezip.GAMEZIP()

sprite_x = 3
sprite_y = 3

# red, yellow, green, blue, purple, white
colours = [[20, 0, 0], [20, 20, 0], [0, 20, 0], [0, 0, 20],
           [20, 0, 20], [20, 20, 20]]
sprite_colour = colours[3]

while True:
    joypad.clear_screen()
    joypad.plot(sprite_x, sprite_y, sprite_colour)
    joypad.show_screen()
    joypad.sleep(100)
    
    if joypad.button_up.is_pressed():
        if sprite_y == 0:
            hit_edge()
        else:
            sprite_y -= 1

    if joypad.button_down.is_pressed():
        if sprite_y == 7:
            hit_edge()
        else:
            sprite_y += 1

    if joypad.button_left.is_pressed():
        if sprite_x == 0:
            hit_edge()
        else:
            sprite_x -= 1

    if joypad.button_right.is_pressed():
        if sprite_x == 7:
            hit_edge()
        else:
            sprite_x += 1

    if  joypad.button_1.is_pressed():
        if colours.index(sprite_colour) - 1 < 0:
            sprite_colour = colours[0]
        else:
            sprite_colour = colours[(colours.index(sprite_colour) - 1)]

    if  joypad.button_2.is_pressed():
        if colours.index(sprite_colour) + 1 >= len(colours):
            sprite_colour = colours[-1]
        else:
            sprite_colour = colours[(colours.index(sprite_colour) + 1)]
