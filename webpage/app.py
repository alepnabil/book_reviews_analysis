import streamlit as st
import mysql.connector
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from indv_book_page import individual_book_layout
from main_page import main_page_layout
from book_intro import *

st.set_option('deprecation.showPyplotGlobalUse', False)





st.set_page_config(page_title='Book review analysis', layout='wide')
st.header('Book review analysis')
st.write('Hi there! This is a book reviews sentiment analysis of my own. This projects scrapes book reviews of books that I have read or plan to read from Goodread and analyzes the data gathered to gain more insights and understanding regarding the overall opinions of other readers.')
st.write('---')



#Options to navigate to pages with analysis of themes or individual books
options = ['All themes', 'Leviathan', 'Second Treatise of Government','The social contract']

# Create a sidebar with the dropdown menu
selected_option = st.sidebar.selectbox('Select a book', options)

st.sidebar.caption('_It is recommended to close this sidebar for better viewing_')




# Define the pages for each option
if selected_option == 'All themes':
    # This is the main page
    st.write('__You can choose whether to see analysis regarding a specific theme/doctrine/ideology 👇 or each individual books 👈.__')
    theme_options = ['Social contract','Intro']
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
