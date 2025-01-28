from newsapi import NewsApiClient
import streamlit as st

NEWS_API_KEY = 'b3ca1de47f7247c2901f0a024292d4f2'

def news_section():
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)

    top_headlines = newsapi.get_top_headlines(category='business', language='en')

    # fetch the top news under that category
    Headlines = top_headlines['articles']

    st.subheader('Latest News')
    col1, col2, col3 = st.columns((2, 1, 1), border=True)
    with col1:
        st.header(Headlines[0]['title'])
        st.image(Headlines[0]['urlToImage'])
        st.write(Headlines[0]['description'])
        st.write(Headlines[0]['url'])

    with col2:
        st.subheader(Headlines[1]['title'])
        st.image(Headlines[1]['urlToImage'])
        st.write(Headlines[1]['description'])
        st.write(Headlines[1]['url'])

    with col3:
        st.subheader(Headlines[2]['title'])
        st.image(Headlines[2]['urlToImage'])
        st.write(Headlines[2]['description'])
        st.write(Headlines[2]['url'])
    
    col4, col5, col6 = st.columns((2, 1, 1), border=True)
    with col4:
        st.header(Headlines[3]['title'])
        st.image(Headlines[3]['urlToImage'])
        st.write(Headlines[3]['description'])
        st.write(Headlines[3]['url'])

    with col5:
        st.subheader(Headlines[4]['title'])
        st.image(Headlines[4]['urlToImage'])
        st.write(Headlines[4]['description'])
        st.write(Headlines[4]['url'])

    with col6:
        st.subheader(Headlines[5]['title'])
        st.image(Headlines[5]['urlToImage'])
        st.write(Headlines[5]['description'])
        st.write(Headlines[5]['url'])