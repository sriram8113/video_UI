import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# Function to fetch video details
def fetch_video_details(begin_time, end_time):
    url = 'https://l4azvl84mf.execute-api.us-east-1.amazonaws.com/prod/details'
    params = {'begin_time': begin_time.strftime('%Y-%m-%d %H:%M:%S'), 
              'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S')}
    response = requests.get(url, params=params)
    return response.json()

# Function to fetch count details
def fetch_count_details(begin_time, end_time):
    url = 'https://l4azvl84mf.execute-api.us-east-1.amazonaws.com/prod/count'
    params = {'begin_time': begin_time.strftime('%Y-%m-%d %H:%M:%S'), 
              'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S')}
    response = requests.get(url, params=params)
    return response.json()

# Streamlit UI components
st.title('Video Processing Dashboard')

with st.sidebar:
    st.header('Set Time Frame')
    begin_time = st.date_input("Begin Date", value=datetime.today())
    end_time = st.date_input("End Date", value=datetime.today())
    submit_button = st.button('Fetch Data')


    st.image("CHOP.png", width = 150)

if submit_button:
    video_details = fetch_video_details(begin_time, end_time)
    count_details = fetch_count_details(begin_time, end_time)

    if video_details:
        st.subheader('Video Details')
        if isinstance(video_details, list) and video_details:
            df_videos = pd.DataFrame(video_details)
            st.dataframe(df_videos)
        else:
            st.error("Received unexpected data format or empty list for video details.")

    if count_details:
        st.subheader('Count Details')
        if isinstance(count_details, list) and count_details:
            df_counts = pd.DataFrame(count_details)
            st.dataframe(df_counts)
        else:
            st.error("Received unexpected data format or empty list for count details.")


         # Check for 'total_videos' column and display chart if available
        if 'total_videos' in df_counts.columns and not df_counts.empty:
            total_videos = df_counts['total_videos'].iloc[0]
            df_counts['metadata_present_percent_of_total'] = df_counts['metadata_present_count'] / total_videos * 100
            df_counts['corruption_checks_passed_percent_of_total'] = df_counts['corruption_checks_passed_count'] / total_videos * 100
            df_counts['has_audio_percent_of_total'] = df_counts['has_audio_count'] / total_videos * 100
            df_counts['has_video_percent_of_total'] = df_counts['has_video_count'] / total_videos * 100
            df_counts['notifications_sent_percent_of_total'] = df_counts['notifications_sent_count'] / total_videos * 100

            fig = px.bar(df_counts, 
                         x=['Metadata Present', 'Corruption Checks Passed', 'Has Audio', 'Has Video', 'Notifications Sent'], 
                         y=[df_counts['metadata_present_percent_of_total'].iloc[0], 
                            df_counts['corruption_checks_passed_percent_of_total'].iloc[0], 
                            df_counts['has_audio_percent_of_total'].iloc[0], 
                            df_counts['has_video_percent_of_total'].iloc[0], 
                            df_counts['notifications_sent_percent_of_total'].iloc[0]],
                         title='Percentage of Total Videos by Category')
            st.plotly_chart(fig)
        else:
            st.error("The expected 'total_videos' column is not in the data or the dataframe is empty.")
