import pyb
import utime

#constant
Encoder_Period = 2**16

class Encoder:

    def __init__(self, pinCH1, pinCH2, timerNum):
        self.timer = pyb.Timer(timerNum, prescaler=0, period=Encoder_Period-1)
        self.timer.channel(1, mode=pyb.Timer.ENC_AB, pin=pinCH1)
        self.timer.channel(2, mode=pyb.Timer.ENC_AB, pin=pinCH2)

        #unbounded position, corresponds to timer_counter unless there is overflow/underflow
        self.position = self.timer.counter()
        self.Eposition = self.timer.counter()

    def zero(self):
        #reset timer
        self.timer.counter(0)
        self.position = self.timer.counter()

    def read(self):
        return self.position

    def updatePosition(self):
        delta = self.timer.counter() - self.Eposition
        self.Eposition = self.timer.counter()
        #Fix Overflow
        if delta > Encoder_Period / 2:
            delta = delta - Encoder_Period

        #Fix Underflow
        elif delta < -(Encoder_Period / 2):
            delta = delta + Encoder_Period

        self.position = self.position + delta


if __name__ == '__main__':
    pinCH1 = pyb.Pin.cpu.B6
    pinCH2 = pyb.Pin.cpu.B7

    myEncoder = Encoder(pinCH1, pinCH2, 4)

    while True:
        utime.sleep(.5)
        myEncoder.updatePosition()
        print(myEncoder.read())