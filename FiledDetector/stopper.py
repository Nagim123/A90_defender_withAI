from ctypes import *
import time

def temp_stop_player():
    windll.user32.BlockInput(True) #enable block
    time.sleep(2)
    windll.user32.BlockInput(False) #disable block