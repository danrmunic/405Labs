'''!
    @file Lab03_PC.py
    @brief Runs PC Code that Communicates with the micro Python Board through the serial board running Lab03 and plots responce.
    @author Rodolfo Diaz
    @author Daniel Munic
    @author John Bennett
    @date Febuary 7, 2022    
'''

import serial
import time
import matplotlib.pyplot as plt

# ## Selected Motor Period
# MotorP = 0
def plotCOMData(s_port):
    '''!@brief reads data from s_port seperates it into x, y data and plots it.
        @param Current serial port
    '''
    ## X Data, Columns 1
    x = []
    ## Y Data, Columns 2
    y = []
    while True:
        val = [ints for ints in s_port.readline().replace(b'\r\n', b'').split(b',')]
        # Converts the first two columns into floats and records them
        try:
            num1 = float(val[0])
            num2 = float(val[1])
        except:
            if val[0] == b'#STOP#':
                break
        else:
            x.append(num1)
            y.append(num2)
    # Plots data
    plt.figure(1)
    plt.plot(x,y,1)
    plt.ylabel('Position rad')
    plt.xlabel('Time ms')
    #plt.ylim(0,max(y)+1)
    plt.title('Plotted as (x,y) data. Motor period = {:}'.format(MotorP))
    plt.show()
    
def write_step(s_port):
    '''!@brief a generator that iterates through writting to the s_port.
        @param Current serial port
    '''
    readVal = "0"
    tf = time.time()+3

    while True:
        yield readVal
        
        s_port.reset_output_buffer()
        readVal = s_port.readline().replace(b'\r\n', b'').decode()
        if ":" in readVal:
            s_port.reset_input_buffer()
            global MotorP
            MotorP = input(readVal)
            print(MotorP)
            s_port.write(MotorP.encode("UTF-8") + b'\r\n')
            time.sleep(.1)
        elif tf < time.time():
            s_port.reset_input_buffer()
            s_port.write(input("input a \"a\" \"b\" \"c\"  or \"d\" :").encode("UTF-8") + b'\r\n')
            
            tf = time.time() + 3
            time.sleep(.1)
        
        elif not (readVal == "" or readVal == '#START#'):
            print(readVal)

if __name__ == '__main__':
    '''!@brief Communicates with the micro Python Board through the serial board
        @details Opens a spesified seiral port and iterates through writting new motor periods and step inputs.
                 Then plotting it.
    '''
    COM = 'COM12'
    Speed = 115200
    
    readVal = b"hi"    
    
    with serial.Serial(COM, Speed,timeout=1) as s_port:
        commandCycle = write_step(s_port)
        s_port.reset_output_buffer()

        while (True):
            try:
                if readVal == '#START#':
                    plotCOMData(s_port)
                    readVal = "hi again!"
                else:
                    readVal = next(commandCycle)

            except KeyboardInterrupt:      
                break

    