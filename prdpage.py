import streamlit as st
import pickle
import numpy as np

COUNTRIES = ("United States of America", "Germany", "United Kingdom of Great Britain and Northern Ireland",
             "India", "Canada", "France", "Brazil", "Spain", "Netherlands", "Australia", "Italy", "Poland", "Sweden")

EDUCATION = ("Bachelor", "Masters", "less than bachelor's", "PostGrad")


def load_model():
    with open("saved_model.pkl", "rb") as f:
        data = pickle.load(f)
    return data


data = load_model()
reg = data["model"]
LE_ED = data['le_ed']
LE_CNT = data['le_cnt']


def show_predict_page():
    st.title("SOFTWARE ENGINEER SALARY PREDICTION")
    st.write("""### We need some of your information to continue...""")
    country = st.selectbox("Country", COUNTRIES,key="country")
    education = st.selectbox("Education Level", EDUCATION,key="education")
    year_exp = st.slider("Years of Experiance")
    start = st.button("Calculate Salary")

    if start:
        X = np.array([[country, education, year_exp]])
        X[:, 0] = LE_CNT.transform(X[:, 0])
        X[:, 1] = LE_ED.transform(X[:, 1])
        X = X.astype(float)
        print(X)

        salary = reg.predict(X)
        salary = round(salary[0])
        st.subheader(f"Your estimated salary is💲{salary}")
