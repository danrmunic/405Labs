'''!
    @file main.py
    @brief Main file runs tasks through loop.
    @details Runs through seperate tasks to test testing the motor_drive task and the encoder task.
            The user can exit program by pressing cntrl+c
    @author Rodi Diaz
    @author Daniel Munic
    @author John Bennett
    @date January 11, 2022    
'''
import Encoder
import motor_driver
import pyb
import utime
import closedLoop

def check_user_input(prompt):
    while True:
        try:
            # Convert it into float
            print(prompt)
            num = input()
            return float(num)
        except ValueError:
            print("No.. "+ num +" input is not a number. It's a string. Enter a Number")
#     Commandline()
    
# def Commandline():
#     print("Ready for next command. Hit characters s,S Steps. k,K Kp.")

if __name__ == '__main__':
    '''! @brief Runs main code
    '''
    ## motor 1 timer (3)
    tim3 = pyb.Timer(3, freq = 20000)
    ## motor 1 pin B4
    pinB4 = pyb.Pin(pyb.Pin.cpu.B4)
    ## motor 1 pin B5
    pinB5 = pyb.Pin(pyb.Pin.cpu.B5)
    ## motor 1 pin Enable Pin A10
    pinENA = pyb.Pin(pyb.Pin.cpu.A10, pyb.Pin.IN, pull = pyb.Pin.PULL_UP)
    ## motor 1 object
    motor1 = motor_driver.Motor_Driver(pinB4, pinB5, tim3, pinENA)
    
    # motor 2
    ## motor 2 timer (5)
    tim5 = pyb.Timer(5, freq = 20000)
    ## motor 2 pin A0
    pinA0 = pyb.Pin(pyb.Pin.cpu.A0)
    ## motor 2 pin A1
    pinA1 = pyb.Pin(pyb.Pin.cpu.A1)
    ## motor 2 pin Enable Pin C1
    pinENB = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.IN, pull = pyb.Pin.PULL_UP)
    ## motor 2 object
    motor2 = motor_driver.Motor_Driver(pinA0, pinA1, tim5, pinENB)
    
    # encoder 1
    ## encoder 1 pin B6
    pinB6 = pyb.Pin.cpu.B6
    ## encoder 1 pin B7
    pinB7 = pyb.Pin.cpu.B7
    ## motor 1 encoder object
    encoder1 = Encoder.Encoder(pinB6, pinB7, 4)
    
    # encoder 2
    ## motor 2 encoder pin C6
    pinC6 = pyb.Pin.cpu.C6
    ## motor 2 encoder pin C7
    pinC7 = pyb.Pin.cpu.C7
    ## motor 2 encoder object
    encoder2 = Encoder.Encoder(pinC6, pinC7, 8)
    
    # controlers
    ## controler object for motor 1 with kp gain of 5
    control1 = closedLoop.ClosedLoop(10)
    
    ## controler object for motor 2 with kp gain of 5
    control2 = closedLoop.ClosedLoop(10)
    
    ## Communication reader between Computer and Nucleo board so user can type commands
    CommReader = pyb.USB_VCP()
    
    ## motor 1 reference Position
    refPos1 = 0
    ## motor 2 reference Position
    refPos2 = 0
    
    ## Time is some dumb timer function that replaces utime.ticks_ms
    Time = utime.ticks_ms
    ## @brief Defines period as what is called in main for period parameter
    Contperiod = 4
    ## @brief Time adjusts once clock reaches the period value plus the current time
    next_time = Contperiod + Time() 

    while (True):
        try:
            encoder1.updatePosition()
            encoder2.updatePosition()
            
            if (Time() >= next_time):
                next_time += Contperiod

                motor1.set_duty(control1.update(encoder1.read(),Contperiod))
                motor2.set_duty(control2.update(encoder2.read(),Contperiod))           
            
#                 print("\n_________State Data Display_________\n"
#                       "Motor1  :    theta = {:.2f}rad,\tduty(\"w\":+5%,\"s\":-5%) = {:.2f}%\n"
#                       "Motor2  :    theta = {:.2f}rad,\tduty(\"u\":+5%,\"j\":-5%) = {:.2f}%\n".format(encoder1.read(),duty1,encoder2.read(),duty2),end="")
            
                if(CommReader.any()):
                    #Reads Most recent Command
                    ## Stores the most recent key pressed
                    keyCommand = CommReader.read(1)
                    # Clears Queue
                    CommReader.read()
                else:
                    keyCommand = b' '
                    
                if(keyCommand[0] == b'k'[0]):
                    control1.set_control_gain(check_user_input("Enter a Kp:"))
                elif(keyCommand[0] == b'K'[0]):
                    control2.set_control_gain(check_user_input("Enter a Kp:"))
                elif(keyCommand[0] == b's'[0]):
                    control1.set_setpoint(check_user_input("Enter a step:"))
                    next_time = Contperiod + Time() 
                elif(keyCommand[0] == b'S'[0]):
                    control2.set_setpoint(check_user_input("Enter a step:"))
                    next_time = Contperiod + Time() 
            
        except KeyboardInterrupt:
            break
    
    motor1.disable()
    motor2.disable()
    print('Program Terminating')
    

    
