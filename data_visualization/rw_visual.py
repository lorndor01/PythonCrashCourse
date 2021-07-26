import matplotlib.pyplot as plt
from random_walk import RandomWalk

#Keep making new walks as long as the user wants.
while True:
    #Make a random walk
    rw = RandomWalk(5_000)
    rw.fill_walk()

    plt.style.use('classic')
    fig, ax = plt.subplots(figsize=(13,8))
    point_numbers = range(rw.num_points)

    #Plot all points.
    ax.scatter(rw.x_values, rw.y_values, s=1, c = point_numbers, 
        cmap=plt.cm.Blues, edgecolors='none')

    #Emphasize first and last point.
    ax.scatter(0, 0, s=50, c = 'green', edgecolors='none')
    ax.scatter(rw.x_values[-1], rw.y_values[-1], s=50, c='red', edgecolors='none')

    #Remove the axes
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    plt.show()

    answer = input("Would you like to generate a new random walk? (y/n)")
    if answer == 'y':
        continue
    else:
        break