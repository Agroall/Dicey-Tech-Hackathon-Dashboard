# Packages
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from plotly import graph_objs as go


# Configuration
st.set_page_config(layout='wide', initial_sidebar_state='expanded')
with open('style.css') as f:
    st.markdown(f'<style>(f.read())</style>', unsafe_allow_html=True)


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


# Data Lists
mediums = [fb_reduced, ig_reduced, tw_reduced, ln_reduced]
mediums_impression_temp = [fb_reduced_impressed, ig_reduced_impressed, tw_reduced_impressed, ln_reduced_impressed]
mediums_engagement_temp = [fb_reduced_engaged, ig_reduced_engaged, tw_reduced_engaged, ln_reduced_engaged]
mediums_list = ['Facebook', 'Instagram', 'Twitter', 'Linkedin']


# Data Cleaning
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
st.title("`Dicey Tech Hackathon Dashboard`")
st.markdown(' ')
st.markdown(' ')

st.sidebar.header("`Dicey Tech Hackathon`")


# Platform Metrics Per Year
st.sidebar.subheader('Yearly Performance Review')
bar_choice = st.sidebar.selectbox('Select metric', [
    'Number of Posts',
    'Impressions',
    'Engagements'
])


st.sidebar.markdown('---')


# Content Type
st.sidebar.subheader('Most Engaging Types of Post')
content_choice = st.sidebar.selectbox(' Select platform', [
    'Facebook',
    'Instagram',
    'Twitter',
    'Linkedin'
])


st.sidebar.markdown('---')


# Heatmaps Dropdown
st.sidebar.subheader('Best Times To Post')
heatmap_choice = st.sidebar.selectbox('Select platform', [
    'Facebook',
    'Instagram',
    'Twitter',
    'Linkedin',
])


st.sidebar.markdown('---')


# Time Series Analysis Dropdown
st.sidebar.subheader('Time Series Analysis')
plot_choice = st.sidebar.selectbox('Select metric to view', [
    'Number of Posts',
    'Impressions',
    'Engagements',
    'Engagements Rate Per Impression'
])


st.sidebar.markdown('---')


# Metrics
st.markdown('### Performance Summary')
col1, col2, col3 = st.columns(3)
col1.metric("Most Used Platform", "Instagram", "27% of posts")
col2.metric("Most Viewed Platform", "Facebook", "5400 Average Impressions Per Post")
col3.metric("Most Engaging Platform", "Facebook", "3% Average Engagement Rate Per Post")


st.markdown('---')


# Bar_chart_Section
st.markdown('### Yearly Performance Review')
if bar_choice == 'Number of Posts':

    for media in mediums:
        media['year'] = media.Date.apply(lambda x: x.strftime('%Y'))
        media.sort_values('Date', inplace=True)
    
    post_counts = {}
    for index, media in enumerate(mediums):
        post_count_temp = media.value_counts('year').sort_index()
        post_counts[mediums_list[index]] = post_count_temp
    
    media_post_count = pd.DataFrame(post_counts)
    media_post_count['year'] = media_post_count.index
    
    colors = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)',
              'rgb(214, 39, 40)', 'rgb(148, 103, 189)', 'rgb(140, 86, 75)']
    
    data = []
    for i, medium in enumerate(mediums_list):
        trace = go.Bar(x=media_post_count['year'], y=media_post_count[medium], name=medium,
                       marker_color=colors[i % len(colors)])
        data.append(trace)
    
    layout = go.Layout(title='Total Yearly Amount Of Posts For All Media Groups',
                       xaxis=dict(title='Year'),
                       yaxis=dict(title='Post Count'),
                       barmode='group',
                       legend=dict(
                            x=0,
                            y=1.0,
                            bgcolor='rgba(255, 255, 255, 0)',
                            bordercolor='rgba(255, 255, 255, 0)'
                        ),
                        height=800, # Increase the height of the chart
                        width=1000 # Increase the width of the chart
                                      )
    
    fig = go.Figure(data=data, layout=layout)
    fig.show()



elif bar_choice == 'Impressions':
    for media in mediums_impression_temp:
        media['year'] = media.Date.apply(lambda x: x.strftime('%Y'))
        media.sort_values('Date', inplace=True)
    
    post_counts = {}
    for index, media in enumerate(mediums_impression_temp):
        impressions_sum_temp = media.groupby('year')['Impressions'].mean()
        post_counts[mediums_list[index]] = impressions_sum_temp
    
    media_post_count = pd.DataFrame(post_counts)
    media_post_count['year'] = media_post_count.index
    
    colors = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)',
              'rgb(214, 39, 40)', 'rgb(148, 103, 189)', 'rgb(140, 86, 75)']
    
    data = []
    for i, medium in enumerate(mediums_list):
        trace = go.Bar(x=media_post_count['year'], y=media_post_count[medium], name=medium,
                       marker_color=colors[i % len(colors)])
        data.append(trace)
    
    layout = go.Layout(title='Total Yearly Average Impressions For All Media Groups',
                       xaxis=dict(title='Year'),
                       yaxis=dict(title='Impressions'),
                       barmode='group',
                       legend=dict(
                            x=0,
                            y=1.0,
                            bgcolor='rgba(255, 255, 255, 0)',
                            bordercolor='rgba(255, 255, 255, 0)'
                        ),
                        height=800, # Increase the height of the chart
                        width=1000 # Increase the width of the chart
                      )
    
    fig = go.Figure(data=data, layout=layout)
    fig.show()


elif bar_choice == 'Engagements':    
    for media in mediums_impression_temp:
        media['year'] = media.Date.apply(lambda x: x.strftime('%Y'))
        media.sort_values('Date', inplace=True)
    
    post_counts = {}
    for index, media in enumerate(mediums_impression_temp):
        impressions_sum_temp = media.groupby('year')['Engagements'].mean()
        post_counts[mediums_list[index]] = impressions_sum_temp
    
    media_post_count = pd.DataFrame(post_counts)
    media_post_count['year'] = media_post_count.index
    
    colors = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)',
              'rgb(214, 39, 40)', 'rgb(148, 103, 189)', 'rgb(140, 86, 75)']
    
    data = []
    for i, medium in enumerate(mediums_list):
        trace = go.Bar(x=media_post_count['year'], y=media_post_count[medium], name=medium,
                       marker_color=colors[i % len(colors)])
        data.append(trace)
    
    layout = go.Layout(title='Total Yearly Average Engagements For All Media Groups',
                       xaxis=dict(title='Year'),
                       yaxis=dict(title='Engagements'),
                       barmode='group',
                       legend=dict(
                            x=0,
                            y=1.0,
                            bgcolor='rgba(255, 255, 255, 0)',
                            bordercolor='rgba(255, 255, 255, 0)'
                        ),
                        height=800, # Increase the height of the chart
                        width=1000 # Increase the width of the chart
                      )
    
    fig = go.Figure(data=data, layout=layout)
    fig.show()

st.plotly_chart(fig)


st.markdown('---')


st.markdown('### Most Engaging Contents')
col1, col2, col3, col4 = st.columns(4)
col1.metric("Most Engaged Content On Facebook", "Text", "380 Average Engagement Per Post")
col2.metric("Most Engaged Content On Instagram", "Video", "140 Average Engagement Per Post")
col3.metric("Most Engaged Content On Twitter", "Photo", "120 Average Engagement Per Post")
col4.metric("Most Engaged Content On Linkedin", "Photo", "600 Average Engagement Per Post")


st.markdown('---')


# Content Type
st.markdown('### Most Engaging Types of Posts')
if content_choice == 'Facebook':
    rr=[]
    for content in fb_reduced['Content Type'].unique():
        re = fb_reduced[fb_reduced['Content Type']==content]['Engagements'].mean()
        rr.append(re)
    fig = go.Figure([go.Bar(x=fb_reduced['Content Type'].unique(), y=rr)])
    fig.update_layout(title=f'Average Engagement By Content Type For Facebook', xaxis_title='Content Type', yaxis_title='Engagements',
                        height=800, # Increase the height of the chart
                        width=1000 # Increase the width of the chart
                     )
    fig.show()

    st.plotly_chart(fig)


elif content_choice == 'Instagram':
    rr=[]
    for content in ig_reduced['Content Type'].unique():
        re = ig_reduced[ig_reduced['Content Type']==content]['Engagements'].mean()
        rr.append(re)
    fig = go.Figure([go.Bar(x=ig_reduced['Content Type'].unique(), y=rr)])
    fig.update_layout(title=f'Average Engagement By Content Type For Instagram', xaxis_title='Content Type', yaxis_title='Engagements',
                        height=800, # Increase the height of the chart
                        width=1000 # Increase the width of the chart
                     )
    fig.show()

    st.plotly_chart(fig)


elif content_choice == 'Twitter':
    rr=[]
    for content in tw_reduced['Content Type'].unique():
        re = tw_reduced[tw_reduced['Content Type']==content]['Engagements'].mean()
        rr.append(re)
    fig = go.Figure([go.Bar(x=tw_reduced['Content Type'].unique(), y=rr)])
    fig.update_layout(title=f'Average Engagement By Content Type For Twitter', xaxis_title='Content Type', yaxis_title='Engagements',
                        height=800, # Increase the height of the chart
                        width=1000 # Increase the width of the chart
                     )
    fig.show()

    st.plotly_chart(fig)


elif content_choice == 'Linkedin':
    rr=[]
    for content in ln_reduced['Content Type'].unique():
        if content in ['Poll', 'Document']:
            continue
        else:
            re = ln_reduced[ln_reduced['Content Type']==content]['Engagements'].mean()
            rr.append(re)
    lister = list(media['Content Type'].unique())
    lister = [lst for lst in lister if lst not in ['Poll', 'Document']] 
    fig = go.Figure([go.Bar(x=lister, y=rr)])
    fig.update_layout(title=f'Average Engagement By Content Type For Linkedin', xaxis_title='Content Type', yaxis_title='Engagements',
                        height=800, # Increase the height of the chart
                        width=1000 # Increase the width of the chart
                     )
    fig.show()

    st.plotly_chart(fig)


st.markdown('---')


st.markdown('### Best Time To Posts')
col1, col2 = st.columns(2)
col1.metric("Best Period To Post On Facebook", "Saturday, Monday, Friday", "8-12pm")
col2.metric("Best Period To Post On Instagram", "Sunday, Saturday, Friday", "9pm-2am")
col3, col4 = st.columns(2)
col3.metric("Best Period To Post On Twitter", "Sunday, Wednesday, Thursday", "8-12pm")
col4.metric("Best Period To Post On LInkedin", "Saturday, Sunday, Monday", "")



st.markdown('---')


# Posting Times
st.markdown('### Best Times To Post By Average Impression')


# Heatmaps Section
if heatmap_choice == 'Facebook':
    heatmap_data = pd.pivot_table(fb_reduced, values='Impressions', index='day_of_week', columns='hour', aggfunc='median')
    heatmap_data = heatmap_data.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    heatmap_data = heatmap_data[heatmap_data < (heatmap_data.mean() * 2.5)]

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Blues'
    ))

    fig.update_layout(
        title=f'Facebook',
        xaxis=dict(title='Hour'),
        yaxis=dict(title='Day of Week'),
        height=800, # Increase the height of the chart
        width=1000 # Increase the width of the chart
    )

    st.plotly_chart(fig)


elif heatmap_choice == 'Instagram':
    heatmap_data = pd.pivot_table(ig_reduced, values='Impressions', index='day_of_week', columns='hour', aggfunc='median')
    heatmap_data = heatmap_data.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    heatmap_data = heatmap_data[heatmap_data < (heatmap_data.mean() * 2.5)]

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Blues'
    ))

    fig.update_layout(
        title=f'Best Time To Post on Instagram By Impressions',
        xaxis=dict(title='Hour'),
        yaxis=dict(title='Day of Week'),
        height=800, # Increase the height of the chart
        width=1000 # Increase the width of the chart
    )

    st.plotly_chart(fig)


elif heatmap_choice == 'Twitter':
    heatmap_data = pd.pivot_table(tw_reduced, values='Impressions', index='day_of_week', columns='hour', aggfunc='median')
    heatmap_data = heatmap_data.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    heatmap_data = heatmap_data[heatmap_data < (heatmap_data.mean() * 2.5)]

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Blues'
    ))

    fig.update_layout(
        title=f'Best Time To Post on Twitter By Impressions',
        xaxis=dict(title='Hour'),
        yaxis=dict(title='Day of Week'),
        height=800, # Increase the height of the chart
        width=1000 # Increase the width of the chart
    )

    st.plotly_chart(fig)


elif heatmap_choice == 'Linkedin':
    heatmap_data = pd.pivot_table(ln_reduced, values='Impressions', index='day_of_week', columns='hour', aggfunc='median')
    heatmap_data = heatmap_data.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    heatmap_data = heatmap_data[heatmap_data < (heatmap_data.mean() * 2.5)]

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Blues'
    ))

    fig.update_layout(
        title=f'Best Time To Post on Linkedin By Impressions',
        xaxis=dict(title='Hour'),
        yaxis=dict(title='Day of Week'),
        height=800, # Increase the height of the chart
        width=1000 # Increase the width of the chart
    )
    
    st.plotly_chart(fig)


st.markdown('---')


# Time Series Analysis Section#
st.markdown('### Time Series Analysis')
if plot_choice == 'Number of Posts':
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
            # fill='tozeroy'
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
        width=1000 # Increase the width of the chart
    )

    # Create the figure object and plot the chart
    fig = go.Figure(data=traces, layout=layout)
    fig.show()


elif plot_choice == 'Impressions':
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
            # fill='tozeroy'
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
        width=1000
    )
    
    # Create the figure object and plot the chart
    fig = go.Figure(data=traces, layout=layout)
    fig.show()


elif plot_choice == 'Engagements':
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
            # fill='tozeroy'
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
        width=1000
    )
    
    # Create the figure object and plot the chart
    fig = go.Figure(data=traces, layout=layout)
    fig.show()


elif plot_choice == 'Engagements Rate Per Impression':
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
            # fill='tozeroy'
        )
        traces.append(trace)
    
    # Create a layout for the chart
    layout = go.Layout(
        title='Engagements Rate Per Impression',
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
        width=1000
    )
    
    # Create the figure object and plot the chart
    fig = go.Figure(data=traces, layout=layout)
    fig.show()

# Display the selected line plot
st.plotly_chart(fig)




st.sidebar.markdown('''
Created By Abatan Ayodeji (Agroall) For Dicey Tech Hackathon.
''')
