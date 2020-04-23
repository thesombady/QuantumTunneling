import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import scipy
import math
from scipy import stats

emass=9.11e-31
echarge=1.602e-19
Sample_A=pd.read_fwf('Sample_A.txt')
Sample_B=pd.read_fwf('Sample_B.txt')
Sample_C=pd.read_fwf('Sample_C.txt')
Sample_D=pd.read_fwf('Sample_D.txt')
hbar=1.054571817e-34

def lists(Sample):
    """Extracts the two list from the sample """
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
    """ Plots the points given by the sample """
    if not isinstance(Voltage,list):
        raise TypeError("The type is of wrong sort")
    if not isinstance(Current,list):
        raise TypeError("The type is of wrong sort")
    plt.plot(Voltage,Current)
    plt.xlabel('Voltage')
    plt.ylabel('Current')
    plt.title(f'Current vs Voltage, Sample{Type}')
    name=f'Controled_Sample{Type}'
    plt.savefig(f'{name}.png')
    plt.show()

def plotting2(Voltage, Current, Type):
    """ Plots the curve for the single barrier"""
    if not isinstance(Voltage,list):
        raise TypeError("The type is of wrong sort")
    if not isinstance(Current,list):
        raise TypeError("The type is of wrong sort")
    effectivecurrent=[]
    effectivevoltage=[]
    for i in range(len(Current)):
        effectivecurrent.append(np.log(Current[i]))
        effectivevoltage.append(-math.sqrt(0.2*echarge-((echarge*0.3)*Voltage[i]/2)))
    plt.plot(effectivevoltage, effectivecurrent)
    plt.xlabel('(V_0-ey/2U)^(1/2)')
    plt.ylabel('Ln(I)')
    plt.title(f'Current vs Voltage, Sample{Type}')
    name=f'Effective_Sample{Type}'
    plt.savefig(f'{name}.png')
    plt.show()
    return effectivevoltage, effectivecurrent


def slope(Voltage, Current, Sample):
    """Function to retreive the slope of the single barrier """
    if not isinstance(Voltage,list):
        raise TypeError("The slope function needs lists as inputs, Voltage is flawed.")
    if not isinstance(Current,list):
        raise TypeError("The slope function needs lists as inputs, Current is flawed.")
    effectivevoltage_ar=Voltage
    effectivecurrent_ar=Current
    name=Sample
    def myfunc(x):
        return slope*x+intercept
    slope, intercept, r, p, std_err = stats.linregress(effectivevoltage_ar, effectivecurrent_ar)
    mymodel = list(map(myfunc, effectivevoltage_ar))
    plt.plot(effectivevoltage_ar, effectivecurrent_ar,'bo')
    a=slope/(2*math.sqrt((2*0.067*emass)/(hbar**2)))
    plt.ylabel('Ln(I)')
    plt.xlabel('(V_0-ey/2U)^(1/2)')
    plt.title(f'Linear regression for retrival of value a, for Sample{Sample}')
    plt.plot(effectivevoltage_ar, mymodel,'o')
    plt.savefig(f'Slope of{name}.png')
    plt.show()
    return f'Sample{name}',f'Width={a}'

def distance(Voltage, Current, Sample):
    """Computing the resonace point """
    if not isinstance(Voltage,list):
        raise TypeError("The distance function needs lists as inputs, Voltage is flawed.")
    if not isinstance(Current,list):
        raise TypeError("The distance function needs lists as inputs, Current is flawed.")
    Increase_current=[]
    precisecurrent=[]
    moreprecise=[]
    evenmoreprecise=[]
    mostprecise=[]
    lastvalue=[]
    Current=Current
    Voltage=Voltage
    number=[]
    for i in range (len(Current)-1):
        if Current[i+1]<Current[i]:
            Increase_current.append(Current[i])
            if Current[i+2]<Current[i]:
                precisecurrent.append(Current[i])
                if Current[i+3]<Current[i]:
                    moreprecise.append(Current[i])
                    if Current[i+4]<Current[i]:
                        evenmoreprecise.append(Current[i])
                        if Current[i+5]<Current[i]:
                            mostprecise.append(Current[i])
                            number.append(i)
    b=hbar**2*(math.pi)**2/(2*0.067*emass*0.3*echarge*Voltage[number[0]]/2)
    actual=math.sqrt(b)
    return mostprecise[0],actual,f'{Sample}'
        

plotting(Voltage_A, Current_A, 'A')
plotting(Voltage_B, Current_B, 'B')
plotting(Voltage_C, Current_C, 'C')
plotting(Voltage_D, Current_D, 'D')

effectivevoltage_A, effectivecurrent_A =plotting2(Voltage_A, Current_A, 'A')#Double barrier
effectivevoltage_B, effectivecurrent_B =plotting2(Voltage_B, Current_B, 'B')#Double barrier
effectivevoltage_C, effectivecurrent_C =plotting2(Voltage_C, Current_C, 'C')#Single barrier
effectivevoltage_D, effectivecurrent_D =plotting2(Voltage_D, Current_D, 'D')#Single Barrier
print(slope(effectivevoltage_C, effectivecurrent_C,'C'))
print(slope(effectivevoltage_D, effectivecurrent_D,'D'))
print(distance(Voltage_A,Current_A, 'A'))
print(distance(Voltage_B,Current_B,'B'))