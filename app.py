import streamlit as st
from prdpage import *
from expage import *

page = st.sidebar.selectbox("*Explore Or Predict*", ("Predict", "Explore"))


if page == "Predict":
    show_predict_page()
else:
    showExplorePage()
