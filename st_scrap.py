#pip install streamlit
import streamlit as st
import Fonction

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

st.markdown(hide_menu, unsafe_allow_html=True)

df = Fonction.read("Tesla.csv")
Fonction.add_background('Noir.jpeg')

if __name__ == '__main__':
    Fonction.main(df)