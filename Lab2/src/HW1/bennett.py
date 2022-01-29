import matplotlib.pyplot as plt
import random




        
def Student_Health_Gen():
    NO_FLU = "NO_FLU"
    MILD_FLU = "MILD_FLU"
    SEVERE_FLU = "SEVERE_FLU"
    RECOVERED = "RECOVERED"
    
    state = NO_FLU
    vaccinated = False
    
    while True:
        
        yield state
        
        vaccinated = random.randint(0,9) == 1 or vaccinated
        health = random.randint(0,1)
        
        if state == NO_FLU:
            if vaccinated or health == 0:
                state = MILD_FLU
                     
        elif state == MILD_FLU:
            if vaccinated:
                state = RECOVERED
            elif health == 1:
                state = NO_FLU
            else:
                state = SEVERE_FLU
                
        elif state == SEVERE_FLU:
            if vaccinated or health == 1:
                state = MILD_FLU
                
        elif state == RECOVERED:
            pass
        
    
if __name__ == '__main__':
    Clayton = Student_Health_Gen()
    x = [i for i in range(0,51)]
    y = []
    for i in x:
        y.append(next(Clayton))
    
    
    # Plots data
    plt.plot(x,y)
    plt.xlabel('Day #')
    plt.title("Student Flu Symptoms Progression Over 50 Days");