import math

c = 4190
um = 0.0058
ut = 0.2888
uT = 0.5774

T = 83.7
t = 252.89
m = 1.497

uc = math.sqrt((c*T*um/t)**2+(c*m*uT/t)**2+(-c*T*m*ut/(t**2))**2)
print(uc)