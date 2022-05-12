    import matplotlib.pyplot as plt
    import numpy as np
    import math
    F = 96485 #C/mole
    T = 298 #K
    R = 8.314

    #REDLICH -KISTER MODEL for LixCoO2
    U0 = -29.614
    x = np.arange(0.5,0.9,0.01)
    A = np.zeros((8,1))
    #A = np.array([0.64832*(10**7),-0.65173*(10**7),0.65664*(10**7),-0.65787*(10**7),0.63021*(10**7),-0.50465*(10**7),0.27113*(10**7),-0.69045*(10**6)])

    y = np.zeros([len(x)],np.float64)
    z = np.zeros([len(x)],np.float64)
    new = 0
    def func():
        for i in range(len(x)):
            t = [0 for k in range(8)]
            for j in range(8):
                t[j] =  ((4+2*j)*(x[i])*(x[i]-1)+1)/((2*x[i]-1)**(1-j))
                
                #f = (A[j])*((4+2*j)*(x[i])*(x[i]-1)+1)/((2*x[i]-1)**(1-j))
                #z[i] = z[i] + f
                
            t = np.array(t) # converted list to numpy array
            print(t.shape)
            y[i] = U0 + (R*T*math.log((1-x[i])/x[i]) + z[i])/F
                      
        if y[i] <0:
        y[i]=0
        return y

    print(x)
    print(y)    
    f1 = plt.figure(figsize=(15,10))
    plt.plot(x,y,marker='*', color='g')
    plt.title('REDLICH_KISTER MODEL-Equilibrium Potential (E) vs x in LixCoO2' , fontsize=10, fontstyle='normal')
    plt.xlabel('x')
    plt.ylabel('Equilibrium potential (in V)')
    plt.grid()
    plt.show()
