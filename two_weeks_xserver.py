#
# Author  - Phil Hall, November 2022
# License - MIT
#

from microbit import *
import neopixel
import music
import radio
import machine
import time

snooze = 10
max_players = 20
# Message IDs
# 0 - global message to all clients
# 1 - message from client to server
# 2 - message from server to client

# pallet dictionary
# (other) players, grass colour one , grass colour two
# enemy, wall, This Player
# blank space, the winning spot
map_colors = {'p' : (20, 20, 0), ',' : (1, 4, 1), '.' : (0, 0, 0), \
              'w' : (0, 0, 20), 'P': (15, 0, 0), 'X' : (10, 0, 10)}

class CrashError(Exception):
    pass

zip_leds = neopixel.NeoPixel(pin0, 64)
zip_leds.clear()

radio.config(channel = 14, queue = int(max_players * 1.5), length = 80)
radio.on()

def plot(xxx, yyy, color):
    global zip_leds
    zip_leds[xxx + (yyy * 8)] = (color[0], color[1], color[2])


display.scroll("Two Weeks")
mach_id = machine.unique_id()
radio.send("1,0," + str(mach_id))

player = None
death = False

# Enroll a new client
while True:
    message = radio.receive()
    if message is None:
        sleep(snooze)
    else:
        message = eval("(" + message + ")")

        # global message 
        if message[0] == 0:
            display.scroll(message[1], wait = False)
        # message to a client is it me?
        elif message[0] == 2:
            if str(mach_id) == str(message[2]):
                player = message[1]
                if player == -1 or player == -2:
                    music.play(["c2:2"], pin2, wait = False)
                    display.scroll(message[3])
                    death = True
                    break
                break

if not death:
    display.scroll(" Player " + str(player + 1), wait = False, loop = True)

# monitor the radio for the go message
while not death:
    message = radio.receive()
    if message is None:
        sleep(snooze)
    else:
        message = eval("(" + message + ")")

        #global message
        if message[0] == 0:
            if message[1] == "Ready":
                for i in range(5):
                    music.play(["c4:2"], pin2, False)
                    display.show(str(5 - i))
                    sleep(1000)
                break
            else:
                display.scroll(message[1], wait = False)
        # message to this client not now!!!
        elif message[0] == 2 and message[1] == player:
            raise CrashError


# play the game
loops = 0
screen = None
winner = 0

while not death:
    if winner == 1:
        winner = 2

    sleep(snooze)
    # get all messages until my screen appears
    while True:
        message = radio.receive()
        if message is None:
            break
        else:
            message = eval("(" + message + ")")

            # global message, this must be game over
            if message[0] == 0:
                display.scroll(message[1], wait = False, loop = True)
                break
            elif message[0] == 2 and message[1] == player:
                if message[2] == 'Winner':
                    music.play(music.POWER_UP, pin2, False)
                    display.scroll(message[2], wait = False)
                    winner = 1
                else:
                    screen = []
                    for i in range(8):
                        screen.append(message[2][i * 8: (i * 8) + 8])

                    player_x = message[3]
                    player_y = message[4]
                    compass = message[5]
                    break

    # draw screen, compass and player
    if not screen is None:
        for xxx in range(8):
            for yyy in range(8):
                plot(xxx, yyy, map_colors[ screen[yyy][xxx] ])

        plot(player_x, player_y, map_colors['P'])
        zip_leds.show()

        if winner == 1:
            sleep(5000)
            
        if compass == -2:
            display.show(Image.HAPPY)
        elif compass == -1:
            display.show(Image.SQUARE)
        else:
            display.show(Image.ALL_CLOCKS[compass])
        

    # game over
    if winner == 2:
        break
    
    # detect buttons, up, down, left, right
    buttons = ""
    if winner == 0:
        if pin8.read_digital() == 0:
            buttons += 'u'
        if pin14.read_digital() == 0:
            buttons += 'd'
        if pin12.read_digital() == 0:
            buttons += 'l'
        if pin13.read_digital() == 0:
            buttons += 'r'

    # send buttons to server
    if loops % 10 == 0 and buttons != "":
        radio.send("1,1," + str(player) + ",'" + buttons + "'")

    if loops == 10000:
        loops = 0
        
    loops += 1


radio.off()

