import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
import matplotlib.pyplot as plt

jasper_data = pd.read_csv('Jasper_Daily_Weather_Data.csv', encoding= 'unicode_escape')  #Importing the daily data
jasper_data['Date (Local Standard Time)'] = pd.to_datetime(jasper_data['Date (Local Standard Time)']) #Converting tbe 'Date (Local Standard Time)' row to Date time data type for easy use to bundle by week, month etc

jasper_data = jasper_data[(jasper_data['Air Temp. Min. Record Completeness (%)'] == 100)]   #Filtering Each completeness column and only taking rows with 100 in the specified column
jasper_data = jasper_data[jasper_data['Air Temp. Max. Record Completeness (%)'] == 100]
jasper_data = jasper_data[jasper_data['Air Temp. Avg. Record Completeness (%)']  == 100]
jasper_data = jasper_data[jasper_data['Wind Speed 10 m Avg. Record Completeness (%)'] == 100]
jasper_data = jasper_data[jasper_data['Wind Dir. 10 m Avg. Record Completeness (%)'] == 100]

monthly_average_windspeed = jasper_data.groupby(pd.Grouper(key='Date (Local Standard Time)',freq='MS'))['Wind Speed 10 m Avg. (km/h)'].mean().reset_index()   #Groups wind speed data by the respective month and takes the average of it
monthly_average_windspeed_direction = jasper_data.groupby(pd.Grouper(key='Date (Local Standard Time)',freq='MS'))['Wind Dir. 10 m Avg. '].mean().reset_index() #groups wind direction average in each month and takes the average of all days avg direction

fig = plt.figure(figsize = [15,10]) #Creates the figure for everything to be graphed on
fig.suptitle('Daily Weather Data Recorded in Jasper National Park', family = 'Times New Roman', size = 15) #creates a title for the entire figure outlining the data set

r = monthly_average_windspeed['Wind Speed 10 m Avg. (km/h)'] #Makes the magnitude of the polar plot the monthly avg windspeed
theta = monthly_average_windspeed_direction['Wind Dir. 10 m Avg. '] #makes the angle (or poisiton on the polar plot the avg direction for each month)
colors = r

ax1 = fig.add_subplot(221, projection='polar')  #adds a subplot for the graph in the figure first spot of 2x2 grid
ax1.set

ax1.set_theta_zero_location('N')    #Sets zero degrees on the plot to represent geographic north (as wind measurements to take North as 0 degrees, NE as 45, E as 90, etc)
ax1.set_theta_direction(-1)
c = ax1.scatter(theta, r, c = r, cmap='plasma')   #creates the plot specifying the angle (theta) the magnitude of wind speed (r) what to base the color map off of (the magnitude r) and the type of colormap used

#Formatting the graph
ax1.set_title('Monthly Average Wind Speed and Direction', family = 'Times New Roman', size = 12, pad = 5)
ax1.set_rmin(4)
ax1.set_rmax(10)
ax1.set_xticks(ax1.get_xticks()) #Sets a FixedLocator for the Fixed Values I set below (Gets rid of warning)
ax1.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']) #Labels the corresponding angles (0, 45, 90, 135, 180, 225, 270, 315, 360) as thier geographical counterparts
#ax1.set_thetamin(0)
#ax1.set_thetamax(360)
ax1.tick_params('x', size = 2)
ax1.set_rlabel_position(25) #sets the magnitude label postion at 25 degrees

cbar = fig.colorbar(c) #adds the colour bar to the plot
cbar.set_label('Wind Speed Range (km/h)', family = 'Times New Roman') #labels the colorbar

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r = r,
    theta = theta,
    name='11-14 m/s',
    mode = 'markers',
    marker_color='rgb(106,81,163)'
))


fig.update_traces(text=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'])
fig.update_layout(
    title='Wind Speed Distribution in Laurel, NE',
    font_size=16,
    legend_font_size=16,
    polar_radialaxis_ticksuffix='%',
    polar_angularaxis_rotation=90,

)
fig.show()


