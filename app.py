import streamlit as st

homepage = st.Page("home.py", title="Home")
editions_comparison = st.Page("editions_comparison.py", title="Comparing Editions")
tokyo2020page = st.Page("editions/tokyo2020.py", title="Tokyo 2020")
rio2016page = st.Page("editions/rio2016.py", title="Rio 2016")
london2012page = st.Page("editions/london2012.py", title="London 2012")
beijing2008page = st.Page("editions/beijing2008.py", title="Beijing 2008")
athens2004page = st.Page("editions/athens2004.py", title="Athens 2004")
sydney2000page = st.Page("editions/sydney2000.py", title="Sydney 2000")

pg = st.navigation(
    {
        "": [homepage],
        "Olympics Through the Years": [editions_comparison],
        "Editions": [tokyo2020page, rio2016page, london2012page, beijing2008page, athens2004page, sydney2000page]
    } 
)

pg.run()