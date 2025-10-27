import numpy as np
n = 10000000
set_n = set(np.arange(2, n))
for i in np.arange(2,n):
    setforsub = set()
    for j in np.arange(2,(n//i + 1)):
        set_n.discard(i*j)
    
print(set_n)
