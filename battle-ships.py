#
# Author  : Phil Hall, November 2022
# Licence : MIT
#
from microbit import *
import gamezip 
import radio
import random
import music

screen = [' ' * 8, ' ' * 8, ' ' * 8, ' ' * 8, ' ' * 8, ' ' * 8, \
          ' ' * 8, ' ' * 8] 
opposition = [' ' * 8, ' ' * 8, ' ' * 8, ' ' * 8, ' ' * 8, ' ' * 8, \
              ' ' * 8, ' ' * 8]

joypad = gamezip.GAMEZIP()
radio.config(channel = 17)
radio.on()
speaker.off()

boats = (4, 3, 3, 2, 2)
boat_str = '01234'

def draw_screen():
    display.show(Image.ARROW_S)
    for x in range(len(screen[0])):
        for y in range(len(screen)):
            if screen[y][x] == ' ':
                colour = [0, 0, 0]
            elif screen[y][x] in boat_str:
                colour = [0, 0, 150]
            elif screen[y][x] == 'H':
                colour = [60, 0, 0]
            else:
                colour = [20, 20, 20]
            
            joypad.plot(x, y, colour)

def draw_opposition():
    display.show(Image.ARROW_N)
    for x in range(len(opposition[0])):
        for y in range(len(opposition)):
            if opposition[y][x] == ' ':
                colour = [0, 0, 0]
            elif opposition[y][x] == 'H':
               colour = [120, 0, 0]
            else:
                colour = [20, 20, 20]
                
            joypad.plot(x, y, colour)

            
def position_boats():
    this_boat = [0, 120, 0]
    for ship in range(len(boats)):
        xxx = 0
        yyy = 0
        vertical = False
        loops = 1
        flash = this_boat

        while True:
            draw_screen()
            for delta in range(boats[ship]):
                if vertical:
                    joypad.plot(xxx, yyy + delta, flash)
                else:
                    joypad.plot(xxx + delta, yyy, flash)

            joypad.show_screen()

            if joypad.button_up.is_pressed() and yyy > 0:
                yyy -= 1

            if joypad.button_down.is_pressed() and \
               (vertical and yyy + boats[ship] < len(screen) or \
                not vertical and yyy < len(screen) - 1):
                yyy += 1

            if joypad.button_left.is_pressed() and xxx > 0:
                xxx -= 1

            if joypad.button_right.is_pressed() and \
               (not vertical and xxx + boats[ship] < len(screen[0]) or \
                vertical and xxx < len(screen[0]) - 1):
                xxx += 1

            if joypad.button_1.is_pressed():
                vertical = not vertical
                if vertical and yyy + boats[ship] >= len(screen):
                    yyy = len(screen) - boats[ship]
                if not vertical and xxx + boats[ship] >= len(screen[0]):
                    xxx = len(screen[0]) - boats[ship]

            if joypad.button_2.is_pressed():
                colide = False
                for delta in range(boats[ship]):
                    if vertical and screen[yyy + delta][xxx] != ' ':
                        colide = True
                    if not vertical and screen[yyy][xxx + delta] != ' ':
                        colide = True

                if colide:
                    joypad.play_tune(['c2:1'])
                else:
                    joypad.play_tune(['c5:2'], wait = True)
                    for delta in range(boats[ship]):
                        if vertical:
                            screen[yyy + delta] = screen[yyy + delta][:xxx] + \
                                str(ship) + screen [yyy + delta][xxx + 1:]
                        else:
                            screen[yyy] = screen[yyy][:xxx + delta] + \
                                str(ship) + screen[yyy][xxx + 1 + delta:]

                    while joypad.button_2.is_pressed():
                        joypad.sleep(10)
                    break

                
                    
            if loops == 500:
                loops = 0

            if loops % 5 == 0:
                if flash == this_boat:
                    flash = [0, 0, 0]
                else:
                    flash = this_boat

            joypad.sleep(10)
            loops += 1


def drop_bomb():
    xxx = 3
    yyy = 3
    loops = 1
    this_bomb = [60, 60, 0]
    flash = this_bomb

    while True:
        draw_opposition()
        joypad.plot(xxx, yyy, flash)
        joypad.show_screen()

        if joypad.button_up.is_pressed() and yyy > 0:
            yyy -= 1

        if joypad.button_down.is_pressed() and yyy < len(screen) - 1:
            yyy += 1
            
        if joypad.button_left.is_pressed() and xxx > 0:
            xxx -= 1

        if joypad.button_right.is_pressed() and xxx < len(screen[0]) - 1:
            xxx += 1

        if joypad.button_2.is_pressed():
            if opposition[yyy][xxx] != ' ':
                joypad.play_tune(['c2:1'])
            else:
                joypad.play_tune(['c5:2'], wait = True)
                radio.send(str(xxx) + ',' + str(yyy))

                while True:
                    received = radio.receive()
                    if not received is None:
                        break
                    joypad.sleep(100)

                destroyed = False
                if received == 'D':
                    received = 'H'
                    destroyed = True

                opposition[yyy] = opposition[yyy][:xxx] + received + \
                    opposition[yyy][xxx + 1:]

                draw_opposition()
                joypad.show_screen()

                if destroyed:
                    display.scroll('Destroyed')
                elif received == 'H':
                    display.scroll('Hit')
                else:
                    display.scroll('Miss')

                joypad.sleep(2000)
                while True:
                    received = radio.receive()
                    if not received is None:
                        break
                    joypad.sleep(100)

                while joypad.button_2.is_pressed():
                    joypad.sleep(10)

                break

        if loops == 500:
            loops = 0

        if loops % 5 == 0:
            if flash == this_bomb:
                flash = [0, 0, 0]
            else:
                flash = this_bomb

        joypad.sleep(10)
        loops += 1
    
    return received == 'dead'


joypad.clear_screen()
position_boats()
draw_screen()
joypad.show_screen()

while True:
    selected = random.choice(('me', 'you'))
    radio.send(selected)
    while True:
        received = radio.receive()
        if not received is None:
            break
        joypad.sleep(100)

    if selected != received:
        break

first = True

while True:
    if first and selected == 'me':
        dead = drop_bomb()

        if dead:
            break

    draw_screen()
    joypad.show_screen()
    
    first = False

    while True:
        received = radio.receive()
        if not received is None:
            break
        joypad.sleep(100)

    xxx, yyy = eval("(" + received + ")")

    if screen[yyy][xxx] in boat_str:
        message = 'H'
    else:
        message = 'M'

    current = screen[yyy][xxx]
    screen[yyy] = screen[yyy][:xxx] + message + screen[yyy][xxx + 1:]

    if current in boat_str:
        destroyed = True
        for row in screen:
            if current in row:
                destroyed = False
                break

        if destroyed:
            message = 'D'

    radio.send(message)
    draw_screen()
    joypad.show_screen()
    joypad.sleep(3000)

    destoyed = True
    breaking = False
    for ship in boat_str:
        for row in screen:
            if ship in row:
                destroyed = False
                breaking = True
                break

        if breaking:
            break

    if destroyed:
        radio.send('dead')
        break
    else:
        radio.send('alive')

    dead = drop_bomb()
    if dead:
        break
    
draw_screen()
joypad.show_screen()
if dead:
    show = Image.SAD
    joypad.play_tune(music.FUNERAL)
else:
    show = Image.HAPPY
    joypad.play_tune(music.POWER_UP)
    
while True:
    display.show(show)
    joypad.sleep(2000)
    draw_opposition()
    joypad.show_screen()

    joypad.sleep(2000)
    draw_screen()
    joypad.show_screen()
