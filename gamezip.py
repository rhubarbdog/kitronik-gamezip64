import microbit
import neopixel
import music
import time

class KEY:
    def __init__(self, pin):
        self._pin = pin
        self._is_pressed = False
        self._was_pressed = False

    def is_pressed(self):
        return self._is_pressed

    def was_pressed(self):
        value = self._was_pressed
        self._was_pressed = False
        return value

    def _check(self):
        if self._pin.read_digital() == 0:
            self._pressed()
        else:
            self._released()
            
    def _pressed(self):
        self._was_pressed = True
        self._is_pressed = True

    def _released(self):
        self._is_pressed = False

class GAMEZIP():
    def __init__(self):
        self._zip_led = neopixel.NeoPixel(microbit.pin0, 64)
        self._zip_led.clear()

        self._clock = 0
        self._future  = None
        self._vibrate = None

        self.button_up = KEY(microbit.pin8)
        self.button_down = KEY(microbit.pin14)
        self.button_left = KEY(microbit.pin12)
        self.button_right = KEY(microbit.pin13)
        self.button_1 = KEY(microbit.pin15)
        self.button_2 = KEY(microbit.pin16)

    def plot(self, x, y, color):
        self._zip_led[x + (y * 8)] = (color[0], color[1], color[2])

    def clear_screen(self):
        self._zip_led.clear()

    def show_screen(self):
        self._zip_led.show()

    def play_tune(self, tune, wait = False):
        music.play(tune, microbit.pin2, wait)

    def vibrate(self, duration, wait = False):
        self._vibrate = time.ticks_add(time.ticks_ms(), duration)
        microbit.pin1.write_digital(1)
        if wait:
            time.sleep_ms(duration)
            microbit.pin1.write_digital(0)
            self._vibrate = None

    def reset_clock(self):
        self._clock = 0
        self._future = time.ticks_add(time.ticks_ms(), 1000)

    def time(self):
        return self._clock
    
    def sleep(self, duration):
        current = time.ticks_ms()
        end = time.ticks_add(current, duration)
        ALL_KEYS = (self.button_up, self.button_down,
                    self.button_left, self.button_right,
                    self.button_1, self.button_2)

        while True:
            # check for key presses
            for button in ALL_KEYS:
                button._check()

            # stop vibrating if the timer has expired
            if (not self._vibrate is None) and \
               time.ticks_diff(current, self._vibrate) >= 0:
                microbit.pin1.write_digital(0)
                self._vibrate = None

            if not self._future is None:
                elapse = time.ticks_diff(current, self._future)
                if elapse >= 0 :
                    self._clock += 1
                    self._future = time.ticks_add(current, 1000 - elapse)
                    
            if time.ticks_diff(current, end) >=0:
                break

            time.sleep_us(50)
            current = time.ticks_ms()
