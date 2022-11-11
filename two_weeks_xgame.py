#
# Author  - Phil Hall, November 2022
# License - MIT
#

from microbit import *
import music
import radio
import machine

snooze = 50
max_players = 20
# Message IDs
# 2 - message from xclient to xserver
# 1 - message from xserver to xclient
# 0 - global message to all xservers

# Messages Sent
# 1, -1 (enroll me), machine_id
# 1, 1 (button presses), player, buttons pressed

# Messages Received
#  2, player, 0, machine_id
#  2, -1, machine_id, too many players
#  2, -2, machine_id, game already started 
#  2, player, 1, winner
#  2, player, 2, screen, player x, player y, compass
#
#  0, Ready
#  0, Game Over



# pallet dictionary
# (other) players, grass colour one , grass colour two
# enemy, wall, the winning spot
map_colors = {'p' : 4, ',' : 1, '.' : 0, 'w' : 9, 'X' : 7}

class CrashError(Exception):
    pass


radio.config(channel = 14, queue = int(max_players * 1.5), length = 96)
radio.on()

def plot(xxx, yyy, ilume):
    display.set_pixel(xxx, yyy, ilume)

display.scroll("Two Weeks")
mach_id = machine.unique_id()
radio.send("1,-1," + str(mach_id))

player = None
die = False

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
                    die = True
                    break
                break

if not die:
    display.scroll(" Player " + str(player + 1), wait = False, loop = True)

# monitor the radio for the go message
while not die:
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


# play the game - main loop
loops = 0
screen = None
winner = 0
ilume = 9

while not die:
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
                if message[2] == 1:
                    music.play(music.POWER_UP, pin2, False)
                    display.scroll(message[3], wait = False)
                    winner = 1
                else:
                    player_x = message[4] - 2
                    player_y = message[5] - 2
                    compass = message[6]
                    screen = []
                    for i in range(8):
                        screen.append(message[3]\
                                      [(i * 8) + min(3, player_x):\
                                       (i * 8) + min(8, 5 + player_x)])
                    screen = screen[min(3, player_y): min(5 + player_y, 8)]

                    break

    # draw screen, compass and player
    if not screen is None and not pin16.read_digital() == 0:
        for xxx in range(5):
            for yyy in range(5):
                print(xxx, yyy, screen[yyy][xxx])
                plot(xxx, yyy, map_colors[ screen[yyy][xxx] ])

        plot(player_x, player_y, ilume)

        if loops % 3 == 0:
            ilume -= 1
            if ilume == 0:
                ilume = 9

        if winner == 1:
            sleep(5000)

    if pin16.read_digital() == 0 or winner == 1:
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
    if loops % 3 == 0 and buttons != "":
        radio.send("1,1," + str(player) + ",'" + buttons + "'")

    if loops == 30000:
        loops = 0
        
    loops += 1


radio.off()

