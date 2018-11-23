<b>A micropython object for the Kitronik Game Zip 64</b>
<br><br>
The aim of this object is to give similar functionality to the joypad buttons as is available to <code>microbit.button_a<\code> and <code>microbit.button_b<\code>.  It also facilitates asynchronous vibration (no pause when vibrating).  This is acheived via method <code>GAMEZIP.sleep<\code>, you must not use <code>microbit.sleep<\code>.  If there are no sleeps in your program you must make regular calls to <code>GAMEZIP.sleep(0)<\code>.  <code>GAMEZIP.sleep<\code> polls the keys on the joypad and stops any vibration, if the duration has not expired it sleeps for 50 micro seconds and loops.
<br><br>
The <code>GAMEZIP<\code> object is made up of 6 <code>KEY<\code> objects:<br>
<code>GAMEZIP.button_up<\code><br>
<code>GAMEZIP.button_down<\code><br>
<code>GAMEZIP.button_left<\code><br>
<code>GAMEZIP.button_right<\code><br>
<code>GAMEZIP.button_1<\code><br>
<code>GAMEZIP.button_2<\code><br>
Keys have the following methods:<br>
<table><tr><td>method</td><td>type</td></tr>
<tr><td><code>.is_pressed()</code></td><td><code>boolean</code></td><td>returns True if the button is pressed.</td></tr>
<tr><td><code>.was_pressed()</code></td><td><code>boolean</code></td><td>returns True if the key has been pressed since reset or the last call to this method.</td></tr>
<tr><td><code>.get_presses()</code></td><td><code>integer</code></td><td>returns the number of times the key has been pressed since reset or the last call to this method.</td></tr>
</table>
<br>
<code>GAMEZIP<code> has the following methods:<br>
<table>
<tr><td>method</td></tr>
<tr><td><code>.plot(x, y, color)</code></td><td>sets the LED at coordinates x, y to the color specified by a list or tuple in RGB format</td></tr>
<tr><td><code>.clear_screen()</code></td><td>blanks all LED's, it's ususal to do this before plotting a new screen</td></tr>
<tr><td><code>.show_screen()</code></td><td>updates the screen with the current plotted values.  It's not enough just to plot your screen yon need to show it</td></tr>
<tr><td><code>.play_tune(tune, wait = False)</code></td><td>plays the tune supplied such as <code>music.ENTERTAINER</code>.  If wait is True this method will block untin the tune has completed.</td></tr>
<tr><td><code>.vibrate(duration, wait = False)</code></td><td>this method makes the joypad vibrate.  If wait is True this method will block for the specified number of milli seconds.</td></tr>
<tr><td><code>.sleep(duration)</code></td><td>this method scans the keys and stops asynchronous vibration whilst it sleeps for the given number of milli seconds. It is crucial to make regular calls to this method to give a good keypad response.</td></tr>
</table>
<br><br>
There are 3 example programs <code>game_one.py, lights.py & music.py</code> They all have a brief instruction in their source code.
<br>