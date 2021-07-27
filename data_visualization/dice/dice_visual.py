from dice import Dice
from plotly.graph_objs import Bar, Layout
from plotly import offline

#Create a D6
dice_1 = Dice()
dice_2 = Dice()

#Make some rolls and store results.
results = []
for roll in range(1_000_000):
    result = dice_1.roll() + dice_2.roll()
    results.append(result)

#Analyze the results.
frequencies = []
max_result = dice_1.num_sides + dice_2.num_sides
for value in range(2, max_result+1):
    frequency = results.count(value)
    frequencies.append(frequency)

#Visualize the result
x_values = list(range(2,max_result+1))
data = Bar(x=x_values, y=frequencies)

x_axis_config = {'title':'Result', 'dtick':1}
y_axis_config = {'title':"Frequency of Result"}
my_layout = Layout(title=f"Results of rolling  D{dice_1.num_sides} dice {len(results)} times",
    xaxis=x_axis_config, yaxis=y_axis_config)
offline.plot({'data':data, 'layout':my_layout}, filename=f'result.html')