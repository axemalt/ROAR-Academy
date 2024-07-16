## This is course material for Introduction to Python Scientific Programming
## Example code: gradient_descent.py
## Author: Allen Y. Yang
##
## (c) Copyright 2020. Intelligent Racing Inc. Not permitted for commercial use

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

fig = plt.figure()

sample_count = 100
x_sample = 10*np.random.random(sample_count)-5
y_sample = 2*x_sample - 1 + np.random.normal(0, 1.0, sample_count)

# plots the parameter space
ax2 = fig.add_subplot(1,1,1, projection = '3d')

def penalty(para_a, para_b):
    global x_sample, y_sample, sample_count

    squares = (y_sample - para_a*x_sample - para_b)**2
    return 1/2/sample_count*np.sum(squares)

a_arr, b_arr = np.meshgrid(np.arange(-5, 5, 0.1), np.arange(-5, 5, 0.1) )

func_value = np.zeros(a_arr.shape)
for x in range(a_arr.shape[0]):
    for y in range(a_arr.shape[1]):
            func_value[x, y] = penalty(a_arr[x, y], b_arr[x, y])

ax2.plot_surface(a_arr, b_arr, func_value, color = 'red', alpha = 0.8)
ax2.set_xlabel('a parameter')
ax2.set_ylabel('b parameter')
ax2.set_zlabel('f(a, b)')

# Plot the gradient descent
def grad(aa):
    grad_aa = np.zeros(2)
    update_vector = (y_sample - aa[0] * x_sample - aa[1])
    grad_aa[0] = - 1/sample_count * x_sample.dot(update_vector)
    grad_aa[1] = - 1/sample_count * np.sum(update_vector)
    return grad_aa

aa = np.array([-4, 4])
delta = np.inf
epsilon = 0.001
learn_rate = 0.01
step_count = 0
ax2.scatter(aa[0], aa[1], penalty(aa[0],aa[1]), c='b', s=100, marker='*')
# Update vector aa
while delta > epsilon:
    # Gradient Descent
    aa_next = aa - learn_rate * grad(aa)
    # Plot the animation
    ax2.plot([aa[0],aa_next[0]],[aa[1], aa_next[1]],\
        [penalty(aa[0],aa[1]), penalty(aa_next[0],aa_next[1]) ], 'ko-')
    delta = np.linalg.norm(aa - aa_next)
    aa = aa_next
    step_count +=1
    fig.canvas.draw_idle()
    plt.pause(0.1)

print('Optimal result: ', aa)
ax2.scatter(aa[0], aa[1], penalty(aa[0],aa[1]), c='b', s=100, marker='*')
plt.show()
print('Step Count:', step_count)