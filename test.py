import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from datetime import datetime as dt
import pytz

st.set_page_config(  #This sets the page name and icon at the top of the browser
    page_title = 'Project 3',
    page_icon = ':monkey:',
    layout = 'centered'
)


jasper_data = pd.read_csv('Jasper_Daily_Weather_Data.csv', encoding= 'unicode_escape')  #Importing the daily data
jasper_data['Date (Local Standard Time)'] = pd.to_datetime(jasper_data['Date (Local Standard Time)']) #Converting tbe 'Date (Local Standard Time)' row to Date time data type for easy use to bundle by week, month etc

jasper_data = jasper_data[(jasper_data['Air Temp. Min. Record Completeness (%)'] == 100)]   #Filtering Each completeness column and only taking rows with 100 in the specified column
jasper_data = jasper_data[jasper_data['Air Temp. Max. Record Completeness (%)'] == 100]
jasper_data = jasper_data[jasper_data['Air Temp. Avg. Record Completeness (%)']  == 100]
jasper_data = jasper_data[jasper_data['Wind Speed 10 m Avg. Record Completeness (%)'] == 100]
jasper_data = jasper_data[jasper_data['Wind Dir. 10 m Avg. Record Completeness (%)'] == 100]

avg_precip = jasper_data.groupby(pd.Grouper(key= 'Date (Local Standard Time)', freq='M'))['Precip. (mm)'].sum() #Sums the percipitation in each month
avg_temp = jasper_data.groupby(pd.Grouper(key= 'Date (Local Standard Time)', freq='M'))['Air Temp. Avg. (C)'].mean() #Does the avg monthly air temp from the daily averages
min_grouped_by_week = jasper_data.groupby(pd.Grouper(key = 'Date (Local Standard Time)', freq = 'W-SUN'))['Air Temp. Min. (C)'].min()
max_grouped_by_week = jasper_data.groupby(pd.Grouper(key = 'Date (Local Standard Time)', freq = 'W-SUN'))['Air Temp. Max. (C)'].max()
date_range = min_grouped_by_week.keys() #grabs each date (start of each week grouped by) that is used by all graphs as common x-values
differce_in_max_and_min = max_grouped_by_week - min_grouped_by_week #Difference between max temperature and min temperature in a month

#All for Windspeed graph below
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
    elif (22.5 < direction < 67.5):
        monthly_average_windspeed_direction.iloc[count, 2] = 'N-E'

monthly_average_windspeed_direction['Date as String'] = monthly_average_windspeed_direction['Date (Local Standard Time)'].dt.strftime('%b %Y') #Converting the dates in the dataframe into strings so that they can be displayed in the graph easily.

#Streamlit doesn't natively support some changes to the webpage so this CSS does that
#Each [] section is a different part in the page 
#The data-testid="stAppViewContainer" part is the whole page and is where we put the background along with its specifications
#The data-testid="stVerticalBlock" part is for the column in the middle with the text and graphs which has the background colour for 
# the section and paddings and width, box-sizing changes the padding of the expander elements
#The header and toolbar parts are for the very top of the page and makes the top bar clear and shifts the toolbar a little to the left 
# so it's more visible
page_css = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url('https://static.vecteezy.com/system/resources/thumbnails/007/515/187/original/timelapse-of-beautiful-blue-sky-in-pure-daylight-with-puffy-fluffy-white-clouds-background-amazing-flying-through-beautiful-thick-fluffy-clouds-nature-and-cloudscape-concept-free-video.jpg');
    background-size: 400%;
    background-repeat: no-repeat;
    background-position: top left;
    background-attachment: local
}

[data-testid="stVerticalBlock"] {
    margin: auto;
    width: 750px;
    padding: 20px;
    background-color: rgba(195, 220, 238, 0.8);
    box-sizing: content-box
}

[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0)
}

[data-testid="stToolbar"] {
    right: 2rem
}
</style>
"""

st.markdown(page_css, unsafe_allow_html=True)  #Takes the CSS and applies it to the page

now = dt.now(pytz.timezone('Canada/Mountain')).strftime('%B %d, %Y %X')  #Gets the current date and time


#Each write section is a different section of text
st.write('''
    # ENDG 310 Project 3
    _Weather Data Recorded in Jasper National Park_
''')

st.write(
    'By: Tanner Oseen, Reid Moline, Morgan Hendry, and Gavin Scott'
)

#Shows the current date and time
st.write(
    'The current date and time is: ',
    now
)

#Has a hyperlink to the page where we got our data
url = "https://acis.alberta.ca/weather-data-viewer.jsp"
st.write(
    "More recent data is available [here](%s)" % url
)

#The multiselect bar that allows freedom for what graphs are displayed
option = st.multiselect(
    'What graphs would you like to display?',
    ['Precipitation', 'Temperature', 'Wind'],
    []
)

#Italics graph "instructions"
st.write('''
    _Graphs can be zoomed and scrolled over to see data points._
    _Click the home button at the top of each graph to reset axis._
    _Lines on the tremperature graph can be turned on and off as desired._
''')

#The next parts show each graph if it has been selected in the multiselect bar
#Each graph has similar customization with regard to colours and text
if 'Precipitation' in option:  #First precipitation graph
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x = pd.date_range("2019-10-03", "2022-11-03", freq='M'), #Date range for data
        y = avg_temp,
        mode='markers', #Sets what the plot looks like whether that's lines or dots or a combination of both
        marker=dict( 
            color=avg_temp, #Variable colour for the points
            colorscale="Viridis", #Theme of colour
            size=avg_precip, #Size of points
            colorbar = dict( 
                title="Type of Precipitation", #Title for colour bar
                tickvals = [-10,0,15],  #Potistion of colourbar labels
                ticktext = ['Snow', 'Sleet', 'Rain'] #Colour bar labels
            ),
        ),
    ))

    #Updates final visuals for the graph
    fig1.update_layout(
        title = dict(
            text="Monthly Average Precipitation Type and Amount",
            font=dict(
                family="Arial",
                size=20,    #Allows the title to have a different font size than the rest of the graph
                color='#000000'
            ),
        ),
        xaxis_title = 'Date',
        yaxis_title = 'Temperature (\u00B0C)',  #Temperature with degrees sign
        plot_bgcolor = 'rgba(255, 255, 255, 0.3)',  #Colour of the data area, set to white with 30% opacity
        paper_bgcolor = 'rgba(0,0,0,0)' #Colour of the whole plot, set to transparent
    )


    st.plotly_chart(fig1)   #Final display of the chart

    #An expander that displays the information of the graph
    with st.expander("Explanation"):
        st.write(
            'The above chart displays date vs temperature throughout each month from October 2019 to September 2022.'
            'The size of each bubble represents the amount of precipitation in the month and the colour corresponds to the type of precipitation whether that is rain or snow.'
        )

#Temperature graph with similar customization to precipitation graph
if 'Temperature' in option:   
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(  #Each trace is a different line for min, max, and difference of temperatures as well as mid line for 0 degrees C
        x = date_range,
        y = [0 for i in range(len(date_range))],
        name = '0\u00B0 C',
        opacity = 0.5,
        line = dict(color = 'black')
        ))
    fig3.add_trace(go.Scatter(
        x = date_range,
        y = min_grouped_by_week,
        name = 'Minimum Temperature',
        mode = "lines+markers", #Plots a line with points where the data is 
        ))
    fig3.add_trace(go.Scatter(
        x = date_range,
        y = max_grouped_by_week,
        name = 'Maximum Temperature',
        mode = 'lines+markers',
        ))
    fig3.add_trace(go.Scatter(
        x = date_range,
        y = differce_in_max_and_min,
        name = 'Difference in Min and Max Temperatures',
        mode = 'lines+markers',
        ))
    fig3.update_layout(
        title = dict(
            text='Weekly Temperature Extremes and their Difference',
            font=dict(
                family="Arial",
                size=20,
                color='#000000'
            ),
        ),
        xaxis_title = 'Date',
        yaxis_title = 'Temperature (\u00B0C)',
        plot_bgcolor = 'rgba(255, 255, 255, 0.3)',
        paper_bgcolor = 'rgba(0,0,0,0)',
        legend=dict(
            orientation="h",    #Orients the legend horizontally and specifies position
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))

    st.plotly_chart(fig3)

    with st.expander("Explanation"):
        st.write(
            'The above chart displays date vs maximum, minimum, and average temperature throughout each week from October 2019 to September 2022.',
        )

#Wind speed and direction graph
if 'Wind' in option:
    fig2 = go.Figure() #Initializes the figure

    fig2.add_trace(go.Scatterpolar( #Polar scatter plot is created with all of the listed values
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


    fig2.update_traces(
        text=monthly_average_windspeed_direction.iloc[:,[3,2]], #Hover text is defined by the date(type: str) and the compass directio(type: str)
        hovertemplate = 'Date: %{text[0]} <extra></extra>' + 
        '<br>Wind speed: %{r:.2f} km/h' +                       #Custom hover text which is displayed when the cursor hovers over a value
        '<br>Direction: %{theta:.2f}°, %{text[1]}',
    )

    fig2.update_layout(
        title=dict(
            text='Monthly Average Windspeed and Direction',
            font=dict(
                family="Arial",
                size=20,
                color='#000000'
            ),
            
        ),
        polar_radialaxis_ticksuffix='',
        polar_angularaxis_rotation=90,
        polar_angularaxis_direction = 'clockwise',
        polar = dict(bgcolor = "rgba(255, 255, 255, 0.3)"),
        paper_bgcolor = 'rgba(0,0,0,0)'
    )

    st.plotly_chart(fig2)

    with st.expander("Explanation"):
        st.write(
            'The above chart displays date vs average windspeed and direction throughout each month from October 2019 to September 2022.',
            'The size and colour of each bubble represent the average strength of the wind in that month.'
        )