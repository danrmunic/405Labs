'''!
    @file main.py
    @brief Main file runs tasks through loop.
    @details Runs through seperate tasks to test testing the motor_drive task and the encoder task.
            The user can exit program by pressing cntrl+c
    @author Rodolfo Diaz
    @author Daniel Munic
    @author John Bennett
    @date January 11, 2022    
'''
import Encoder
import motor_driver
import pyb
import utime

if __name__ == '__main__':
    ''' @brief Runs main code
    '''
    tim3 = pyb.Timer(3, freq = 20000)
    pinB4 = pyb.Pin(pyb.Pin.cpu.B4)
    pinB5 = pyb.Pin(pyb.Pin.cpu.B5)
    pinENA = pyb.Pin(pyb.Pin.cpu.A10, pyb.Pin.IN, pull = pyb.Pin.PULL_UP)
    ## motor 1 object
    motor1 = motor_driver.Motor_Driver(pinB4, pinB5, tim3, pinENA)
    
    # motor 2
    tim5 = pyb.Timer(5, freq = 20000)
    pinA0 = pyb.Pin(pyb.Pin.cpu.A0)
    pinA1 = pyb.Pin(pyb.Pin.cpu.A1)
    pinENB = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.IN, pull = pyb.Pin.PULL_UP)
    ## motor 2 object
    motor2 = motor_driver.Motor_Driver(pinA0, pinA1, tim5, pinENB)
    
    # encoder 1
    pinB6 = pyb.Pin.cpu.B6
    pinB7 = pyb.Pin.cpu.B7
    ## motor 1 encoder object
    encoder1 = Encoder.Encoder(pinB6, pinB7, 4)
    
    # encoder 2
    pinC6 = pyb.Pin.cpu.C6
    pinC7 = pyb.Pin.cpu.C7
    ## motor 2 encoder object
    encoder2 = Encoder.Encoder(pinC6, pinC7, 8)
    
    ## Communication reader between Computer and Nucleo board so user can type commands
    CommReader = pyb.USB_VCP()
    ## motor 1 current duty
    duty1 = 0
    ## motor 2 current duty
    duty2 = 0
    while (True):
        try:
            utime.sleep(.1)
            encoder1.updatePosition()
            encoder2.updatePosition()
            
            print("\n_________State Data Display_________\n"
                  "Motor1  :    theta = {:.2f}ticks,\tduty(\"w\":+5%,\"s\":-5%) = {:.2f}%\n"
                  "Motor2  :    theta = {:.2f}ticks,\tduty(\"u\":+5%,\"j\":-5%) = {:.2f}%\n".format(encoder1.read(),duty1,encoder2.read(),duty2),end="")
            if(CommReader.any()):
                #Reads Most recent Command
                keyCommand = CommReader.read(1)
                # Clears Queue
                CommReader.read()
            else:
                keyCommand = b' '
            if(keyCommand[0] == b'w'[0]):
                duty1 += 5
                motor1.set_duty(duty1)
                print("up")
            elif(keyCommand[0] == b's'[0]):
                duty1 -= 5
                motor1.set_duty(duty1)
            elif(keyCommand[0] == b'u'[0]):
                duty2 += 5
                motor2.set_duty(duty2)
            elif(keyCommand[0] == b'j'[0]):
                duty2 -= 5
                motor2.set_duty(duty2)
            
        except KeyboardInterrupt:
            break
    
    motor1.disable()
    motor2.disable()
    print('Program Terminating')
    
