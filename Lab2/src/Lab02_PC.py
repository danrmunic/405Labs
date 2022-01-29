import serial
import time
import matplotlib.pyplot as plt

def plotCOMData(COM, Speed):
    ''' 
        @brief              unpacks data from a CSV file and plots it
    '''
    ## X Data, Columns 1
    x = []
    ## Y Data, Columns 2
    y = []
    with serial.Serial(COM, Speed) as s_port:
        while s_port.readable():
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
    print('exit')
    # Plots data
    plt.plot(x,y)
    plt.ylabel('Position rad');
    plt.xlabel('Time ms');
    plt.title('Plotted as (x,y) data');
    
def write_step(COM, Speed):
    with serial.Serial(COM, Speed) as s_port:
        s_port.write(b'k')
        kp = input("Enter a Kp").encode("UTF-8")
        s_port.write(kp + b'\r\n')
        time.sleep(.5)
        s_port.write(b's')
        s = input("Enter a Step").encode("UTF-8")
        s_port.write(s + b'\r\n')    

if __name__ == '__main__':
    ''' 
        @brief              runs csv file plotting function
    '''
    
    COM = 'COM12'
    Speed = 115200
    while (True):
        try:
            write_step(COM, Speed)
                
            for i in range(5,1,-1):
                print(i)
                time.sleep(.5)
                    
            plotCOMData(COM, Speed)
                    
        except KeyboardInterrupt:      
            break

    