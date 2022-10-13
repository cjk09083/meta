from time import time, sleep
import serial

PORT = "COM6"
BAUD = "115200"

KEYMAP = {
    '64' : 'top',
    '66' : 'left',
    '68' : 'center',
    '67' : 'right',
    '65' : 'bottom',
    }

ser = serial.Serial(port=PORT, baudrate=BAUD, timeout = 1)

if __name__ == "__main__":
    try:
        print("Starting IR Listener")
        while True:
            if ser.readable():
                res = ser.readline().strip().decode('utf-8')
                if res and res != '0':
                    code = res
                    # print(code)
                    try:
                        key = KEYMAP[code]
                    except KeyError:
                        key = "ERROR"
                    print(key,"(",str(code),")")

                sleep(0.01)

            # GPIO.wait_for_edge(PIN, GPIO.FALLING)
    except KeyboardInterrupt as e:
        print(e)
        pass
    except RuntimeError as e:
        # this gets thrown when control C gets pressed
        # because wait_for_edge doesn't properly pass this on
        print(e)
        pass
    print("Quitting")