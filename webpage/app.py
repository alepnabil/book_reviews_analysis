import streamlit as st
st.set_page_config(page_title='Book reviews analysis', layout='wide')

import requests
import mysql.connector
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from indv_book_page import individual_book_layout
from main_page import main_page_layout
from book_intro import *
from streamlit_lottie import st_lottie



st.set_option('deprecation.showPyplotGlobalUse', False)
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)


def load_lottie_animation(url):
    r=requests.get(url)
    if r.status_code!=200:
            return None
    return r.json()
lotte_animation=load_lottie_animation('https://assets7.lottiefiles.com/private_files/lf30_x8aowqs9.json')


st_lottie(lotte_animation,height=200,key='book')
st.title('Book review analysis')
st.write('Hi there !👋 This is a political philosophy book reviews sentiment analysis dashboard. This projects scrapes book reviews of books (_that I have read or plan to read_) from [Goodreads](https://www.goodreads.com/?ref=nav_hom) and analyzes the data gathered to gain more insights and understanding regarding the overall opinions of other readers.')
st.write(' To know more about this project, check out the Github link : [Project link](https://github.com/alepnabil/book_reviews_analysis)')
st.write('__You can choose whether to see analysis regarding a specific theme/doctrine/ideology 👇__')
st.write('__or each individual books 👈__')
st.write('---')



#Options to navigate to pages with analysis of themes or individual books
options = ['All themes', 
           'Leviathan', 'Second Treatise of Government', 'The social contract',
           'Utilitarianism','The Principles of Morals and Legislation',
           'The state and revolution','Das Kapital'
           'The Garments of Court and Palace: Machiavelli and the World that he Made']

# Create a sidebar with the dropdown menu
selected_option = st.sidebar.selectbox('Select a book', options)

st.sidebar.caption('_It is recommended to close this sidebar for better viewing_')




# Define the pages for each option
if selected_option == 'All themes':
    # This is the main page
    theme_options = ['Social contract','Utilitarianism','Communism','Machiavellianism']
    theme_options_selected=st.selectbox('Select theme',theme_options)        
    main_page_layout(theme_options_selected)


elif selected_option == 'Leviathan':
    # This is the page for Leviathan
    st.text_area(f'This is the page for {selected_option}.',leviathan,height=110)
    individual_book_layout(selected_option)
elif selected_option == 'Second Treatise of Government':
    # This is the page for Second Treatise of Government
    st.text_area(f'This is the page for {selected_option}.',second_treatise_of_government,height=110)
    individual_book_layout(selected_option)
elif selected_option == 'The social contract':
    # This is the page for Second Treatise of Government
    st.text_area(f'This is the page for {selected_option}.',social_contract,height=110)
    individual_book_layout(selected_option)
elif selected_option == 'Utilitarianism':
    # This is the page for Second Treatise of Government
    st.text_area(f'This is the page for {selected_option}.',utilitarianism,height=110)
    individual_book_layout(selected_option)
elif selected_option == 'The Principles of Morals and Legislation':
    # This is the page for Second Treatise of Government
    st.text_area(f'This is the page for {selected_option}.',principles_of_morals_and_legislation,height=110)
    individual_book_layout(selected_option)
elif selected_option == 'The state and revolution':
    # This is the page for Second Treatise of Government
    st.text_area(f'This is the page for {selected_option}.',the_state_and_revolution,height=110)
    individual_book_layout(selected_option)
elif selected_option == 'Das Kapital':
    # This is the page for Second Treatise of Government
    st.text_area(f'This is the page for {selected_option}.',das_kapital,height=110)
    individual_book_layout(selected_option)
elif selected_option == 'The Garments of Court and Palace: Machiavelli and the World that he Made':
    # This is the page for Second Treatise of Government
    st.text_area(f'This is the page for {selected_option}.',machiavelli_and_the_world_he_made,height=110)
    individual_book_layout(selected_option)
