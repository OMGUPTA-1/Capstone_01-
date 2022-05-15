import matplotlib.pyplot as plt
import numpy as np
import math
F = 96485 #C/mole
T = 298 #K
R = 8.314

#REDLICH -KISTER MODEL for LixCoO2
U0 = -29.614
x = np.arange(0.5,0.9,0.01)
A = np.array([0.64832*(10**7),-0.65173*(10**7),0.65664*(10**7),-0.65787*(10**7),0.63021*(10**7),-0.50465*(10**7),0.27113*(10**7),-0.69045*(10**6)])
y = np.zeros([len(x)],np.float64)
z = np.zeros([len(x)],np.float64)
new = 0
for i in range(len(x)):
    for j in range(len(A)):
        #f = (A[j])*((2*x[i]-1)**(j+1))/F - (A[j])*(2*x[i]*j*(1-x[i]))/(F*(2*x[i]-1)**(1-j))
        f = (A[j])*((4+2*j)*(x[i])*(x[i]-1)+1)/((2*x[i]-1)**(1-j))
        z[i] = z[i] + f
        
    y[i] = U0 + (R*T*math.log((1-x[i])/x[i]) + z[i])/F
              
    if y[i] <0:
        y[i]=0
    
f1 = plt.figure(figsize=(15,10))
plt.plot(x,y,marker='*', color='g')
plt.title('REDLICH_KISTER MODEL-Equilibrium Potential (E) vs x in LixCoO2' , fontsize=10, fontstyle='normal')
plt.xlabel('x')
plt.ylabel('Equilibrium potential (in V)')
plt.grid()
plt.show()
