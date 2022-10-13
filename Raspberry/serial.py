from time import time
from serial import serial

PORT = "COM4"
BAUD = "115200"


print(serial)

# ser = serial.Serial(port=PORT, baudrate=BAUD, timeout = 1)


if __name__ == "__main__":
    try:
        print("Starting IR Listener")
        while True:
            break
            # ser = serial

            # if ser.readable():
            #     res = ser.readline()
            #     print(res)

            # GPIO.wait_for_edge(PIN, GPIO.FALLING)
            # code = on_ir_receive(PIN)
            # if code:
            #     try:
            #         key = KEYMAP[code]
            #     except KeyError:
            #         key = "ERROR"
            #     print(str(hex(code)),"(",str(code),")",key)
    except KeyboardInterrupt as e:
        print(e)
        pass
    except RuntimeError as e:
        # this gets thrown when control C gets pressed
        # because wait_for_edge doesn't properly pass this on
        print(e)
        pass
    print("Quitting")