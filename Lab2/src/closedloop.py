'''!
    @file closedloop.py
    @brief Closed loop controller containing methods to control an arbitraries motor duty cycle
    @details Controller uses the difference of reference and current values to create an error variable. the time 
             difference, and magnitude of error are then used in the update method to return a duty for the motor to be run.
    @author John Bennett
    @date   January 25, 2022
'''

class ClosedLoop:
    '''!@brief                  Interface with closed loop controller
        @details                Contains all methods that will be used in task_hardware to set the duty cycle based on closed
                                loop control.
    '''
        
    def __init__ (self, setpoint, Kp, Ki = 0, Kd = 0, satLim = [-100,100]):
        '''!@brief Constructs a closed loop controller
            @details Sets saturation limits to what is determined by task_hardware and instantiates error variables.
            @param satLim is a list containing the upper and lower bounds of saturation      
        '''
        ## @brief Instantiates gains and setpoint
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.setpoint = setpoint
        # PID Kp(*%/rad)Ki(*%/rad)Kd(*%s2/rad)
        ## @brief Instantiates duty saturation upper and lower bounds
        self.satLim = satLim
        
        ## @brief Sum of error over a difference in time
        self.esum = 0
        ## @brief Previous error
        self.laste = 0

    def update (self, read, tdif):
        ''' @brief Constructs a closed loop controller
            @details Sets saturation limits to what is determined by task_hardware and instantiates error variables.
            @param satLim is a list containing the upper and lower bounds of saturation    
            @return Sends back saturated duty value using sat method.
        '''
        ## @brief Error signal which is the difference between the expected setpoint and the measured value [read].
        e = self.setpoint - read
        #Updates sum of error (area under curve)
        self.esum += (self.laste+e)*tdif/2
        ## @brief Delta error calculated by taking difference in error values over a time difference
        dele = (e - self.laste)/tdif
        # Updates last error
        self.laste = e
        
        ## @brief Actuation signal (in duty cycle) calculation using gains and error values
        actuation_signal = self.Kp*(e) + self.Ki*(self.esum) + self.Kd*(dele) 
        return self.sat(actuation_signal)
                
    def sat(self,duty):
        ''' @brief Saturation functionallity
            @details Controls if a duty is too large from what is calculated in update method.
            @param duty is the value sent by what is calculated in update method.
            @return Sends back either the saturated limit if duty is too high or original duty based on bounds.
        '''
        if duty<self.satLim[0]:
            return self.satLim[0]
        elif duty>self.satLim[1]:
            return self.satLim[1]
        return duty

    def set_setpoint(self, point):
        self.setpoint = point

    def set_control_gain(self, gain):
        self.Kp = gain