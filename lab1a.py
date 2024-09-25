import picar_4wd as fc
# import sys
# import tty
# import termios
# import asyncio
# import time


def PivotCar(left, middle, right, lefts):
    print(lefts)
    REVERSE_POWER_LEVEL = 40
    TURN_POWER_LEVEL = 40
    fc.stop()
    fc.backward(REVERSE_POWER_LEVEL)
    time.sleep(0.25)
    
    if(lefts > 0):
        if(left == ([2] * len(left))):
            fc.turn_left(TURN_POWER_LEVEL)
            lefts += 1
        else:
            fc.turn_right(TURN_POWER_LEVEL)
            lefts -= 1
    else:
        if(right == ([2] * len(right))):
            fc.turn_right(TURN_POWER_LEVEL)
            lefts -= 1
        else:
            fc.turn_left(TURN_POWER_LEVEL)
            lefts += 1


    time.sleep(0.25)

    return lefts


try:
    lefts = 0
    caution = False
    while True:
        scan_list = fc.scan_step(35)
        if not scan_list:
            continue

        n = len(scan_list)
        third = n // 3
        remainder = n % 3

        sizes = [third, third + remainder, third]

        left = scan_list[:sizes[0]]
        middle = scan_list[sizes[0]:sizes[0]+sizes[1]]
        right = scan_list[sizes[0]+sizes[1]:]
        
        print(left, middle, right)
        if(scan_list != [2] * len(scan_list)):
            caution = True
        else:
            caution = False

        if middle != ([2] * len(middle)):
            lefts = PivotCar(left, middle, right, lefts)
        else:
            fc.forward(30 if not caution else 20)

finally:
    print("Quit")
    fc.stop()
