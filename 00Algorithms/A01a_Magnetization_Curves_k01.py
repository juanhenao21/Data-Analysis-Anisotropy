
# coding: utf-8

# ###### Algorithm to plot the magnetization curves and compute the critical temperatures and critical exponents of magnetic thin films varying the thickness. The simulation was made using a constant anisotropy K = 0.1, and changing a parameter Gamma (0.037, 0.111, 0.333, 1.000, 3.000 and 9.000) related with the superficial anisotropy. The thickness used in the simulation were d = 2, 4, 6, 8, 10, 12, 14 and 16. The critical temperature was obtained using a regression with the library curve_fit, that also give us the critical exponent of each simulation.

# In[4]:

#%matplotlib inline


# # Files management

# In[5]:

import glob
import re
import collections
import os


# In[6]:

# Glob sirve para buscar archivos
files = {g: sorted(glob.glob('../d*/k0.1/gamma%s/resultados.dat' % g)) for g in ('0.037', '0.111', '0.333', '1.000', '3.000', '9.000')}
files = collections.OrderedDict(sorted(files.items()))

filename = re.compile(r'../d(?P<d>\d+)/k[0-9.]+/gamma[0-9.]+/resultados.dat')

for gamma, filenames in files.items():
    for file in filenames:
        match = filename.match(file)
        
os.makedirs('../01Magnetization_Curves')
os.makedirs('../02Critical_Values')


# ###### The file 'resultados.dat'  contains the following columns with information
# 
# - Temperature
# - Mean Energy
# - Normalized Energy
# - Specific Heat
# - Mean Magnetization
# - Normalized Magnetization
# - Susceptibilty

# # Importing Modules

# In[7]:

import numpy as np
from matplotlib import pyplot as plt
from numpy import loadtxt
from scipy.optimize import curve_fit


# ###### Function to obtain the value of the critical temperature and the critical exponent using curve_fit.

# In[8]:

def magnetization(T, Tc, beta, A):
    result = np.zeros_like(T)
    result[T < Tc] = A * (1 - T[T < Tc] / Tc) ** beta
    return result


# ###### Ploting Magnetization vs Temperature for each Gamma and different thickness. Computation of the values of the critical temperatures and critical exponents of each simulation.

# In[9]:

for fileGamma in files:
    file_save = open('../02Critical_Values/01aTc_k01_%s.txt' % fileGamma, 'a')
    plt.figure(figsize=(16,9))

    print("\nGamma = ", fileGamma)
    
    for file in files[fileGamma]:
        temp, mag = loadtxt(file, usecols=(0, 5, ), unpack=True)
        d = filename.match(file).groupdict()['d']
                
        print("d = ", d)

        plt.subplot(211)
        plt.plot(temp, mag, label= "$d = %s$" % (d, ))
        plt.legend()
        plt.xlabel('Temperatura (K)')
        plt.ylabel('Magnetización')
        plt.title('Curvas de Magnetización k = 0.1 - Gamma = %s' % fileGamma)
        plt.grid(True)
        plt.tight_layout()

        params, corr = curve_fit(magnetization, temp, mag, p0 = (450, 0.5, 1.0))

        plt.subplot(212)
        plt.plot(temp,magnetization(temp,*params), '-g', linewidth=2)#, label = 'fit')
        plt.plot(temp, mag, 'ok', ms=2)#, label = "Magnetization")
        plt.xlabel('Temperatura (K)')
        plt.ylabel('Magnetización')
        plt.grid(False)

        print('Tc (d',d,') = ', params[0])
        print('Ec (d',d,') = ', params[1], '\n')

        file_save.write(d)
        file_save.write(' ')
        file_save.write(str(params[0]))
        file_save.write(' ')
        file_save.write(str(params[1]))
        file_save.write('\n')

    plt.savefig('../01Magnetization_Curves/01a_Graph_k01_Gamma%s.png' % fileGamma)
    plt.close()

    file_save.close()


# In[ ]:



