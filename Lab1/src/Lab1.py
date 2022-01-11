import pyb
import utime

class Motor_Driver:
    ''' @brief A motor class implements a motor driver for an ME405 kit.
        @details Objects of this class can be used to apply PWM to a given
                 DC motor.
    '''
    def __init__ (self,motorChannel,pinCH1,pinCH2,timX,pinEN):
        ''' @brief Initializes and creates a motor object associated.
            @details Creates timer channels that will be used specific to each motor channel to control motor function.
            @param motorChannel moter driver channel
            @param pinCH1 First pin for configuring motor
            @param pinCH2 Second pin for configuring motor
            @param timX Timer Assosiated with Pins
            @param pinEN the Enable Pin for the L6206
        '''
        ## @brief Timer channel to the first motor channel for some motor
        self.t2c1 = timX.channel(motorChannel, mode = pyb.Timer.PWM, pin=pinCH1)
        ## @brief Timer channel to the second motor channel for some motor
        self.t2c2 = timX.channel(motorChannel+1, mode = pyb.Timer.PWM, pin=pinCH2)
        
        pinEN.high()
        
    def set_duty (self, duty):
        
        ''' @brief Set the PWM duty cycle for the motor channel.
            @details This method sets the duty cycle to be sent
                    to the motor to the given level. Positive values
                    cause effort in one direction, negative values
                    in the opposite direction.
            @param duty A signed number holding the duty
                      cycle of the PWM signal sent to the motor
        '''
        #if duty is positive then set the first channel to specified duty and other to 0.
        if duty >= 0:
            if duty <= 100:
                self.t2c1.pulse_width_percent(100)
                self.t2c2.pulse_width_percent(100-duty)
            else:
                self.t2c1.pulse_width_percent(100)
                self.t2c2.pulse_width_percent(0)
        #if duty is negative then set the second channel to a specified duty (negative sign will make duty positive) and other to 0.
        elif duty < 0:
            if duty >= -100:
                self.t2c2.pulse_width_percent(100)
                self.t2c1.pulse_width_percent(100+duty)
            else:
                self.t2c2.pulse_width_percent(100)
                self.t2c1.pulse_width_percent(0)
                
if __name__ == '__main__':
    tim3 = pyb.Timer(3, freq = 20000)
    channel1 = 1
    pinB4 = pyb.Pin(pyb.Pin.cpu.B4)
    pinB5 = pyb.Pin(pyb.Pin.cpu.B5)
    pinENA = pyb.Pin(pyb.Pin.cpu.A10, pyb.Pin.IN, pull = pyb.Pin.PULL_UP)
    print('run')
    
    motor1 = Motor_Driver(channel1, pinB4, pinB5, tim3, pinENA)
    motor1.set_duty(50)
    utime.sleep(2)
    motor1.set_duty(-100)
    utime.sleep(2)
    motor1.set_duty(0)
    