'''!
    @file main.py
    @brief Creates an LED Sawtooth Pattern for Lab 0
    @details Pin A0 and Pin 3v3 are used in creating a 5 second Sawtooth partern on a nucleo
    @author Cade Liberty
    @author Daniel Munic
    @author John Bennett
    @date January 4, 2022    
'''
import pyb
import utime

def led_setup ():
    '''!
        @brief Sets up pins and timers and channels for the led pattern
        @details Pin A0, Timer 2, and Channel 1 (inverted PWM) are set up for use in the LED pattern
    '''
   pinA0 = pyb.Pin (pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
   tim2 = pyb.Timer (2, freq=20000)
   global ch1
   ch1 = tim2.channel (1, pyb.Timer.PWM_INVERTED, pin=pinA0)
   

def led_brightness(duty):
    '''!
        @brief Sets the Duty to Channel 1's PWM
        @details Controls the LED brightness with an inputed parameter called duty
        @param duty is a value between 0 and 100, 100 is high, 0 is low
    '''
   ch1.pulse_width_percent (duty)

if __name__ == "__main__":
    '''!
        @brief Controls the LED responce
        @details First sets up LED then repeatedly recalculates the current duty to
                create a sawtooth pattern. Clrl+C terminates Program.
    '''
    led_setup ()

    ##  The current state
    State = 0
    ##  Keeps of current time
    tcur = -1
    ##  Current time
    to = -1  
    ##  Calculated Duty value between 0-100 for LED brightness
    P = 0
         
    while (True):
        try:
            tcur = utime.ticks_ms()
            delt = utime.ticks_diff(tcur,to)
            
            if (State == 0):
                #Run the State 0 code
                print('Welcome, LED enthusiasts here is a blinking LED\n'
                      'with a Sawtooth pattern'
                      '\nToo stop press Cntrl+C.')
                
                State = 1; # Transisions to state 1
                
            elif (State == 1):
                # Runs the State 1 code
                # Generates Sawtooth wave responce with a period of 5000 ms
                P = ((delt) % 5000) /50
            led_brightness(P)
            
        #If there is an interuption break
        except KeyboardInterrupt:
            break
        
    print('Program Terminating')