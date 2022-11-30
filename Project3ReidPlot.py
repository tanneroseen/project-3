import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import plotly.io as pio
import matplotlib.pyplot as plt

jasper_data = pd.read_csv('Jasper_Daily_Weather_Data.csv', encoding= 'unicode_escape')  #Importing the daily data
jasper_data['Date (Local Standard Time)'] = pd.to_datetime(jasper_data['Date (Local Standard Time)']) #Converting tbe 'Date (Local Standard Time)' row to Date time data type for easy use to bundle by week, month etc

jasper_data = jasper_data[jasper_data['Air Temp. Min. Record Completeness (%)'] == 100]   #Filtering Each completeness column and only taking rows with 100 in the specified column
jasper_data = jasper_data[jasper_data['Air Temp. Max. Record Completeness (%)'] == 100]
jasper_data = jasper_data[jasper_data['Air Temp. Avg. Record Completeness (%)']  == 100]
jasper_data = jasper_data[jasper_data['Wind Speed 10 m Avg. Record Completeness (%)'] == 100]
jasper_data = jasper_data[jasper_data['Wind Dir. 10 m Avg. Record Completeness (%)'] == 100]

avg_precip = jasper_data.groupby(pd.Grouper(key= 'Date (Local Standard Time)', freq='M'))['Precip. (mm)'].sum() #Sums the percipitation in each month
avg_temp = jasper_data.groupby(pd.Grouper(key= 'Date (Local Standard Time)', freq='M'))['Air Temp. Avg. (C)'].mean() #Does the avg monthly air temp from the daily averages
min_temp = min_grouped_by_week = jasper_data.groupby(pd.Grouper(key = 'Date (Local Standard Time)', freq = 'M'))['Air Temp. Min. (C)'].min()

#plt start **
#fig = plt.figure(figsize = [15,10]) #Creates the figure for everything to be graphed on
#ax3 = fig.add_subplot(212) #adds a subplot for the graph in the figure (2nd spot in 2x1 grid)

#Manipulating the data from the CSV to give insight
min_grouped_by_week = jasper_data.groupby(pd.Grouper(key = 'Date (Local Standard Time)', freq = 'W-SUN'))['Air Temp. Min. (C)'].min() #On graph date shown is end of the week
max_grouped_by_week = jasper_data.groupby(pd.Grouper(key = 'Date (Local Standard Time)', freq = 'W-SUN'))['Air Temp. Max. (C)'].max()
differce_in_max_and_min = max_grouped_by_week - min_grouped_by_week

min_xvals = min_grouped_by_week.keys()
min_yvals = list(min_grouped_by_week)
max_xvals = max_grouped_by_week.keys()
max_yvals = list(max_grouped_by_week)
difference_xvals = differce_in_max_and_min.keys()
difference_yvals = list(differce_in_max_and_min)
zero_linex = min_grouped_by_week.keys()
zero_liney = [0 for x in range(len(min_xvals))]


#Plots the data with time
xlabel = ['Date']
ylabel = ['Temperature (\u00B0C)']
'''
min_grouped_by_week.plot(color = 'royalblue', label = 'Minimum', alpha = 0.4)
max_grouped_by_week.plot(color = 'r', label = 'Maximum', alpha = 0.4)
differce_in_max_and_min.plot(color = 'limegreen', label = 'Difference', alpha = 1)
'''
'''
#Formatting the Graph
plt.title('Weekly Temperature Extremes and their Difference', family = 'Times New Roman', size = 12, pad = 5) #\/
plt.xlabel('Date', family = 'Times New Roman', size = 10)
plt.ylabel('Temperature (\u00B0C)', family = 'Times New Roman', size = 10)
plt.axhline(color = 'k', alpha = 0.25) #creates line at temperature of 0 degrees celcius (freezing temp)
plt.minorticks_on()
plt.legend(loc = 'lower right', shadow = True)
plt.tick_params(axis = 'both', labelsize = 8)
'''
#plt end **
#plotly start **
fig3 = go.Figure()

fig3.add_trace(go.Scatter(
    x=min_xvals,
    y=min_yvals,
    mode="lines+markers",
    marker=dict(
        color='royalblue'
        ),
    ))

fig3.add_trace(go.Scatter(
x=max_xvals,
y=max_yvals,
mode="lines+markers"
#color = 'r',
))
fig3.add_trace(go.Scatter(
x=difference_xvals,
y=difference_yvals,
mode="lines+markers"
#color = 'limegreen',
))
fig3.add_trace(go.Scatter(
x=zero_linex,
y=zero_liney,
mode="lines+markers"
#color = 'k',
))
#pio.show(fig)
fig3.show()
#pl0tly end **