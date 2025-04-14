from newsapi import NewsApiClient
import streamlit as st

NEWS_API_KEY = 'b3ca1de47f7247c2901f0a024292d4f2'

def news_section():
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)

    top_headlines = newsapi.get_top_headlines(category='business', language='en')

    # fetch the top news under that category
    Headlines = top_headlines['articles']
    newsArticles = []
    for headline in Headlines:
        if headline['title'] and headline['urlToImage'] and headline['description'] and headline['url']:
            newsArticles.append(headline)

    st.subheader('Latest News', anchor=False)

    cols = []
    cols2 = []
    match(len(newsArticles)):
        case 0:
            st.subheader('No news today! Check back tomorrow.', anchor=False)
        case 1:
            cols = st.columns(1, border=True)
        case 2:
            cols = st.columns(2, border=True)
        case 3:
            cols = st.columns((2, 1, 1), border=True)
        case 4:
            cols = st.columns((2, 1, 1), border=True)
            cols2 = st.columns(1, border=True)
        case 5:
            cols = st.columns((2, 1, 1), border=True)
            cols2 = st.columns(2, border=True)
        case _:
            cols = st.columns((2, 1, 1), border=True)
            cols2 = st.columns((2, 1, 1), border=True)

    for i in range(len(newsArticles)):
        if i == 6:
            break
        if i < 3:
            with cols[i]:
                if i == 0:
                    st.header(newsArticles[i]['title'], anchor=False)
                else:
                    st.subheader(newsArticles[i]['title'], anchor=False)
                st.image(newsArticles[i]['urlToImage'])
                st.write(newsArticles[i]['description'])
                st.write(newsArticles[i]['url'])
        if i >= 3:
            with cols2[i-3]:
                if i == 3:
                    st.header(newsArticles[i]['title'], anchor=False)
                else:
                    st.subheader(newsArticles[i]['title'], anchor=False)
                st.image(newsArticles[i]['urlToImage'])
                st.write(newsArticles[i]['description'])
                st.write(newsArticles[i]['url'])
