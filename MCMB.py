

#Redlich Klister MOdel for anode MCMB



import matplotlib.pyplot as plt
import numpy as np
import math
F = 96485 #C/mole
T = 298 #K
R = 8.314

U0 =  1.720
A = np.array([0.35799*(10**6),0.35008*(10**6),0.35247*(10**6),0.35692*(10**6),0.38633*(10**6),
              0.35908*(10**6),0.28794*(10**6),0.14979*(10**6),0.39912*(10**6),0.96172*(10**6) ,0.63262*(10**6)])
x = np.arange(0.1,0.9,0.01)
y = np.zeros([len(x)],np.float64)
z = np.zeros([len(x)],np.float64)
new = 0
for i in range(len(x)):
    for j in range(len(A)):
        #new = (A[j])*((2*x[i]-1)**(j+1))/F - (A[j])*(2*x[i]*j-2*j*(x[i]**2))/(F*(2*x[i]-1)**(1-j))
        new = ((-A[j]))*((4+2*j)*(x[i])*(x[i]-1)+1)/((2*x[i]-1)**(1-j))
        z[i] = z[i] + new
        
    y[i] = (-1*U0) + (R*T*math.log((1-x[i])/x[i]) + z[i])/F
              
    if y[i] <0:
        y[i]=0

for i in range(len(y)) :
    print(round(y[i],4))
    print("\n")
f1 = plt.figure(figsize=(15,10))
plt.plot(x,y,marker='*', color='g')
plt.title('REDLICH_KISTER MODEL-Equilibrium Potential (E) vs x in MCMB' , fontsize=13, fontstyle='italic')
plt.xlabel('x')
plt.ylabel('Equilibrium potential (in V)')
plt.grid()
plt.show()
