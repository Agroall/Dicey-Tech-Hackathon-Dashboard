import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from plotly import graph_objs as go


st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>(f.read())</style>', unsafe_allow_html=True)

st.sidebar.header("`Dicey Tech Hackathon`")
                  
# Data
fb_reduced = pd.read_csv('Dicey/fb_reduced') 
fb_reduced_engaged = pd.read_csv('Dicey/fb_reduced_engaged') 
fb_reduced_impressed = pd.read_csv('Dicey/fb_reduced_impressed') 
ln_reduced = pd.read_csv('Dicey/ln_reduced') 
ln_reduced_engaged = pd.read_csv('Dicey/ln_reduced_engaged') 
ln_reduced_impressed = pd.read_csv('Dicey/ln_reduced_impressed') 
tw_reduced = pd.read_csv('Dicey/tw_reduced') 
tw_reduced_engaged = pd.read_csv('Dicey/tw_reduced_engaged') 
tw_reduced_impressed = pd.read_csv('Dicey/tw_reduced_impressed') 
ig_reduced = pd.read_csv('Dicey/ig_reduced') 
ig_reduced_engaged = pd.read_csv('Dicey/ig_reduced_engaged') 
ig_reduced_impressed = pd.read_csv('Dicey/ig_reduced_impressed') 


mediums = [fb_reduced, ig_reduced, tw_reduced, ln_reduced]
mediums_impression_temp = [fb_reduced_impressed, ig_reduced_impressed, tw_reduced_impressed, ln_reduced_impressed]
mediums_engagement_temp = [fb_reduced_engaged, ig_reduced_engaged, tw_reduced_engaged, ln_reduced_engaged]
mediums_list = ['Facebook', 'Instagram', 'Twitter', 'Linkedin']

for lister in [mediums, mediums_impression_temp, mediums_engagement_temp]:
    for media in lister:
        media['Date'] = pd.to_datetime(media['Date'], format='%m/%d/%Y %I:%M %p')
        media.sort_values('Date',inplace=True)
        media['year_month'] = media['Date'].apply(lambda x: x.strftime('%Y-%m'))
        media['year'] = media['Date'].apply(lambda x: x.strftime('%Y'))
        media['day_of_week'] = media['Date'].apply(lambda x: x.strftime('%A'))
        media['hour'] = media['Date'].apply(lambda x: x.strftime('%H'))
        media['hour']=media['hour'].astype('int64')
        media['hour_cat']=pd.cut(media['hour'],[0,4,8,12,16,20,24])
        for column in media.columns:
            try:
                media[column] = media[column].str.replace(',', '')
                media[column] = media[column].str.replace('%', '')
            except AttributeError:
                continue
            if column in media.select_dtypes(include='object').columns:
                try:
                    media[column] = media[column].astype('float64')
                except ValueError:
                    continue


        

# Streamlit app
# def app():
st.title('`Dicey Tech Hackathon Dashboard`')

# Add a dropdown to select the line plot
st.sidebar.subheader('Time Series Analysis')
st.markdown('### Time Series Analysis')

plot_choice = st.selectbox('Select metric to view', [
    'Number of Posts Made on All Media Platforms',
    'Average Monthly Impressions Made on All Media',
    'Average Monthly Engagements Made on All Media',
    'Average Monthly Engagements Rate Per Impression Made on All Media'

])
# Create the selected line plot
if plot_choice == 'Number of Posts Made on All Media Platforms':
    traces = []

    start_date = min(media['year_month'].min() for media in mediums)
    end_date = max(media['year_month'].max() for media in mediums)
    date_range = pd.date_range(start=start_date, end=end_date, freq='M') 

    for index, media in enumerate(mediums):
        post_count_temp = media.value_counts('year_month').sort_index()
        trace = go.Scatter(
            x=post_count_temp.index,
            y=post_count_temp,
            name=mediums_list[index],
            line=dict(width=3),
            fill='tozeroy'
        )
        traces.append(trace)

    # Create a layout for the chart
    layout = go.Layout(
        title='Time Series Analysis of The Number of Posts Made on All Media Platforms',
        xaxis=dict(
            tickmode='array',
            tickvals=pd.date_range(start=start_date, end=end_date, freq='M')[::3],
            ticktext=pd.date_range(start=start_date, end=end_date, freq='M')[::3].strftime('%Y-%m'),
            tickangle=90,
            tickfont=dict(size=12)
        ),
        yaxis=dict(title='Number of Posts', showgrid=True), # Add horizontal gridlines
        legend=dict(x=0, y=1),
        margin=dict(l=50, r=50, b=50, t=80, pad=0),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=800, # Increase the height of the chart
        width=1200 # Increase the width of the chart
    )

    # Create the figure object and plot the chart
    fig = go.Figure(data=traces, layout=layout)
    fig.show()


elif plot_choice == 'Average Monthly Impressions Made on All Media':
    traces = []

    start_date = min(media['year_month'].min() for media in mediums_impression_temp)
    end_date = max(media['year_month'].max() for media in mediums_impression_temp)
    date_range = pd.date_range(start=start_date, end=end_date, freq='M')
    
    for index, media in enumerate(mediums_impression_temp):
        impressions_avg_temp = media.groupby('year_month')['Impressions'].mean()
        trace = go.Scatter(
            x=impressions_avg_temp.index,
            y=impressions_avg_temp,
            name=mediums_list[index],
            line=dict(width=3),
            fill='tozeroy'
        )
        traces.append(trace)
    
    # Create a layout for the chart
    layout = go.Layout(
        title='Time Series Analysis of The Average Monthly Impressions Made on All Media',
        xaxis=dict(
            tickmode='array',
            tickvals=pd.date_range(start=start_date, end=end_date, freq='M')[::3],
            ticktext=pd.date_range(start=start_date, end=end_date, freq='M')[::3].strftime('%Y-%m'),
            tickangle=90,
            tickfont=dict(size=12)
        ),
        yaxis=dict(title='Average Monthly Impressions'),
        legend=dict(x=0, y=1),
        margin=dict(l=50, r=50, b=50, t=80, pad=0),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=800,
        width=1200
    )
    
    # Create the figure object and plot the chart
    fig = go.Figure(data=traces, layout=layout)
    fig.show()


elif plot_choice == 'Average Monthly Engagements Made on All Media':
    traces = []

    start_date = min(media['year_month'].min() for media in mediums_engagement_temp)
    end_date = max(media['year_month'].max() for media in mediums_engagement_temp)
    date_range = pd.date_range(start=start_date, end=end_date, freq='M')
    
    for index, media in enumerate(mediums_engagement_temp):
        engagement_avg_temp = media.groupby('year_month')['Engagements'].mean()
        engagement_avg_temp[engagement_avg_temp > 1500] = 1200
        trace = go.Scatter(
            x=engagement_avg_temp.index,
            y=engagement_avg_temp,
            name=mediums_list[index],
            line=dict(width=3),
            fill='tozeroy'
        )
        traces.append(trace)
    
    # Create a layout for the chart
    layout = go.Layout(
        title='Time Series Analysis of The Average Monthly Engagements Made on All Media',
        xaxis=dict(
            tickmode='array',
            tickvals=pd.date_range(start=start_date, end=end_date, freq='M')[::3],
            ticktext=pd.date_range(start=start_date, end=end_date, freq='M')[::3].strftime('%Y-%m'),
            tickangle=90,
            tickfont=dict(size=12)
        ),
        yaxis=dict(title='Average Monthly Engagements', showgrid=True),
        legend=dict(x=0, y=1),
        margin=dict(l=50, r=50, b=50, t=80, pad=0),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=800,
        width=1200
    )
    
    # Create the figure object and plot the chart
    fig = go.Figure(data=traces, layout=layout)
    fig.show()


elif plot_choice == 'Average Monthly Engagements Rate Per Impression Made on All Media':
    traces = []

    start_date = min(media['year_month'].min() for media in mediums)
    end_date = max(media['year_month'].max() for media in mediums)
    date_range = pd.date_range(start=start_date, end=end_date, freq='M')
    
    for index, media in enumerate(mediums_engagement_temp):
        engagement_avg_temp = media.groupby('year_month')['Engagement Rate (per Impression)'].mean()
        engagement_avg_temp[engagement_avg_temp > 25] = 25
        trace = go.Scatter(
            x=engagement_avg_temp.index,
            y=engagement_avg_temp,
            name=mediums_list[index],
            line=dict(width=3),
            fill='tozeroy'
        )
        traces.append(trace)
    
    # Create a layout for the chart
    layout = go.Layout(
        title='Time Series Analysis of The Average Monthly Engagements Rate Per Impression Made on All Media',
        xaxis=dict(
            tickmode='array',
            tickvals=pd.date_range(start=start_date, end=end_date, freq='M')[::3],
            ticktext=pd.date_range(start=start_date, end=end_date, freq='M')[::3].strftime('%Y-%m'),
            tickangle=90,
            tickfont=dict(size=12)
        ),
        yaxis=dict(title='Average Engagements Rate (per Impression)', showgrid=True),
        legend=dict(x=0, y=1),
        margin=dict(l=50, r=50, b=50, t=80, pad=0),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=800,
        width=1200
    )
    
    # Create the figure object and plot the chart
    fig = go.Figure(data=traces, layout=layout)
    fig.show()


# Display the selected line plot
st.plotly_chart(fig)



st.markdown('### Heatmaps')

heatmap_choice = st.selectbox('Select metric to view', [
    'Heatmap of Values by Day of Week and Hour for Facebook',
    'Heatmap of Values by Day of Week and Hour for Instagram',
    'Heatmap of Values by Day of Week and Hour for Twitter',
    'Heatmap of Values by Day of Week and Hour for Linkedin',
])

                              
if heatmap_choice == 'Heatmap of Values by Day of Week and Hour for Facebook':
    # Code for Facebook heatmap ...
    heatmap_data = pd.pivot_table(fb_reduced, values='Impressions', index='day_of_week', columns='hour')
    heatmap_data = heatmap_data.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    heatmap_data = heatmap_data[heatmap_data < (heatmap_data.mean() * 2.5)]

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Blues'
    ))

    fig.update_layout(
        title=f'Heatmap of Values by Day of Week and Hour for Facebook',
        xaxis=dict(title='Hour'),
        yaxis=dict(title='Day of Week'),
        height=800, # Increase the height of the chart
        width=1200 # Increase the width of the chart
    )

    st.plotly_chart(fig)

elif heatmap_choice == 'Heatmap of Values by Day of Week and Hour for Instagram':
    # Code for Instagram heatmap ...
    heatmap_data = pd.pivot_table(ig_reduced, values='Impressions', index='day_of_week', columns='hour')
    heatmap_data = heatmap_data.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    heatmap_data = heatmap_data[heatmap_data < (heatmap_data.mean() * 2.5)]

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Blues'
    ))

    fig.update_layout(
        title=f'Heatmap of Values by Day of Week and Hour for Instagram',
        xaxis=dict(title='Hour'),
        yaxis=dict(title='Day of Week'),
        height=800, # Increase the height of the chart
        width=1200 # Increase the width of the chart
    )

    st.plotly_chart(fig)



elif heatmap_choice == 'Heatmap of Values by Day of Week and Hour for Twitter':
    # Code for Twitter heatmap ...
    heatmap_data = pd.pivot_table(tw_reduced, values='Impressions', index='day_of_week', columns='hour')
    heatmap_data = heatmap_data.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    heatmap_data = heatmap_data[heatmap_data < (heatmap_data.mean() * 2.5)]

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Blues'
    ))

    fig.update_layout(
        title=f'Heatmap of Values by Day of Week and Hour for Twitter',
        xaxis=dict(title='Hour'),
        yaxis=dict(title='Day of Week'),
        height=800, # Increase the height of the chart
        width=1200 # Increase the width of the chart
    )

    st.plotly_chart(fig)

elif heatmap_choice == 'Heatmap of Values by Day of Week and Hour for Linkedin':
    # Code for Linkedin heatmap ...
    heatmap_data = pd.pivot_table(ln_reduced, values='Impressions', index='day_of_week', columns='hour')
    heatmap_data = heatmap_data.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    heatmap_data = heatmap_data[heatmap_data < (heatmap_data.mean() * 2.5)]

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Blues'
    ))

    fig.update_layout(
        title=f'Heatmap of Values by Day of Week and Hour for Linkedin',
        xaxis=dict(title='Hour'),
        yaxis=dict(title='Day of Week'),
        height=800, # Increase the height of the chart
        width=1200 # Increase the width of the chart
    )

    st.plotly_chart(fig)



st.sidebar.markdown('''
---
Created By Abatan Ayodeji (Agroall) For Dicey Tech Hackathon.
''')

# # Run the Streamlit app
# if __name__ == '__main__':
#     app()
