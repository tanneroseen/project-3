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

monthly_average_windspeed = jasper_data.groupby(pd.Grouper(key='Date (Local Standard Time)',freq='MS'))['Wind Speed 10 m Avg. (km/h)'].mean().reset_index()  #Groups wind speed data by the respective month and takes the average of it
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

#Creates an extra column to populate in the following loop
monthly_average_windspeed_direction['Compass Direction'] = None

#Between degree values, the values are assigned a direction based on a compass and they are shown in the figure when you hover your mouse over plotted values.
for count, direction in enumerate(monthly_average_windspeed_direction['Wind Dir. 10 m Avg. ']):
    if 112.5 < direction < 157.5:
        monthly_average_windspeed_direction.iloc[count, 2] = 'S-E'
    elif 157.5 < direction < 202.5:
        monthly_average_windspeed_direction.iloc[count, 2] = 'South'
    if 202.5 < direction < 247.5:
        monthly_average_windspeed_direction.iloc[count, 2] = 'S-w'
    elif 247.5 < direction < 292.5:
        monthly_average_windspeed_direction.iloc[count, 2] = 'West'
    if 292.5 < direction < 337.5:
        monthly_average_windspeed_direction.iloc[count, 2] = 'N-W'
    elif (337.5 < direction < 360) or (0 < direction < 22.5):
        monthly_average_windspeed_direction.iloc[count, 2] = 'North'
    elif (22.5 < direction < 67.5) or (0 < direction < 22.5):
        monthly_average_windspeed_direction.iloc[count, 2] = 'N-E'

#Converting the dates in the dataframe into strings so that they can be displayed in the graph easily
monthly_average_windspeed_direction['Datetime as String'] = monthly_average_windspeed_direction['Date (Local Standard Time)'].astype(str)


fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r = r,
    theta = theta,
    mode = 'markers',
    marker = dict(
        size=2.5*r,
        #cmax=10,
        #cmin=0,
        color=r,
        colorbar=dict(
            title="Wind Speed Range (km/h)"
        ),
        colorscale="plasma"
)))


fig.update_traces(
    text=monthly_average_windspeed_direction.iloc[:,[3,2]],
    hovertemplate = 'Date: %{text[0]} <extra></extra>' + 
    '<br>Windspeed: %{r:.2f} km/h' +
    '<br>Direction: %{theta:.2f}°, %{text[1]}',
)

fig.update_layout(
    title='Monthly Average Windspeed Recorded in Jasper National Park',
    font_size=16,
    legend_font_size=16,
    polar_radialaxis_ticksuffix='',
    polar_angularaxis_rotation=90,
    polar_angularaxis_direction = 'clockwise',


)
fig.show()
