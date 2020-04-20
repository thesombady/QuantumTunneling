import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import scipy

Sample_A=pd.read_fwf('Sample_A.txt')
Sample_B=pd.read_fwf('Sample_B.txt')
Sample_C=pd.read_fwf('Sample_C.txt')
Sample_D=pd.read_fwf('Sample_D.txt')

def lists(Sample):
    Sample1=Sample
    Voltage=[]
    Current=[]
    size=int((Sample1.size)/2)
    voltage=Sample1['Voltage']
    current=Sample1['Current']
    for i in range(size):
        Voltage.append(voltage[i])
        Current.append(current[i])
    return Voltage, Current

Voltage_A, Current_A=lists(Sample_A)
Voltage_B, Current_B=lists(Sample_B)
Voltage_C, Current_C=lists(Sample_C)
Voltage_D, Current_D=lists(Sample_D)

def plotting(Voltage, Current, Type):
    if not isinstance(Voltage,list):
        raise TypeError("The type is of wrong sort")
    if not isinstance(Current,list):
        raise TypeError("The type is of wrong sort")
    plt.plot(Voltage,Current)
    plt.xlabel('Voltage')
    plt.ylabel('Current')
    plt.title('Current vs Voltage')
    name=f'Sample{Type}'
    plt.savefig(f'{name}.png')
    plt.show()

plotting(Voltage_A, Current_A, 'A')
plotting(Voltage_B, Current_B, 'B')
plotting(Voltage_C, Current_C, 'C')
plotting(Voltage_D, Current_D, 'D')
