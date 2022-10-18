#pip install streamlit
import streamlit as st
#pip install pandas
import pandas as pd
import smtplib, ssl
import plotly.express as px
import matplotlib.pyplot as plt
import base64
import os
import altair as alt
from email.utils import formataddr
from wordcloud import WordCloud, STOPWORDS


def count_rows(rows):
    return len(rows)

def plot_means_by_weekday(df):
    
    option = st.selectbox(
        'Choose the year',
        ('2022', '2021'))
    if (option=='2022'):
        df_year = df[(df['Year']==2022)]
        plot_bar_weekday_percent(df_year)
    elif (option=='2021'):
        df_year = df[(df['Year']==2021)]
        plot_bar_weekday_percent(df_year)

def plot_bar_weekday_percent(df):
    domain = ["1.positif", "2.neutral", "3.negatif"]
    range_ = ["green", "white", "red"]

    bar_chart_2 = alt.Chart(df).transform_aggregate(
        count='count()',
        groupby=['Fin_statement', 'Week']
    ).transform_joinaggregate(
        total='sum(count)',
        groupby=['Week'] 
    ).transform_calculate(
        frac=alt.datum.count / alt.datum.total
    ).mark_bar().encode(
        x=alt.X('Week:O', axis=alt.Axis(title='Week')),
        y=alt.Y('count:Q', stack="normalize", axis=alt.Axis(title="Percent", format="%")),
        color=alt.Color("Fin_statement", scale=alt.Scale(domain=domain, range=range_)),
        tooltip=[
            alt.Tooltip('count:Q', title="Total tweets"),
            alt.Tooltip('frac:Q', title="Percentage of Students", format='.0%')
        ]
    )
    st.altair_chart(bar_chart_2,use_container_width=True)

   
def tweet_by_month(df):
    st.header('Evolution of tweets per month')
    df_tweets = df.groupby(by='Month', as_index=False).apply(count_rows)
    df_tweets.columns = ['Month', 'Number_of_tweets']
    st.bar_chart(df_tweets, x='Month', y='Number_of_tweets')

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}">
            <img src="data:image/{img_format};base64,{bin_str}" />
        </a>'''
    return html_code

def add_background(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

def header(url):
     st.markdown(f'<p style="font-family:arial; text-align: justify; color:White; font-size: 15px;">{url}</p>', unsafe_allow_html=True)

def tweet1(url):
     st.markdown(f'<p style="font-family:arial; text-align: justify; color:Gray; font-size: 15px;">{url}</p>', unsafe_allow_html=True)

def vizu(url):
     st.markdown(f'<p style="font-family:arial; color:White; font-size: 14px;">{url}</p>', unsafe_allow_html=True)

def titre(url):
     st.markdown(f'<p style="font-family:arial; color:White;text-align: center; font-size: 42px;font-weight: bold;">{url}</p>', unsafe_allow_html=True)

def read(df):
    return pd.read_csv(df, index_col=[0])  

def most_user(df, top_N):
    header('You can change the value to see the most user tweet')
    df_groupby = df['User'].value_counts().reset_index(name='counts')
    fig = px.pie(df_groupby.head(top_N), values='counts', names='index', 
                    title="Percentage of the most User",
                    labels={"index": "Username", "counts": "Number of tweets"})
    st.plotly_chart(fig,use_container_width=True)

def cloud(df):
    tweet = df.Tweet.replace('https://t.co/|https://', '', regex = True)
    # generate wordcloud
    wordcloud = WordCloud (
                        background_color = 'Black',
                        width = 1920,
                        height = 1080,
                        colormap = "GnBu"
                ).generate(' '.join(tweet))
    fig, ax = plt.subplots()
    plt.imshow(wordcloud)
    st.pyplot(fig)

def sentiments(df):
    header('This is the tweet with the most Like !')
    maxValueLike = df['Like'].idxmax()
    tweet1(df.at[maxValueLike,'User'])
    tweet1(df.at[maxValueLike,'Tweet'])
    tweet1(df.at[maxValueLike,'Like'])
    header('This is the tweet the most positive !')
    maxValuePos = df['sentiment_compound'].idxmax()
    tweet1(df.at[maxValuePos,'User'])
    tweet1(df.at[maxValuePos,'Tweet'])
    header('This is the tweet the most negative !')
    maxValueNeg = df['sentiment_compound'].idxmin()
    tweet1(df.at[maxValueNeg,'User'])
    tweet1(df.at[maxValueNeg,'Tweet'])

def send_email():
    titre('Send a Email')
    # Please replace below with your email address and password
    email_from = 'songcedric123@gmail.com'
    password = 'vrbtofdqtvmgcooj'
    email_to = 'cedric.song@efrei.net'

    # Plain Text string as the email message
    header('Your Email Subject')
    subject = st.text_input('')
    header('What is your message')
    body = st.text_area('')

    # Connect to the Gmail SMTP server and Send Email
    # Create a secure default settings context
    context = ssl.create_default_context()
    # Connect to Gmail's SMTP Outgoing Mail server with such context
    if st.button('Send Email'):
        try:
            message = "Subject:{}\n\n{}".format(subject,body)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                # Provide Gmail's login information
                server.login(email_from, password)
                # Send mail with from_addr, to_addrs, msg, which were set up as variables above
                server.sendmail(email_from, email_to, message)
                st.success('Email Send Succefully !')
        except Exception as e:
            if password == "":
                st.error('Please Fill Password Field')
            else:
                a = os.system("ping google.com")
                if a == 1:
                    st.error('Connect To Internet')
                else:
                    st.error('Wrong Email or Password')

def home():
    titre('Home Page')
    header('We finally choose to do our study on Tesla. It is a brand of manufacturer of electric cars for the general public. The name of the company is chosen as a tribute to Nikola Tesla, an American inventor, and engineer. Tesla was originally run by Martin Eberhard and Marc Tarpenning with Elon Musk as chairman of the board, but the two CEOs decided to step down giving the rights to Elon Musk. Today Tesla has 18.76 billion in revenues and almost a hundred thousand employees (2021). Tesla is now present in most countries as a brand representing quality and latest-generation cars.')
    col1, col2, col3, col4 = st.columns([0.5,1,1,1])
    with col2:
        st.image('tesla.jpeg', caption=None, width=500, use_column_width=None, clamp=False, channels='RGB', output_format='auto')

def all_vizu(df):
    titre('Visualisation')
    header('This is the number of tweet on the dataframe:')
    st.write(len(df.index))
    top_N = st.slider(
        "",
        min_value=5,
        max_value=25,
        value=10,
        help="You can choose the number of users with the most tweets. Between 5 and 25, default number is 10.",
        key = 10)
    most_user(df, top_N)
    cloud(df)
    tweet_by_month(df)
    sentiments(df)
    plot_means_by_weekday(df)

def all_about_us():
    titre('About us')
    header("We are three students in the first year of a master's degree with a view to becoming a computer engineer, specializing in business intelligence and analytics.We chose the second subject that was offered to us because we prefer the field of data processing. This is why this project mixing our passion but also a technology that was unknown to us (scraping) attracted us so much.")
    col1, col2, col3, col4, col5 = st.columns([0.2,0.2,0.2,1,2])
    url = "https://www.linkedin.com/in/cedric-song-7619b91a0/"
    header('Our social Media')
    col1, col2, col3, col4, col5 = st.columns([0.2,0.2,0.2,1,2])
    with col1:
        Insta_html = get_img_with_href("Insta.png", 'https://www.instagram.com/teslamotors/')
        st.markdown(Insta_html, unsafe_allow_html=True)
    with col2:
        Twitter_html = get_img_with_href('twitter.png', 'https://twitter.com/Tesla')
        st.markdown(Twitter_html, unsafe_allow_html=True)
    with col3:
        Facebook_html = get_img_with_href('Facebook.png', 'https://www.facebook.com/TeslaMotorsCorp/')
        st.markdown(Facebook_html, unsafe_allow_html=True)
def main(df):
    select = st.sidebar.selectbox('Pages',['Home','Visualisation','About us','Contact us'], key = '1')
    if select == 'Home':
        home()
    elif select == 'Visualisation':
        all_vizu(df)
    elif select == 'About us':
        all_about_us()
    elif select == 'Contact us':
        send_email()
    else:
        st.error("You don't write or choose the good value")
