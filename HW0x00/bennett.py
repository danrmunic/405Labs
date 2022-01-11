import matplotlib.pyplot as plt

if __name__ == '__main__':
    ''' 
        @brief              unpacks data from a CSV file and plots it
    '''
    plt.clf()
    disfile = "test2.csv"
    
    ## X Data, Columns 1
    x = []
    ## Y Data, Columns 2
    y = []
    
    # reads File and sorts data into lists of data
    with open(disfile, 'r') as file:
        rawdata = file.read()
        rows = [[ints for ints in rows.strip().split(',')] for rows in rawdata.strip().split('\n')]
    for val in rows:
        # Converts the first two columns into floats and records them
        if val[0].replace('-','').replace('.','').isnumeric() and val[1].replace('-','').replace('.','').isnumeric():
            x.append(float(val[0]))
            y.append(float(val[1]))
    
    # Plots data
    plt.plot(x,y)
    plt.ylabel('y Data');
    plt.xlabel('x Data');
    plt.title('CSV file: {:}, plotted as (x,y) data'.format(disfile));