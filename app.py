import streamlit as st

homepage = st.Page("home.py", title="Home")
rio2016page = st.Page("editions/rio2016.py", title="Rio 2016")
tokyo2020page = st.Page("editions/tokyo2020.py", title="Tokyo 2020")

pg = st.navigation(
    {
        "": [homepage],
        "Editions": [rio2016page, tokyo2020page]
    } 
)

pg.run()