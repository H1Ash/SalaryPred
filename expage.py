import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image


def shorten_categories(cat, cutoff):
    categorial_map = {}
    for i in range(len(cat)):
        if cat.values[i] >= cutoff:
            categorial_map[cat.index[i]] = cat.index[i]
        else:
            categorial_map[cat.index[i]] = "other"
    return categorial_map


def clean_exp(x):
    if x == "Less than 1 year":
        return 0.5
    if x == "More than 50 years":
        return 50
    return float(x)


def clean_ed(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor'
    if "Master’s degree" in x:
        return 'Masters'
    if 'Professional degree' in x or 'Other doctoral degree' in x:
        return 'PostGrad'
    return "less than bachelor's"

@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df.rename({"YearsCodePro": "CodingExperiance"}, axis=1)
    df = df[df.Salary.notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    Country_map = shorten_categories(df.Country.value_counts(), 500)
    df.Country = df.Country.map(Country_map)
    df = df[df.Salary <= 175000]
    df = df[df.Salary >= 10000]
    df = df[df.Country != "other"]
    df = df.drop("Employment", axis=1)
    df.EdLevel = df.EdLevel.apply(clean_ed)
    df.CodingExperiance = df.CodingExperiance.apply(clean_exp)
    return df

df = load_data()

@st.cache_resource
def show_img():
    fig = Image.open("corr.png")
    st.image(fig)

def showExplorePage():
    st.title("Behind the scenes...")
    st.write(""" 
    ## Stack Overflow Develper Survey 2022
    """)
    data = df.Country.value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(data,labels=data.index,autopct="%1.1f%%",shadow=True,startangle=90)
    ax1.axis("equal")
    st.write("### number of data from diffrent countries ")
    st.pyplot(fig1)

    st.write(" ### The corelation matrix for better understanding ")
    show_img()

    st.write("### Mean Salary by Country")
    data = df.groupby(["Country"])["Salary"].mean().sort_index(ascending=True)
    st.bar_chart(data)

    st.write("### Mean Salary by Experiance")
    data = df.groupby(["CodingExperiance"])["Salary"].mean().sort_index(ascending=True)
    st.line_chart(data)