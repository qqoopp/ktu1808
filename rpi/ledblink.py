import RPi.GPIO as IO
import time
import subprocess

def checktask():
    proc1 = subprocess.Popen(['ps', '-g'], stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(['grep', 'wake'], stdin=proc1.stdout,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.

    try:
        for line in iter(proc2.stdout.readline, b''):
            if (str(line.strip().decode('utf-8')).index("kitt") >= 0):
                return 1
    except:
        return 0


if __name__ == "__main__":
    pinLED = 5
    IO.setmode(IO.BOARD)
    IO.setup(pinLED,IO.OUT)
    IO.output(pinLED,0)

    try:
        while True:
            if ( checktask() == 1):
                subprocess.Popen(['aplay','-D','hw:0,0','test.wav'])                
                while True:
                    IO.output(pinLED,1)
                    time.sleep(1)
                    IO.output(pinLED,0)
                    time.sleep(1)

            else:
                IO.output(pinLED,0)
                pass
    except:
        IO.cleanup()