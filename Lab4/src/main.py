import pyb
import utime
import task_share

def isr_fun(dum):
    myQueue.put(myadc.read())

if __name__ == "__main__":
    pinC1 = pyb.Pin(pyb.Pin.cpu.C1, mode=pyb.Pin.OUT_PP)
    pinC0 = pyb.Pin(pyb.Pin.cpu.C0)
    tim1 = pyb.Timer(1, freq = 1000)
    
    myQueue = task_share.Queue("h", 1000, name="Jonathan")
    
    myadc = pyb.ADC(pinC0)
    
    while True:
        input("ready to start hit anything:")
        pinC1.high()
        
        tim1.callback(isr_fun)
        utime.sleep(1)
        tim1.callback(None)
        
        pinC1.low()
        
        print("#START#")
        for i in range(999):
            print(str(myQueue.get()) + "," + str(i * 0.001))
        myQueue.clear()
        print("#STOP#")
        