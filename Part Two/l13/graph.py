import matplotlib.pyplot as plt
import numpy as np

points = np.array([[1, 2], [2, 4], [3, 1]])

plt.plot(points[:, 0], points[:, 1])
plt.xlim(1, 3)
plt.ylim(1, 4)
plt.xticks(np.arange(1,3.1,.5), [str(i/2) for i in range(2, 7, 1)])

plt.title("Sample graph!")
plt.xlabel("x - axis")
plt.ylabel("y - axis")

plt.tick_params(left=True, top=True)

plt.show()