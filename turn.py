import picar_4wd as fc
import time


POWER_RATIO = 1.16

def turn_right():
    fc.turn_right(100)
    time.sleep(0.75 * POWER_RATIO)
    fc.stop()

def turn_left():
    fc.turn_left(100)
    time.sleep(0.67 * POWER_RATIO)
    fc.stop()

if __name__ == "__main__":
    turn_right()
    time.sleep(1)
    turn_left()   

