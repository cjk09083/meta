#!/usr/bin/env python
# coding: utf-8
from time import time
import serial
import inspect

PORT = "COM4"
BAUD = "115200"

print(serial)
print(inspect.getfile(serial))

ser = serial.Serial(port=PORT, baudrate=BAUD, timeout = 1)


if __name__ == "__main__":
    try:
        print("Starting IR Listener")
        while True:
            if ser.readable():
                res = ser.readline()
                print(res)
    except KeyboardInterrupt as e:
        print(e)
        pass
    except RuntimeError as e:
        # this gets thrown when control C gets pressed
        # because wait_for_edge doesn't properly pass this on
        print(e)
        pass
    print("Quitting")