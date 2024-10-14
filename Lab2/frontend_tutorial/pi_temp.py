import os

def get_temp():
    output = os.popen("vcgencmd measure_temp").read()
    return output.split('=')[1]