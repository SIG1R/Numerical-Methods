from direct_methods import Upper_Triangular as UT
import numpy as np

m = np.matrix([[200,2,1],[0,10,1],[0,0,5]])
b = np.array([5,10,20])

lower = UT()
lower.set_parameters(m,b)
lower.fit()
print(lower.solution)
for i in lower.solution:
    print(i)
