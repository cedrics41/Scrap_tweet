
from cProfile import label
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import base64
import os
import altair as alt
from wordcloud import WordCloud, STOPWORDS

st.set_page_config(page_title='Scraping Tesla', 
page_icon="random", layout="centered", 
initial_sidebar_state="collapsed")

hide_menu = """
<style>
#MainMenu{
    visibility:hidden;
    }
footer{
    visibility:hidden;
}
footer:after{
    content : 'Copyright @2022: SONG MASSON RICOCHIN';
    display:block;
    position:relative;
    color:white;
    visibility: visible;
    padding:5px;
    top:2px;
}
header{
    visibility:hidden;
}
</style>
"""


def plot_means_by_weekday(df):
    domain = ["1.positif", "2.neutral", "3.negatif"]
    range_ = ["green", "white", "red"]

    bar_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('week(Date):O', axis=alt.Axis(title='Week')),
        y=alt.Y('count(sentiment_compound):Q', stack="normalize", axis=alt.Axis(title='Normalization')),
        color=alt.Color("Fin_statement", scale=alt.Scale(domain=domain, range=range_)),
        tooltip='count(sentiment_compound):Q'
    )

    st.altair_chart(bar_chart,use_container_width=True)

    option = st.selectbox(
        'Choose the year',
        ('2022', '2021', '2020'))
    if (option=='2022'):
        df_year = df[(df['Year']==2022)]
        st.write(df_year)
        plot_bar_weekday_percent(df_year)
    elif (option=='2021'):
        df_year = df[(df['Year']==2021)]
        st.write(df_year)
        plot_bar_weekday_percent(df_year)
    elif (option=='2020'):
        df_year = df[(df['Year']==2020)]
        st.write(df_year)
        plot_bar_weekday_percent(df_year)

def plot_bar_weekday_percent(df):
    domain = ["1.positif", "2.neutral", "3.negatif"]
    range_ = ["green", "white", "red"]

    bar_chart_2 = alt.Chart(df).transform_aggregate(
        count='count()',
        groupby=['Fin_statement', 'week']
    ).transform_joinaggregate(
        total='sum(count)',
        groupby=['week'] 
    ).transform_calculate(
        frac=alt.datum.count / alt.datum.total
    ).mark_bar().encode(
        x=alt.X('week:O', axis=alt.Axis(title='Week')),
        y=alt.Y('count:Q', stack="normalize", axis=alt.Axis(title="Percent", format="%")),
        color=alt.Color("Fin_statement", scale=alt.Scale(domain=domain, range=range_)),
        tooltip=[
            alt.Tooltip('count:Q', title="Total tweets"),
            alt.Tooltip('frac:Q', title="Percentage of Students", format='.0%')
        ]
    )
    st.altair_chart(bar_chart_2,use_container_width=True)

   

def plot_means_by_months(df):

    bar_chart = alt.Chart(df).mark_bar().encode(
        x="month(Date):O",
        y=alt.Y('mean(Statement):Q', stack="normalize"),
        color="Fin_statement:N"
    )
    st.altair_chart(bar_chart,use_container_width=True)


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

def contactUs(url):
     st.markdown(f'<p style="font-family:arial; text-align: end; color:Gray; font-size: 15px;">{url}</p>', unsafe_allow_html=True)

def vizu(url):
     st.markdown(f'<p style="font-family:arial; color:White; font-size: 14px;">{url}</p>', unsafe_allow_html=True)

def titre(url):
     st.markdown(f'<p style="font-family:arial; color:White;text-align: center; font-size: 42px;font-weight: bold;">{url}</p>', unsafe_allow_html=True)

def couleur(*args, **kwargs):
    import random
    return "rgb(0, 100, {})".format(random.randint(100, 255))

def read(df):
    return pd.read_csv(df, index_col=[0])  

df = read("Tesla.csv")

add_background('Noir.jpeg')

st.markdown(hide_menu, unsafe_allow_html=True)

select = st.sidebar.selectbox('Pages',['Home','Visualisation','About us'], key = '1')
if select == 'Home':
    titre('Home Page')
    header('We finally choose to do our study on Tesla. It is a brand of manufacturer of electric cars for the general public. The name of the company is chosen as a tribute to Nikola Tesla, an American inventor, and engineer. Tesla was originally run by Martin Eberhard and Marc Tarpenning with Elon Musk as chairman of the board, but the two CEOs decided to step down giving the rights to Elon Musk. Today Tesla has 18.76 billion in revenues and almost a hundred thousand employees (2021). Tesla is now present in most countries as a brand representing quality and latest-generation cars.')
    col1, col2, col3, col4 = st.columns([0.5,1,1,1])
    with col2:
        st.image('tesla.jpeg', caption=None, width=500, use_column_width=None, clamp=False, channels='RGB', output_format='auto')

elif select == 'Visualisation':
    titre('Visualisation')
    col1, col2= st.columns([1,1])
    with col1:
        vizu('Percentage of positif/neutral/negatif')
        df_groupby = df['Fin_statement'].value_counts().reset_index(name='counts')
        fig = px.pie(df_groupby, values="counts", names='index')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        vizu('Percentage of the most User')
        df_groupby = df['User'].value_counts().reset_index(name='counts')
        fig = px.pie(df_groupby.head(5), values="counts", names='index')
        st.plotly_chart(fig,use_container_width=True)
    tweet = df.Tweet.replace('https://t.co/|https://', '', regex = True)
    # generate wordcloud
    wordcloud = WordCloud (
                        background_color = 'white',
                        width = 1920,
                        height = 1080,
                        colormap = "GnBu"
                ).generate(' '.join(tweet))
    fig, ax = plt.subplots()
    plt.imshow(wordcloud)
    st.pyplot(fig)
    header('This is the tweet with the most Like !')
    maxValueLike = df['Like'].idxmax()
    tweet1(df.at[maxValueLike,'User'])
    tweet1(df.at[maxValueLike,'Tweet'])
    tweet1(df.at[maxValueLike,'Like'])
    header('This is the tweet the most positive !')
    maxValuePos = df['sentiment_positive'].idxmax()
    tweet1(df.at[maxValuePos,'User'])
    tweet1(df.at[maxValuePos,'Tweet'])
    header('This is the tweet the most negative !')
    maxValueNeg = df['sentiment_negative'].idxmax()
    tweet1(df.at[maxValueNeg,'User'])
    tweet1(df.at[maxValueNeg,'Tweet'])
    st.write(df)
    st.pyplot(plot_means_by_weekday(df))
    st.pyplot(plot_means_by_months(df))

elif select == 'About us':
    titre('About us')
    header("We are three students in the first year of a master's degree with a view to becoming a computer engineer, specializing in business intelligence and analytics.We chose the second subject that was offered to us because we prefer the field of data processing. This is why this project mixing our passion but also a technology that was unknown to us (scraping) attracted us so much.")
    col1, col2, col3, col4, col5 = st.columns([0.2,0.2,0.2,1,2])
    url = "https://www.linkedin.com/in/cedric-song-7619b91a0/"
    contactUs('Contact Us')
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