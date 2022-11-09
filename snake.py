from microbit import *
import gamezip
import random
import music

joypad = gamezip.GAMEZIP()
screen = 30

head_colour = (30, 0, 0)
tail_colour = (20, 20, 20)
brick_colour = (0, 0, 25)
floor_tile = (1, 4, 1)
food_colour = (7, 7, 7)
dying_food = (10, 0, 0)

food = []
tail = []
bricks = []

def draw_screen(snake_x, snake_y):
    if snake_x < 4:
        end_x = 8
    elif snake_x > screen - 4:
        end_x = screen
    else:
        end_x = min(screen, snake_x + 4)
    if snake_y < 4:
        end_y = 8
    elif snake_y > screen - 4:
        end_y = screen
    else:
        end_y = min(screen, snake_y + 4)
        
    begin_x = max(end_x - 8, 0)
    begin_y = max(end_y - 8, 0)

    for xxx in range(begin_x, end_x):
        for yyy in range(begin_y, end_y):

            if (xxx // 2) % 2 == (yyy // 2) % 2:
                joypad.plot(xxx - begin_x, yyy - begin_y, floor_tile)
            else:
                joypad.plot(xxx - begin_x, yyy - begin_y, (0, 0, 0))
                
            for tmp in food:
                if tmp[2] < 3:
                    colour = dying_food
                else:
                    colour = food_colour
                    
                if tmp[0] == xxx and tmp[1] == yyy:
                    joypad.plot(xxx - begin_x, yyy - begin_y, colour)

            for tmp in tail:
                if tmp[0] == xxx and tmp[1] == yyy:
                    joypad.plot(xxx - begin_x, yyy - begin_y, tail_colour)

            if xxx == 0 or xxx >= screen - 1 or yyy == 0 or yyy >= screen - 1:
                joypad.plot(xxx - begin_x, yyy - begin_y, brick_colour)

            if xxx == snake_x and yyy == snake_y:
                joypad.plot(xxx - begin_x, yyy - begin_y, head_colour)

            for tmp in bricks:
                if tmp[0] == xxx and tmp[1] == yyy:
                    joypad.plot(xxx - begin_x, yyy - begin_y, brick_colour)


def draw_map(snake_x, snake_y):
    display.clear()
    divide = screen / 5
    for xxx in range(1,6):
        for yyy in range(1,6):
            for tmp in food:
                if tmp[0] > int(divide * (xxx - 1)) and \
                   tmp[0] <= int(divide * xxx) and \
                   tmp[1] > int(divide * (yyy - 1)) and \
                   tmp[1] <= int(divide * yyy):
                    display.set_pixel(xxx - 1, yyy - 1, 3)

            if snake_x > int(divide * (xxx - 1)) and \
               snake_x <= int(divide * xxx) and \
               snake_y > int(divide * (yyy - 1)) and \
               snake_y <= int(divide * yyy):
                    display.set_pixel(xxx - 1, yyy - 1, 9)
                    
                

xxx = 20
yyy = 20
dy = 0
dx = 1
dead = False
loops = 0

while True:
    
    draw_screen(xxx, yyy)
    draw_map(xxx, yyy)
    joypad.show_screen()

    if joypad.button_up.is_pressed():
        if dy == 1 and len(tail) > 0:
            dead = True
        dx = 0
        dy = -1
    elif joypad.button_down.is_pressed():
        if dy == -1 and len(tail) > 0:
            dead = True
        dx = 0
        dy = 1
    elif joypad.button_left.is_pressed():
        if dx == 1 and len(tail) > 0:
            dead = True
        dx = -1
        dy = 0
    elif joypad.button_right.is_pressed():
        if dx == -1 and len(tail) > 0:
            dead = True
        dx = 1
        dy = 0

    # Turned back on yourself
    if dead:
        break

    # hit the edge
    if xxx == 0 or xxx == screen - 1 or yyy == 0 or yyy == screen -1:
        dead = True
        break

    # crashed into dead food
    if loops % 4 == 0:
        for tmp in bricks:
            if xxx == tmp[0] and yyy == tmp[1]:
                dead = True
                break

    if dead:
        break

    # Eaten your own tail
    if loops % 4 == 0:
        for tmp in tail:
            if xxx == tmp[0] and yyy == tmp[1]:
                dead = True
                break

    if dead:
        break

    # eating food
    adding = False
    if loops % 4 == 0:
        for tmp in food:
            if xxx == tmp[0] and yyy == tmp[1]:
                tail.append((xxx, yyy))
                adding = True
                food = food[:food.index(tmp)] + food[food.index(tmp) + 1:]
                break
        
    if loops % 4 == 0 and len(tail) > 0 and not adding:
        tail = tail[1:]
        tail.append((xxx, yyy))

    if loops % 4 == 0:
        xxx += dx
        yyy += dy

    # add food 20% of the time
    if loops % 4 == 0 and random.random() <= 0.20:
        mode = random.randrange(15) + 1
        while True:
            food_x = random.randrange(screen - 1) + 1
            food_y = random.randrange(screen - 1) + 1
            adding = True
            for tmp in bricks:
                if tmp[0] == food_x and tmp[1] == food_y:
                    adding = False
                    break

            if adding:
                break
            
        food.append([food_x, food_y, mode])
                     

    #degrade food every 2000 milli  seconds
    if loops % 20 == 0:
        for tmp in food:
            _, _, mode = tmp
            mode -= 1
            if mode <= 0:
                mode = 0
                bricks.append((tmp[0], tmp[1]))

            i = food.index(tmp)
            if mode == 0:
                food = food[:i] + food[i+1:]
            else:
                food = food[:i] + [[tmp[0], tmp[1], mode]] + \
                    food[i+1:]

    loops += 1
    if loops == 10000:
        loops = 0

    joypad.sleep(100)

joypad.play_tune(music.FUNERAL)
display.scroll("Game Over - " + str(len(tail)), wait = False, loop = True)
joypad.sleep(300)



