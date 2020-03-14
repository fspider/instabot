
#imports the library
from pykeyboard import PyKeyboard
#import the sleep function
from time import sleep
#initialize the keyboard simulator
keyboard = PyKeyboard()
#presses the key
keyboard.press_key('x')
#waits five seconds before releasing the key
sleep(5)
#releases the key
keyboard.release_key('x')