<h1><b>Kitronik Gamezip64</b> - <code>gamezip.py</code></h1>

<br/>
The aim of this object is to give similar functionality to the joypad buttons
as is available to <code>microbit.button_a</code> and <code>microbit.button_b
</code>.  It also facilitates asynchronous vibration (no pause when vibrating).
This is acheived via method <code>GAMEZIP.sleep</code>, you must not use <code>
microbit.sleep</code>.  If there are no sleeps in your program you must make
regular calls to <code>GAMEZIP.sleep(0)</code>.  <code>GAMEZIP.sleep</code>
polls the keys on the joypad and stops any vibration, if the duration has not
expired it sleeps for 50 micro seconds and loops.

<br/>
The <code>GAMEZIP</code> object is made up of 6 <code>KEY</code> objects:<br/>
<code>GAMEZIP.button_up</code><br/>
<code>GAMEZIP.button_down</code><br/>
<code>GAMEZIP.button_left</code><br/>
<code>GAMEZIP.button_right</code><br/>
<code>GAMEZIP.button_1</code><br/>
<code>GAMEZIP.button_2</code><br/><br/>

Keys have the following methods:<br/>
<table><tr><td>method</td><td>type</td></tr>
<tr><td><code>.is_pressed()</code></td><td><code>boolean</code></td><td>returns True if the button is pressed.</td></tr>
<tr><td><code>.was_pressed()</code></td><td><code>boolean</code></td><td>returns True if the key has been pressed since reset or the last call to this method.</td></tr>
</table>
<code>GAMEZIP</code> has the following methods:<br/>
<table>
<tr><td>method</td></tr>
<tr><td><code>.plot(x, y, color)</code></td><td>sets the LED at coordinates x, y to the color specified by a list or tuple in RGB format</td></tr>
<tr><td><code>.clear_screen()</code></td><td>blanks all LED's, it's ususal to do this before plotting a new screen</td></tr>
<tr><td><code>.show_screen()</code></td><td>updates the screen with the current plotted values.  It's not enough just to plot your screen yon need to show it</td></tr>
<tr><td><code>.play_tune(tune, wait = False)</code></td><td>plays the tune supplied such as <code>music.ENTERTAINER</code>.  If wait is True this method will block until the tune has completed.</td></tr>
<tr><td><code>.vibrate(duration, wait = False)</code></td><td>this method makes the joypad vibrate.  If wait is True this method will block for the specified number of milli seconds.</td></tr>
<tr><td><code>.reset_clock</code></td><td>this method starts or resets the clock to 0.</td></tr>
<tr><td><code>.time</code></td><td>this method returns the number of elapsed seconds since the clock was last reset. This is an aproximate clock it may be a second or two slow.</td></tr>
<tr><td><code>.sleep(duration)</code></td><td>this method scans the keys and stops asynchronous vibration whilst it sleeps for the given number of milli seconds. It is crucial to make regular calls to this method to give a good keypad response.</td></tr>
</table>
<br/><br/>
To use a game you need to flash the microbit with <code>uflash</code> or copy
a  <code>microbit.hex</code> file over then use microFS to transfer the module
<code>gamezip.py</code> and the program to become <code>main.py</code> as in the
following example.
<br/><br/>
<code>
ufs put gamezip.py
</code><br/><code>
ufs put battle-ships.py main.py
</code>
<br/>

<h2>Games</h2>

<h4>game-one.py</h4>
a demo of using the module <code>gamezip.py</code>. Move the sprite around the
screen using the arrow keys and change it's colour with the fire buttons. 
<br/>
<h4>pallet.py</h4>
Move the cursor left and right to select a primary colour, increase and decrease it's intensity with up and down. Reveal, the tuple to define the colour with either fire button, uses <code>gamezip.py</code> 
<br/>
<h4>music.py</h4>
Turn your gamezip into a juke box, use up and down to change the tune. Uses
<code>gamezip.py</code>
<br/>
<h4>battle-ships.py</h4>
A 2 player game for the gamezip and microbit version 2, you'll need two of each
. Position your boats using the arrow buttons, rotate them with fire button 1,
fix them with fire button one. When bombing your opponent the arrow keys move
the bomb and fire button 2 drops it. Uses <code>gamezip.py</code>.
<br/>
<h4>snake.py</h4>
Use the arrow keys to guide snake around a massive room eating food, growing a
longer and longer tail. Use the map on the microbit to find your next food.
Snake is the bright dot, food the faint ones.  Be warned food goes bad and
turns to poison and the perimeter wall is made of stone.  Avoid your tail
and avoid stones, avoid poison, eat food. This is for version 2 microbits and uses <code>gamezip.py</code>.
<br/>
<h3>Two Weeks - a Fortnight clone for microbit</h3>
<br/>
Two weeks now has it's own repository at https://github.com/rhubarbdog/microbit-two-weeks