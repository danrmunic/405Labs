import matplotlib.pyplot as plt

def plotcsv(file):
    ''' 
        @brief              unpacks data from a CSV file and plots it
    '''
    ## X Data, Columns 1
    x = []
    ## Y Data, Columns 2
    y = []
    
    # reads File and sorts data into lists of data
    with open(file, 'r',encoding='utf-8-sig') as file:
        rawdata = file.read()
    for val in [[ints for ints in rows.strip().split(',')] for rows in rawdata.strip().split('\n')]:
        # Converts the first two columns into floats and records them
        try:
            num1 = float(val[0])
            num2 = float(val[1])
        except:
            pass
        else:
            x.append(num1)
            y.append(num2)
            
    # Plots data
    plt.plot(x,y)
    plt.ylabel('y Data');
    plt.xlabel('x Data');
    plt.title('CSV file: {:}, plotted as (x,y) data'.format(disfile));
    
if __name__ == '__main__':
    ''' 
        @brief              runs csv file plotting function
    '''
    disfile = "test2.csv"
    plotcsv(disfile)
    
