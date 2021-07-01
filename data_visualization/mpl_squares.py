import matplotlib.pyplot as plt

input_values = range(1,1000)
squares = [x**2 for x in input_values]

plt.style.use('seaborn')

fig, ax = plt.subplots()
ax.scatter(input_values, squares, s=10, c=squares, cmap=plt.cm.Blues)

#Set chart title and label axes.
ax.set_title("Square Numbers", fontsize=24)
ax.set_xlabel("Value", fontsize=14)
ax.set_ylabel("Square of Value", fontsize=14)

#Set size of tick labels.
ax.tick_params(axis='both', labelsize=14)

#Set the range for each axis
ax.axis([0,1000, 0, 1000000])

plt.savefig('squares_plot.png')