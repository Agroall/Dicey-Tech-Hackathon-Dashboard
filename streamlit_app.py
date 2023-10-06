import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
        

# Streamlit app
def app():
    st.title('Time Series Analysis')
    
    # Add a dropdown to select the line plot
    plot_choice = st.selectbox('Select line plot', [
        'Number of Posts Made on All Media Platforms',
        'Average Monthly Impressions Made on All Media',
        'Average Monthly Engagements Made on All Media',
        'Average Monthly Engagements Rate Per Impression Made on All Media'
  
    ])
    
    # Create the selected line plot
    if plot_choice == 'Number of Posts Made on All Media Platforms':
        fig, ax = plt.subplots(figsize=[20, 10])
        start_date = min(media['year_month'].min() for media in mediums)
        end_date = max(media['year_month'].max() for media in mediums)
        date_range = pd.date_range(start=start_date, end=end_date, freq='M')
        for index, media in enumerate(mediums):
            post_count_temp=media.value_counts('year_month').sort_index()
            df={'post_count_temp':post_count_temp}
            post_count_temp=pd.DataFrame(df, index=post_count_temp.index)
            post_count_temp['date']=post_count_temp.index
            sns.lineplot(
                data=post_count_temp,
                x='date',
                y='post_count_temp',
                ax=ax,
                label=mediums_list[index],
                linewidth=3
            )
        ax.set_xticks(range(0, len(date_range), 3))
        ax.set_xticklabels(date_range[::3].strftime('%Y-%m'), rotation=90, fontsize=12)
        ax.set_title('Time Series Analysis of The Number of Posts Made on All Media Platforms')
        ax.legend()
        plt.grid(which='major',axis='y')

    elif plot_choice == 'Average Monthly Impressions Made on All Media':
        fig, ax = plt.subplots(figsize=[20, 10])
        start_date = min(media['year_month'].min() for media in mediums_impression_temp)
        end_date = max(media['year_month'].max() for media in mediums_impression_temp)
        date_range = pd.date_range(start=start_date, end=end_date, freq='M')
        for index, media in enumerate(mediums_impression_temp):
            impressions_avg_temp = media.groupby('year_month')['Impressions'].mean()
            df={'impressions_avg_temp':impressions_avg_temp}
            impressions_avg_temp=pd.DataFrame(df, index=impressions_avg_temp.index)
            impressions_avg_temp['date']=impressions_avg_temp.index
            sns.lineplot(
                data=impressions_avg_temp,
                x='date',
                y='impressions_avg_temp',
                ax=ax,
                label=mediums_list[index],
                linewidth=3
            )
        ax.set_xticks(range(0, len(date_range), 3))
        ax.set_xticklabels(date_range[::3].strftime('%Y-%m'), rotation=90, fontsize=12)
        ax.set_title('Time Series Analysis of The Average Monthly Impressions Made on All Media')
        ax.legend()
        plt.grid(which='major',axis='y')
    elif plot_choice == 'Average Monthly Engagements Made on All Media':
        fig, ax = plt.subplots(figsize=[20, 10])
        start_date = min(media['year_month'].min() for media in mediums_engagement_temp)
        end_date = max(media['year_month'].max() for media in mediums_engagement_temp)
        date_range = pd.date_range(start=start_date, end=end_date, freq='M')
        for index, media in enumerate(mediums_engagement_temp):
            engagement_avg_temp = media.groupby('year_month')['Engagements'].mean()
            engagement_avg_temp[engagement_avg_temp > 1500] = 1200
            df={'engagement_avg_temp':engagement_avg_temp}
            engagement_avg_temp=pd.DataFrame(df, index=engagement_avg_temp.index)
            engagement_avg_temp['date']=engagement_avg_temp.index
            
            sns.lineplot(
                data=engagement_avg_temp,
                x='date',
                y='engagement_avg_temp',
                ax=ax,
                label=mediums_list[index],
                linewidth=3
            )
        ax.set_xticks(range(0, len(date_range), 3))
        ax.set_xticklabels(date_range[::3].strftime('%Y-%m'), rotation=90, fontsize=12)
        plt.grid(which='major',axis='y')
        ax.set_title('Time Series Analysis of The Average Monthly Engagements Made on All Media')
        ax.legend()
    elif plot_choice == 'Average Monthly Engagements Rate Per Impression Made on All Media':
        fig, ax = plt.subplots(figsize=[20, 10])
        start_date = min(media['year_month'].min() for media in mediums)
        end_date = max(media['year_month'].max() for media in mediums)
        date_range = pd.date_range(start=start_date, end=end_date, freq='M')
        for index, media in enumerate(mediums_engagement_temp):
            engagement_avg_temp = media.groupby('year_month')['Engagement Rate (per Impression)'].mean()
            engagement_avg_temp[engagement_avg_temp > 25] = 25
            df={'engagement_avg_temp':engagement_avg_temp}
            engagement_avg_temp=pd.DataFrame(df, index=engagement_avg_temp.index)
            engagement_avg_temp['date']=engagement_avg_temp.index
            
            sns.lineplot(
                data=engagement_avg_temp,
                x='date',
                y='engagement_avg_temp',
                ax=ax,
                label=mediums_list[index],
                linewidth=3
            )
            
        ax.set_xticks(range(0, len(date_range), 3))
        ax.set_xticklabels(date_range[::3].strftime('%Y-%m'), rotation=90, fontsize=12)
        plt.grid(which='major',axis='y')
        ax.set_title('Time Series Analysis of The Average Monthly Engagements Rate Per Impression Made on All Media')
        ax.legend()
    
    
    # Display the selected line plot
    st.pyplot(fig)

# Run the Streamlit app
if __name__ == '__main__':
    app()
