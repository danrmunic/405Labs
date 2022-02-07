"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share
import motor_driver
import closedLoop
import Encoder

def check_user_input(prompt):
    while True:
        try:
            # Convert it into float
            num = input(prompt)
            return float(num)
        except ValueError:
            print("No.. "+ num +" input is not a number. It's a string. Enter a Number")

def task_motor1 ():
    """
    Task which
    """   
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
    
    # encoder 1
    ## encoder 1 pin B6
    pinB6 = pyb.Pin.cpu.B6
    ## encoder 1 pin B7
    pinB7 = pyb.Pin.cpu.B7
    ## motor 1 encoder object
    encoder1 = Encoder.Encoder(pinB6, pinB7, 4)
    
    control1 = closedLoop.ClosedLoop(50)
    
    
    while True:
        encoder1.updatePosition()
        
        motor1.set_duty(control1.update(encoder1.read(),10))
        
        if keyShare.get() == 1:
            encoder1.zero()
            control1.set_setpoint(20)
            keyShare.put(0)
        elif keyShare.get() == 3:
            encoder1.zero()
            control1.set_setpoint(20)
        yield (0)
    
def task_motor2 ():
    """
    Task which
    """   
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
    
    # encoder 2
    ## motor 2 encoder pin C6
    pinC6 = pyb.Pin.cpu.C6
    ## motor 2 encoder pin C7
    pinC7 = pyb.Pin.cpu.C7
    ## motor 2 encoder object
    encoder2 = Encoder.Encoder(pinC6, pinC7, 8)
    
    control2 = closedLoop.ClosedLoop(50)
    
    while True:
        
        encoder2.updatePosition()        
        motor2.set_duty(control2.update(encoder2.read(),10))
        if keyShare.get() == 2:
            encoder2.zero()
            control2.set_setpoint(20)
            keyShare.put(0)
        elif keyShare.get() == 3:
            encoder2.zero()
            control2.set_setpoint(20)
            keyShare.put(0)
        yield (0)

def task_user ():
    """
    Task which
    """
    vcp = pyb.USB_VCP ()
    
    while True:
        yield (0)
        if vcp.any():
            command = vcp.read(1)
            if command == b'a':
                keyShare.put(1)
            elif command == b'd':
                keyShare.put(3)
            elif command == b'b':
                keyShare.put(2)
            elif command == b'c':
                print("read")
                keyShare.put(-1)
                
            print(vcp.read())
        
    
    
# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    
    while True:
        print ('\033[2J________Running__LAB03________ \r\n'
           'Press \"a\" or \"b\" to step motor 1 or 2. Or \"d\" for both'
           'Press \"c\" to stop and show diagnostics.')
    
        keyShare = task_share.Share ('h', thread_protect = False, name = "Share 0")
        
        num = check_user_input("Select a motor Period:")
        
        # Create the tasks. If trace is enabled for any task, memory will be
        # allocated for state transition tracing, and the application will run out
        # of memory after a while and quit. Therefore, use tracing only for 
        # debugging and set trace to False when it's not needed
        task1 = cotask.Task (task_motor1, name = 'Task_Motor1', priority = 1, 
                         period = num, profile = True, trace = False)
        task2 = cotask.Task (task_motor2, name = 'Task_Motor2', priority = 1, 
                             period = num, profile = True, trace = False)
        task3 = cotask.Task (task_user, name = 'Task_User', priority = 1, 
                             period = 100, profile = True, trace = False)
        cotask.task_list = cotask.TaskList()
        cotask.task_list.append (task1)
        cotask.task_list.append (task2)
        cotask.task_list.append (task3)
        
        # Run the memory garbage collector to ensure memory is as defragmented as
        # possible before the real-time scheduler is started
        gc.collect ()
        
        # Run the scheduler with the chosen scheduling algorithm. Quit if any 
        # character is received through the serial port
        while keyShare.get() != -1:
            cotask.task_list.pri_sched ()
        
        keyShare.put(2318008)
        
        # Print a table of task data and a table of shared information data
        print ('\n' + str (cotask.task_list))
        print (task_share.show_all ())
        #print (task1.get_trace ())
        print ('\r\n')
