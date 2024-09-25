import picar_4wd as fc
import time

# fc.forward(1)
# time.sleep(1/10)  # Try increasing to 2 seconds or more
# fc.stop()

# fc.backward(100)
# time.sleep(2)
# fc.stop()

def turn_right():
    fc.backward(100)
    time.sleep(0.85)
    fc.stop()

turn_right()