from datetime import datetime
now = datetime.now()
print now
print type(now)
now = str(datetime.now().date())
print now
print type(now)

# create single row matrix aka vector 
import numpy as np 
y = np.array([44,1.0,3])
print y
print type(y)
print y.shape
print y[2]

# Create matrix
X=np.array([[44,3,1],[54,2,1],[2,3,0]])
print X

Z=np.array([1,5,4,7,87,43,21,0,1]).reshape(3,3)
print Z
print type(Z)

# Perform addition, mulitplication division and substraction on matrix
print X * Z 
print X * y
print X + Z
print X - Z 
print X/Z