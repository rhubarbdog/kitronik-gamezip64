#
# gamezip.py - A simple object to interface with the kitronik gamezip 64 joypad
# Author - Phil Hall, November 2018
from microbit import *
import neopixel
import music
import time

class KEY:
    def __init__(self, pin):
        self._pin = pin
        self._is_pressed = False
        self._was_pressed = False
        self._get_presses = 0

    def is_pressed(self):
        return self._is_pressed

    def was_pressed(self):
        value = self._was_pressed
        self._was_pressed = False
        return value

    def get_presses(self):
        value = self._get_presses
        self._get_presses = 0
        return value

    def _check(self):
        if self._pin.read_digital() == 0:
            self._pressed()
        else:
            self._released()
            
    def _pressed(self):
        self._get_presses += 1
        self._was_pressed = True
        self._is_pressed = True

    def _released(self):
        self._is_pressed = False

class GAMEZIP():
    def __init__(self):
        self._zip_led = neopixel.NeoPixel(pin0, 64)
        self._zip_led.clear()

        self._vibrate = None

        self.button_up = KEY(pin8)
        self.button_down = KEY(pin14)
        self.button_left = KEY(pin12)
        self.button_right = KEY(pin13)
        self.button_1 = KEY(pin15)
        self.button_2 = KEY(pin16)

    def _key_handler(self):
        ALL_KEYS = (self.button_up, self.button_down,
                    self.button_left, self.button_right,
                    self.button_1, self.button_2)

        for button in ALL_KEYS:
            button._check()

    def plot(self, x, y, color):
        self._zip_led[x + (y * 8)] = (color[0], color[1], color[2])

    def clear_screen(self):
        self._zip_led.clear()

    def show_screen(self):
        self._zip_led.show()

    def play_tune(self, tune, wait = False):
        music.play(tune, pin2, wait)

    def vibrate(self, duration, wait = False):
        self._vibrate = time.ticks_add(time.ticks_ms(), duration)
        pin1.write_digital(1)
        if wait:
            time.sleep_ms(duration)
            pin1.write_digital(0)
            self._vibrate = None

    def sleep(self, duration):
        current = time.ticks_ms()
        end = time.ticks_add(current, duration)

        while True:
            # check for key presses
            self._key_handler()
            # stop vibrating if the timer has expired
            if (not self._vibrate is None) and \
               time.ticks_diff(current, self._vibrate) >= 0:
                pin1.write_digital(0)
                self._vibrate = None

            if time.ticks_diff(current, end) >=0:
                break

            current = time.ticks_ms()
            time.sleep_us(50)
