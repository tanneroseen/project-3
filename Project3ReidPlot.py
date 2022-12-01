import plotly.graph_objects as go
import pandas as pd

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

#Manipulating the data from the CSV to give insight
min_grouped_by_week = jasper_data.groupby(pd.Grouper(key = 'Date (Local Standard Time)', freq = 'W-SUN'))['Air Temp. Min. (C)'].min() #On graph date shown is end of the week
max_grouped_by_week = jasper_data.groupby(pd.Grouper(key = 'Date (Local Standard Time)', freq = 'W-SUN'))['Air Temp. Max. (C)'].max()
differce_in_max_and_min = max_grouped_by_week - min_grouped_by_week


#Anything below this is Plotly not matplotlib.pylot

date_range = min_grouped_by_week.keys() #grabs each date (start of each week grouped by) that is used by all graphs as common x-values

fig3 = go.Figure()

fig3.add_trace(go.Scatter(
    x = date_range,
    y = [0 for i in range(len(date_range))],
    name = '0\u00B0 C',
    opacity = 0.5,
    line = dict(color = 'black')
    ))
#fig3.update_traces(line_color = 'black')


fig3.add_trace(go.Scatter(
    x = date_range,
    y = min_grouped_by_week,
    name = 'Minimum Temperature',
    mode = "lines+markers",
    line = dict(color = '#0000FF')
    ))

fig3.add_trace(go.Scatter(
    x = date_range,
    y = max_grouped_by_week,
    name = 'Maximum Temperature',
    mode = 'lines+markers',
    line = dict(color = '#FF0000')
    ))
fig3.add_trace(go.Scatter(
    x = date_range,
    y = differce_in_max_and_min,
    name = 'Difference in Min and Max Temperatures',
    mode = 'lines+markers',
    line = dict(color = '#00FF00')
    ))
fig3.update_layout(
        title = 'Weekly Temperature Extremes and their Difference',
        xaxis_title = 'Date',
        yaxis_title = 'Temperature (\u00B0C)',
        paper_bgcolor = 'powderblue'
        )

fig3.show()
