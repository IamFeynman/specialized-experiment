import numpy as np
import matplotlib.pyplot as plt
import sympy as sy

x = np.array([1, 1, 1, 1, 1, 1])    #x[n]
h = np.array([0, 1, 2, 3, 4, 5])    #h[n]

# 卷积和
y = np.convolve(x, h)

plt.subplot(3, 1, 1)
plt.xlim(-1, len(y))
plt.stem(range(len(x)), x)

plt.subplot(3, 1, 2)
plt.xlim(-1, len(y))
plt.stem(range(len(x)), h)

plt.subplot(3, 1, 3)
plt.xlim(-1, len(y))
plt.stem(range(len(y)), y, basefmt="-")

plt.show()