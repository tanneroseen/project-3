import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
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

r = monthly_average_windspeed['Wind Speed 10 m Avg. (km/h)'] #Makes the magnitude of the polar plot the monthly avg windspeed
theta = monthly_average_windspeed_direction['Wind Dir. 10 m Avg. '] #makes the angle (or position on the polar plot the avg direction for each month)

monthly_average_windspeed_direction['Compass Direction'] = None #Creates an extra column to populate in the following loop

for count, direction in enumerate(monthly_average_windspeed_direction['Wind Dir. 10 m Avg. ']):  #Between degree values, the values are assigned a direction based on a compass and they are shown in the figure when you hover your mouse over plotted values.
    if 112.5 < direction < 157.5:
        monthly_average_windspeed_direction.iloc[count, 2] = 'S-E'
    elif 157.5 < direction < 202.5:
        monthly_average_windspeed_direction.iloc[count, 2] = 'South'
    if 202.5 < direction < 247.5:
        monthly_average_windspeed_direction.iloc[count, 2] = 'S-W'
    elif 247.5 < direction < 292.5:
        monthly_average_windspeed_direction.iloc[count, 2] = 'West'
    if 292.5 < direction < 337.5:
        monthly_average_windspeed_direction.iloc[count, 2] = 'N-W'
    elif (337.5 < direction < 360) or (0 < direction < 22.5):
        monthly_average_windspeed_direction.iloc[count, 2] = 'North'
    elif (22.5 < direction < 67.5) or (0 < direction < 22.5):
        monthly_average_windspeed_direction.iloc[count, 2] = 'N-E'

monthly_average_windspeed_direction['Date as String'] = monthly_average_windspeed_direction['Date (Local Standard Time)'].dt.strftime('%b %Y') #Converting the dates in the dataframe into strings so that they can be displayed in the graph easily.


fig = go.Figure() #Initializes the figure

fig.add_trace(go.Scatterpolar( #Polar Scatter plot is created with all of the listed values
    r = r,
    theta = theta,
    mode = 'markers',
    marker = dict(
        size=2.5*r,             #Adds variable marker size depending on the magnitude of the wind speed
        color=r,                #Colour is also dynamic with the magnitude of the wind speed
        colorbar=dict(          #Colour bar (displayed on the right of the graph) is generated showing the colour mapped with the magnitude.
            title="Wind Speed Range (km/h)"
        ),
        colorscale="plasma"
)))


fig.update_traces(
    text=monthly_average_windspeed_direction.iloc[:,[3,2]], #Hover text is defined by the date(type: str) and the compass directio(type: str)
    hovertemplate = 'Date: %{text[0]} <extra></extra>' + 
    '<br>Wind speed: %{r:.2f} km/h' +                       #Custom hover text which is displayed when the cursor hovers over a value
    '<br>Direction: %{theta:.2f}°, %{text[1]}',
)

fig.update_layout(
    title='Monthly Average Windspeed and Direction Recorded in Jasper National Park',
    font_size=16,
    legend_font_size=16,
    polar_radialaxis_ticksuffix='',
    polar_angularaxis_rotation=90,
    polar_angularaxis_direction = 'clockwise',


)

fig.show()