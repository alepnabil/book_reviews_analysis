import mysql.connector
import streamlit as st


host=st.secrets["host"]
user=st.secrets["user"]
password=st.secrets["password"]
database=st.secrets["database"]

mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )
