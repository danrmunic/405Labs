import serial
import time
import matplotlib.pyplot as plt

kp = 0
def plotCOMData(s_port):
    ''' 
        @brief              unpacks data from a CSV file and plots it
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
    plt.title('Plotted as (x,y) data. Kp = {:}'.format(kp))
    plt.show()
    
def write_step(s_port):
    b = 1
    readVal = "0"
    while True:
        yield readVal
        if b==1:
            s_port.write(b'k\r\n')
        else:
            s_port.write(b's\r\n')
        time.sleep(.5)
        
        
        s_port.reset_output_buffer()
        readVal = s_port.readline().replace(b'\r\n', b'')
        if readVal != b"#START#":
            s_port.reset_input_buffer()
            s_port.write(input(readVal).encode("UTF-8") + b'\r\n')
            time.sleep(.1)
            if b == 0:
                time.sleep(2)
            if b == 1:
                global kp
                kp = s_port.readline().replace(b'\r\n', b'').decode()
            s_port.readline()
            b^=1

        

        

if __name__ == '__main__':
    ''' 
        @brief              runs csv file plotting function
    '''
    
    COM = 'COM12'
    Speed = 115200
    
    readVal = b"hi"    
    
    with serial.Serial(COM, Speed,timeout=1) as s_port:
        commandCycle = write_step(s_port)

        
        while (True):
            try:
                if readVal == b'#START#':
                    plotCOMData(s_port)
                    readVal = "hi again!"
                else:
                    readVal = next(commandCycle)

            except KeyboardInterrupt:      
                break

    