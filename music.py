"""
press up and down to change the tune index
press button 1 to select and play 
"""
import gamezip
import music

joypad = gamezip.GAMEZIP()
TUNES = [ music.ENTERTAINER, music.FUNERAL, music.WEDDING ]

index = 0

while True:
    joypad.play_tune(TUNES[index])

    while not joypad.button_1.was_pressed():
        if joypad.button_up.is_pressed():
            index += 1
        if joypad.button_down.is_pressed():
            index -= 1

        if index < 0:
            index = 0
            joypad.vibrate(30)
        elif index >= len(TUNES):
            index = len(TUNES) - 1
            joypad.vibrate(30)

        joypad.sleep(300)
